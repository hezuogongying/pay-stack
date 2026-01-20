"""
支付宝支付客户端
遵循单一职责原则 - 专门负责支付宝支付
"""

import logging
from typing import Optional, Dict, Any
from urllib.parse import urlencode

from gopay.client import PaymentClient
from gopay.config import AlipayConfig
from gopay.http import HttpClient
from gopay.utils.datastructure import BodyMap, ResponseData
from gopay.utils.signer import SignerFactory
from gopay.exceptions import PaymentError, SignError


logger = logging.getLogger(__name__)


class AlipayClient(PaymentClient):
    """
    支付宝支付客户端
    支持支付宝网页支付、手机网站支付、APP支付等多种支付方式
    """

    def __init__(self, config: AlipayConfig):
        """
        初始化支付宝客户端
        :param config: 支付宝配置
        """
        if not isinstance(config, AlipayConfig):
            raise ValueError("配置必须是 AlipayConfig 类型")

        super().__init__(config)
        self.config: AlipayConfig = config

        # 初始化HTTP客户端
        self.http_client = HttpClient(
            timeout=config.timeout,
            max_retries=config.http_max_retries,
            retry_interval=config.http_retry_interval,
            enable_log=config.enable_log,
        )

        # 获取签名器
        self.signer = SignerFactory.get_signer(config.sign_type)

    def _build_common_params(self) -> Dict[str, Any]:
        """构建公共参数"""
        return {
            "app_id": self.config.app_id,
            "method": "",  # 具体接口方法名
            "format": self.config.format,
            "charset": self.config.charset,
            "sign_type": self.config.sign_type,
            "timestamp": self._get_timestamp(),
            "version": "1.0",
        }

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _sign_request(self, params: Dict[str, Any]) -> str:
        """
        对请求参数签名
        :param params: 请求参数
        :return: 签名
        """
        # 过滤空值和sign字段
        filtered_params = {k: v for k, v in params.items() if v not in [None, ""] and k != "sign"}
        # 按key排序
        sorted_params = sorted(filtered_params.items())
        # 拼接参数
        param_str = "&".join([f"{k}={v}" for k, v in sorted_params])

        private_key = self.config.get_app_private_key()
        if not private_key:
            raise SignError("应用私钥未配置", "ALIPAY")

        return self.signer.sign(param_str, private_key)

    def _verify_response(self, params: Dict[str, Any], sign: str) -> bool:
        """
        验证响应签名
        :param params: 响应参数
        :param sign: 签名
        :return: 是否验证通过
        """
        public_key = self.config.get_alipay_public_key()
        if not public_key:
            logger.warning("支付宝公钥未配置,跳过验签")
            return True

        # 过滤空值和sign字段
        filtered_params = {k: v for k, v in params.items() if v not in [None, ""] and k != "sign"}
        # 按key排序
        sorted_params = sorted(filtered_params.items())
        # 拼接参数
        param_str = "&".join([f"{k}={v}" for k, v in sorted_params])

        return self.signer.verify(param_str, sign, public_key)

    def _do_request(self, method: str, biz_content: Dict[str, Any], **kwargs) -> ResponseData:
        """
        执行API请求
        :param method: API方法名
        :param biz_content: 业务参数
        :param kwargs: 其他参数
        :return: 响应数据
        """
        # 构建请求参数
        params = self._build_common_params()
        params["method"] = method

        # 添加业务参数
        import json
        params["biz_content"] = json.dumps(biz_content, ensure_ascii=False)

        # 添加其他参数
        if self.config.notify_url:
            params["notify_url"] = self.config.notify_url
        if self.config.return_url:
            params["return_url"] = self.config.return_url

        params.update(kwargs)

        # 签名
        params["sign"] = self._sign_request(params)

        # 发送请求
        try:
            response = self.http_client.post(
                self.config.gateway_url,
                data=params,
            )

            if response.status_code != 200:
                return ResponseData.error_response(
                    error=f"HTTP请求失败: {response.status_code}",
                    code=str(response.status_code),
                    raw_response=response.text,
                )

            # 解析响应
            result = response.json()
            response_key = f"{method.replace(".", "_")}_response"

            if response_key not in result:
                return ResponseData.error_response(
                    error="响应格式错误",
                    raw_response=response.text,
                )

            response_data = result[response_key]
            sign = result.get("sign", "")

            # 验签
            if not self._verify_response(response_data, sign):
                logger.warning("响应验签失败")

            # 检查业务状态
            if response_data.get("code") != "10000":
                return ResponseData.error_response(
                    error=response_data.get("msg", "请求失败"),
                    code=response_data.get("code"),
                    raw_response=response.text,
                )

            return ResponseData.success_response(
                data=response_data,
                raw_response=response.text,
            )

        except Exception as e:
            logger.error(f"请求失败: {e}")
            return ResponseData.error_response(
                error=str(e),
                raw_response=None,
            )

    # ==================== 支付接口 ====================

    def trade_page_pay(self, params: BodyMap) -> ResponseData:
        """
        统一收单下单并支付页面接口
        适用于PC网站支付
        文档: https://opendocs.alipay.com/open/028r8t

        :param params: 参数对象
        :return: 支付URL
        """
        biz_content = params.to_dict()

        # 构建请求参数
        request_params = self._build_common_params()
        request_params["method"] = "alipay.trade.page.pay"

        import json
        request_params["biz_content"] = json.dumps(biz_content, ensure_ascii=False)

        if self.config.notify_url:
            request_params["notify_url"] = self.config.notify_url
        if self.config.return_url:
            request_params["return_url"] = self.config.return_url

        # 签名
        request_params["sign"] = self._sign_request(request_params)

        # 构建支付URL
        pay_url = f"{self.config.gateway_url}?{urlencode(request_params)}"

        return ResponseData.success_response(
            data={"pay_url": pay_url},
        )

    def trade_wap_pay(self, params: BodyMap) -> ResponseData:
        """
        手机网站支付接口
        适用于H5支付
        文档: https://opendocs.alipay.com/open/028r8t

        :param params: 参数对象
        :return: 支付URL
        """
        biz_content = params.to_dict()

        # 构建请求参数
        request_params = self._build_common_params()
        request_params["method"] = "alipay.trade.wap.pay"

        import json
        request_params["biz_content"] = json.dumps(biz_content, ensure_ascii=False)

        if self.config.notify_url:
            request_params["notify_url"] = self.config.notify_url
        if self.config.return_url:
            request_params["return_url"] = self.config.return_url

        # 签名
        request_params["sign"] = self._sign_request(request_params)

        # 构建支付URL
        pay_url = f"{self.config.gateway_url}?{urlencode(request_params)}"

        return ResponseData.success_response(
            data={"pay_url": pay_url},
        )

    def trade_app_pay(self, params: BodyMap) -> ResponseData:
        """
        APP支付接口
        适用于APP支付
        文档: https://opendocs.alipay.com/open/028r8t

        :param params: 参数对象
        :return: 支付订单字符串
        """
        biz_content = params.to_dict()

        # 构建请求参数
        request_params = self._build_common_params()
        request_params["method"] = "alipay.trade.app.pay"

        import json
        request_params["biz_content"] = json.dumps(biz_content, ensure_ascii=False)

        if self.config.notify_url:
            request_params["notify_url"] = self.config.notify_url

        # 签名
        request_params["sign"] = self._sign_request(request_params)

        # 构建支付订单字符串
        order_string = urlencode(request_params)

        return ResponseData.success_response(
            data={"order_string": order_string},
        )

    def trade_create(self, params: BodyMap) -> ResponseData:
        """
        统一收单交易创建接口
        适用于商户通过API创建交易
        文档: https://opendocs.alipay.com/open/028r8t

        :param params: 参数对象
        :return: 交易创建结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.trade.create", biz_content)

    def trade_query(self, out_trade_no: Optional[str] = None, trade_no: Optional[str] = None) -> ResponseData:
        """
        统一收单线下交易查询
        文档: https://opendocs.alipay.com/open/028r8t

        :param out_trade_no: 商户订单号
        :param trade_no: 支付宝交易号
        :return: 查询结果
        """
        if not out_trade_no and not trade_no:
            raise PaymentError("out_trade_no和trade_no至少需要传一个")

        biz_content = {}
        if out_trade_no:
            biz_content["out_trade_no"] = out_trade_no
        if trade_no:
            biz_content["trade_no"] = trade_no

        return self._do_request("alipay.trade.query", biz_content)

    def trade_close(self, out_trade_no: Optional[str] = None, trade_no: Optional[str] = None) -> ResponseData:
        """
        统一收单交易关闭接口
        文档: https://opendocs.alipay.com/open/028r8t

        :param out_trade_no: 商户订单号
        :param trade_no: 支付宝交易号
        :return: 关闭结果
        """
        if not out_trade_no and not trade_no:
            raise PaymentError("out_trade_no和trade_no至少需要传一个")

        biz_content = {}
        if out_trade_no:
            biz_content["out_trade_no"] = out_trade_no
        if trade_no:
            biz_content["trade_no"] = trade_no

        return self._do_request("alipay.trade.close", biz_content)

    def trade_cancel(self, out_trade_no: Optional[str] = None, trade_no: Optional[str] = None) -> ResponseData:
        """
        统一收单交易撤销接口
        文档: https://opendocs.alipay.com/open/028r8t

        :param out_trade_no: 商户订单号
        :param trade_no: 支付宝交易号
        :return: 撤销结果
        """
        if not out_trade_no and not trade_no:
            raise PaymentError("out_trade_no和trade_no至少需要传一个")

        biz_content = {}
        if out_trade_no:
            biz_content["out_trade_no"] = out_trade_no
        if trade_no:
            biz_content["trade_no"] = trade_no

        return self._do_request("alipay.trade.cancel", biz_content)

    # ==================== 退款接口 ====================

    def trade_refund(
        self,
        refund_amount: float,
        out_trade_no: Optional[str] = None,
        trade_no: Optional[str] = None,
        out_request_no: Optional[str] = None,
        refund_reason: Optional[str] = None,
        **kwargs
    ) -> ResponseData:
        """
        统一收单交易退款接口
        文档: https://opendocs.alipay.com/open/028r8t

        :param refund_amount: 退款金额
        :param out_trade_no: 商户订单号
        :param trade_no: 支付宝交易号
        :param out_request_no: 退款请求号
        :param refund_reason: 退款原因
        :param kwargs: 其他参数
        :return: 退款结果
        """
        if not out_trade_no and not trade_no:
            raise PaymentError("out_trade_no和trade_no至少需要传一个")

        biz_content = {
            "refund_amount": str(refund_amount),
        }

        if out_trade_no:
            biz_content["out_trade_no"] = out_trade_no
        if trade_no:
            biz_content["trade_no"] = trade_no
        if out_request_no:
            biz_content["out_request_no"] = out_request_no
        if refund_reason:
            biz_content["refund_reason"] = refund_reason

        biz_content.update(kwargs)

        return self._do_request("alipay.trade.refund", biz_content)

    def trade_fastpay_refund_query(
        self,
        out_trade_no: Optional[str] = None,
        trade_no: Optional[str] = None,
        out_request_no: Optional[str] = None,
    ) -> ResponseData:
        """
        统一收单交易退款查询
        文档: https://opendocs.alipay.com/open/028r8t

        :param out_trade_no: 商户订单号
        :param trade_no: 支付宝交易号
        :param out_request_no: 退款请求号
        :return: 退款查询结果
        """
        if not out_trade_no and not trade_no:
            raise PaymentError("out_trade_no和trade_no至少需要传一个")

        biz_content = {}
        if out_trade_no:
            biz_content["out_trade_no"] = out_trade_no
        if trade_no:
            biz_content["trade_no"] = trade_no
        if out_request_no:
            biz_content["out_request_no"] = out_request_no

        return self._do_request("alipay.trade.fastpay.refund.query", biz_content)

    # ==================== 实现基类接口 ====================

    def create_order(self, params: BodyMap) -> ResponseData:
        """创建订单"""
        return self.trade_create(params)

    def query_order(self, order_no: str, trade_no: Optional[str] = None) -> ResponseData:
        """查询订单"""
        return self.trade_query(out_trade_no=order_no, trade_no=trade_no)

    def close_order(self, order_no: str, trade_no: Optional[str] = None) -> ResponseData:
        """关闭订单"""
        return self.trade_close(out_trade_no=order_no, trade_no=trade_no)

    def refund(
        self,
        order_no: str,
        refund_amount: float,
        refund_no: Optional[str] = None,
        **kwargs
    ) -> ResponseData:
        """申请退款"""
        return self.trade_refund(
            refund_amount=refund_amount,
            out_trade_no=order_no,
            out_request_no=refund_no,
            **kwargs
        )

    def query_refund(self, refund_no: str, order_no: Optional[str] = None) -> ResponseData:
        """查询退款"""
        return self.trade_fastpay_refund_query(
            out_trade_no=order_no,
            out_request_no=refund_no,
        )

    def verify_notify(self, data: Dict[str, Any], signature: str) -> bool:
        """验证异步通知"""
        public_key = self.config.get_alipay_public_key()
        if not public_key:
            logger.warning("支付宝公钥未配置,无法验签")
            return False

        # 过滤空值和sign字段
        filtered_data = {k: v for k, v in data.items() if v not in [None, ""] and k != "sign"}
        # 按key排序
        sorted_params = sorted(filtered_data.items())
        # 拼接参数
        param_str = "&".join([f"{k}={v}" for k, v in sorted_params])

        return self.signer.verify(param_str, signature, public_key)
