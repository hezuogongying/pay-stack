"""
微信支付客户端
遵循单一职责原则 - 专门负责微信支付
"""

import logging
import hashlib
import random
import string
from typing import Optional, Dict, Any
from datetime import datetime

from gopay.client import PaymentClient
from gopay.config import WechatConfig
from gopay.http import HttpClient
from gopay.utils.datastructure import BodyMap, XmlMap, ResponseData
from gopay.utils.signer import SignerFactory
from gopay.exceptions import PaymentError, SignError


logger = logging.getLogger(__name__)


class WechatClient(PaymentClient):
    """
    微信支付客户端
    支持公众号支付、小程序支付、APP支付、H5支付等多种支付方式
    """

    def __init__(self, config: WechatConfig):
        """
        初始化微信支付客户端
        :param config: 微信支付配置
        """
        if not isinstance(config, WechatConfig):
            raise ValueError("配置必须是 WechatConfig 类型")

        super().__init__(config)
        self.config: WechatConfig = config

        # 初始化HTTP客户端
        self.http_client = HttpClient(
            timeout=config.timeout,
            max_retries=config.http_max_retries,
            retry_interval=config.http_retry_interval,
            enable_log=config.enable_log,
        )

        # 获取签名器
        self.signer = SignerFactory.get_signer(config.sign_type)

    def _generate_nonce_str(self) -> str:
        """生成随机字符串"""
        return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

    def _sign_params(self, params: Dict[str, Any]) -> str:
        """
        对参数签名
        :param params: 参数字典
        :return: 签名
        """
        if not self.config.api_key:
            raise SignError("API密钥未配置", "WECHAT")

        # 过滤空值和sign字段
        filtered_params = {k: v for k, v in params.items() if v not in [None, ""] and k != "sign"}
        # 按key排序
        sorted_params = sorted(filtered_params.items())
        # 拼接参数
        param_str = "&".join([f"{k}={v}" for k, v in sorted_params])

        # 签名
        return self.signer.sign(param_str, self.config.api_key)

    def _verify_response(self, params: Dict[str, Any], sign: str) -> bool:
        """
        验证响应签名
        :param params: 响应参数
        :param sign: 签名
        :return: 是否验证通过
        """
        if not self.config.api_key:
            logger.warning("API密钥未配置,跳过验签")
            return True

        # 过滤空值和sign字段
        filtered_params = {k: v for k, v in params.items() if v not in [None, ""] and k != "sign"}
        # 按key排序
        sorted_params = sorted(filtered_params.items())
        # 拼接参数
        param_str = "&".join([f"{k}={v}" for k, v in sorted_params])

        calculated_sign = self.signer.sign(param_str, self.config.api_key)
        return calculated_sign == sign

    def _build_common_params(self) -> Dict[str, Any]:
        """构建公共参数"""
        return {
            "appid": self.config.app_id,
            "mch_id": self.config.mch_id,
            "nonce_str": self._generate_nonce_str(),
        }

    def _do_request(self, url: str, params: Dict[str, Any]) -> ResponseData:
        """
        执行API请求
        :param url: 请求URL
        :param params: 请求参数
        :return: 响应数据
        """
        # 签名
        params["sign"] = self._sign_params(params)

        # 构建XML
        xml_data = XmlMap()
        for k, v in params.items():
            xml_data.set(k, v)
        xml_str = xml_data.to_xml()

        # 发送请求
        try:
            response = self.http_client.post(
                url,
                data=xml_str.encode("utf-8"),
                headers={"Content-Type": "application/xml"},
            )

            if response.status_code != 200:
                return ResponseData.error_response(
                    error=f"HTTP请求失败: {response.status_code}",
                    code=str(response.status_code),
                    raw_response=response.text,
                )

            # 解析XML响应
            result_xml = XmlMap.from_xml(response.text)
            result = result_xml.to_dict()

            # 验签
            if "sign" in result:
                if not self._verify_response(result, result["sign"]):
                    logger.warning("响应验签失败")

            # 检查业务状态
            if result.get("return_code") != "SUCCESS":
                return ResponseData.error_response(
                    error=result.get("return_msg", "请求失败"),
                    code=result.get("return_code"),
                    raw_response=response.text,
                )

            if result.get("result_code") != "SUCCESS":
                return ResponseData.error_response(
                    error=result.get("err_code_des", "交易失败"),
                    code=result.get("err_code"),
                    raw_response=response.text,
                )

            return ResponseData.success_response(
                data=result,
                raw_response=response.text,
            )

        except Exception as e:
            logger.error(f"请求失败: {e}")
            return ResponseData.error_response(
                error=str(e),
                raw_response=None,
            )

    # ==================== 支付接口 ====================

    def unified_order(
        self,
        body: str,
        out_trade_no: str,
        total_fee: int,
        spbill_create_ip: str,
        trade_type: str,
        **kwargs
    ) -> ResponseData:
        """
        统一下单接口
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param body: 商品描述
        :param out_trade_no: 商户订单号
        :param total_fee: 总金额(分)
        :param spbill_create_ip: 终端IP
        :param trade_type: 交易类型(JSAPI,NATIVE,APP等)
        :param kwargs: 其他参数
        :return: 下单结果
        """
        params = self._build_common_params()
        params.update({
            "body": body,
            "out_trade_no": out_trade_no,
            "total_fee": total_fee,
            "spbill_create_ip": spbill_create_ip,
            "trade_type": trade_type,
        })

        if self.config.notify_url:
            params["notify_url"] = self.config.notify_url

        # 添加可选参数
        params.update(kwargs)

        url = f"{self.config.gateway_url}/pay/unifiedorder"
        return self._do_request(url, params)

    def order_query(self, out_trade_no: Optional[str] = None, transaction_id: Optional[str] = None) -> ResponseData:
        """
        查询订单接口
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param out_trade_no: 商户订单号
        :param transaction_id: 微信订单号
        :return: 查询结果
        """
        if not out_trade_no and not transaction_id:
            raise PaymentError("out_trade_no和transaction_id至少需要传一个")

        params = self._build_common_params()
        if out_trade_no:
            params["out_trade_no"] = out_trade_no
        if transaction_id:
            params["transaction_id"] = transaction_id

        url = f"{self.config.gateway_url}/pay/orderquery"
        return self._do_request(url, params)

    def close_order(self, out_trade_no: str) -> ResponseData:
        """
        关闭订单接口
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param out_trade_no: 商户订单号
        :return: 关闭结果
        """
        params = self._build_common_params()
        params["out_trade_no"] = out_trade_no

        url = f"{self.config.gateway_url}/pay/closeorder"
        return self._do_request(url, params)

    # ==================== 退款接口 ====================

    def refund(
        self,
        out_trade_no: str,
        out_refund_no: str,
        total_fee: int,
        refund_fee: int,
        **kwargs
    ) -> ResponseData:
        """
        申请退款接口
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param out_trade_no: 商户订单号
        :param out_refund_no: 退款单号
        :param total_fee: 总金额(分)
        :param refund_fee: 退款金额(分)
        :param kwargs: 其他参数
        :return: 退款结果
        """
        params = self._build_common_params()
        params.update({
            "out_trade_no": out_trade_no,
            "out_refund_no": out_refund_no,
            "total_fee": total_fee,
            "refund_fee": refund_fee,
        })

        params.update(kwargs)

        url = f"{self.config.gateway_url}/secapi/pay/refund"

        # 退款需要证书
        cert_content = self.config.get_cert_content()
        key_content = self.config.get_key_content()

        if not cert_content or not key_content:
            logger.warning("退款需要证书,但证书未配置")

        # TODO: 添加证书支持
        # 目前先使用普通请求
        return self._do_request(url, params)

    def refund_query(self, out_refund_no: Optional[str] = None, transaction_id: Optional[str] = None) -> ResponseData:
        """
        查询退款接口
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param out_refund_no: 退款单号
        :param transaction_id: 微信订单号
        :return: 查询结果
        """
        if not out_refund_no and not transaction_id:
            raise PaymentError("out_refund_no和transaction_id至少需要传一个")

        params = self._build_common_params()
        if out_refund_no:
            params["out_refund_no"] = out_refund_no
        if transaction_id:
            params["transaction_id"] = transaction_id

        url = f"{self.config.gateway_url}/pay/refundquery"
        return self._do_request(url, params)

    # ==================== 实现基类接口 ====================

    def create_order(self, params: BodyMap) -> ResponseData:
        """创建订单"""
        params_dict = params.to_dict()
        return self.unified_order(**params_dict)

    def query_order(self, order_no: str, transaction_id: Optional[str] = None) -> ResponseData:
        """查询订单"""
        return self.order_query(out_trade_no=order_no, transaction_id=transaction_id)

    def close_order(self, order_no: str) -> ResponseData:
        """关闭订单"""
        return self.close_order(out_trade_no=order_no)

    def refund(
        self,
        order_no: str,
        refund_amount: float,
        refund_no: Optional[str] = None,
        **kwargs
    ) -> ResponseData:
        """申请退款"""
        # 微信金额单位是分,需要转换
        total_fee = int(refund_amount * 100)
        refund_fee = total_fee  # 简化处理,假设全额退款

        return self.refund(
            out_trade_no=order_no,
            out_refund_no=refund_no or self._generate_nonce_str(),
            total_fee=total_fee,
            refund_fee=refund_fee,
            **kwargs
        )

    def query_refund(self, refund_no: str, transaction_id: Optional[str] = None) -> ResponseData:
        """查询退款"""
        return self.refund_query(out_refund_no=refund_no, transaction_id=transaction_id)

    def verify_notify(self, data: Dict[str, Any], signature: str) -> bool:
        """验证异步通知"""
        if not self.config.api_key:
            logger.warning("API密钥未配置,无法验签")
            return False

        return self._verify_response(data, signature)
