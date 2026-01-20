"""
通联支付客户端
遵循单一职责原则 - 专门负责通联支付
"""

import logging
import random
import string
from typing import Optional, Dict, Any

from gopay.client import PaymentClient
from gopay.config import PaymentConfig
from gopay.http import HttpClient
from gopay.utils.datastructure import BodyMap, XmlMap, ResponseData
from gopay.utils.signer import SignerFactory
from gopay.exceptions import PaymentError, SignError


logger = logging.getLogger(__name__)


class AllinPayConfig(PaymentConfig):
    """
    通联支付配置
    遵循开闭原则 - 继承基类扩展通联特有配置
    """

    # 通联支付网关
    gateway_url: str = "https://vsp.allinpay.com/apiweb/unittrade"

    # 签名类型
    sign_type: str = "MD5"

    # 版本号
    version: str = "v1.0"

    # 字符集
    charset: str = "UTF-8"

    # 商户号
    merchant_id: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()


class AllinPayClient(PaymentClient):
    """
    通联支付客户端
    支持通联支付的各种支付方式
    """

    def __init__(self, config: AllinPayConfig):
        """
        初始化通联支付客户端
        :param config: 通联支付配置
        """
        if not isinstance(config, AllinPayConfig):
            raise ValueError("配置必须是 AllinPayConfig 类型")

        super().__init__(config)
        self.config: AllinPayConfig = config

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
            raise SignError("API密钥未配置", "ALLINPAY")

        # 过滤空值和sign字段
        filtered_params = {k: v for k, v in params.items() if v not in [None, ""] and k != "sign"}
        # 按key排序
        sorted_params = sorted(filtered_params.items())
        # 拼接参数
        param_str = "&".join([f"{k}={v}" for k, v in sorted_params])
        # 添加密钥
        sign_str = f"{param_str}&key={self.config.api_key}"

        # 签名
        return self.signer.sign(sign_str, self.config.api_key)

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
        # 添加密钥
        sign_str = f"{param_str}&key={self.config.api_key}"

        calculated_sign = self.signer.sign(sign_str, self.config.api_key)
        return calculated_sign == sign

    def _build_common_params(self) -> Dict[str, Any]:
        """构建公共参数"""
        return {
            "cusid": self.config.merchant_id or self.config.app_id,
            "appid": self.config.app_id,
            "version": self.config.version,
            "randomstr": self._generate_nonce_str(),
            "charset": self.config.charset,
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

        # 发送请求
        try:
            response = self.http_client.post(
                url,
                data=params,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            if response.status_code != 200:
                return ResponseData.error_response(
                    error=f"HTTP请求失败: {response.status_code}",
                    code=str(response.status_code),
                    raw_response=response.text,
                )

            # 解析响应
            try:
                result = response.json()
            except:
                result = {"response": response.text}

            # 验签
            if "sign" in result:
                if not self._verify_response(result, result["sign"]):
                    logger.warning("响应验签失败")

            # 检查业务状态
            if result.get("returncode") != "SUCCESS":
                return ResponseData.error_response(
                    error=result.get("returnmsg", "请求失败"),
                    code=result.get("returncode"),
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

    def create_order(self, params: BodyMap) -> ResponseData:
        """
        统一下单接口
        :param params: 参数对象
        :return: 下单结果
        """
        params_dict = params.to_dict()

        # 构建请求参数
        request_params = self._build_common_params()
        request_params.update(params_dict)

        if self.config.notify_url:
            request_params["notify_url"] = self.config.notify_url
        if self.config.return_url:
            request_params["back_url"] = self.config.return_url

        url = f"{self.config.gateway_url}/pay"
        return self._do_request(url, request_params)

    def query_order(self, order_no: str, transaction_id: Optional[str] = None) -> ResponseData:
        """
        查询订单接口
        :param order_no: 商户订单号
        :param transaction_id: 通联订单号
        :return: 查询结果
        """
        params = self._build_common_params()
        if order_no:
            params["orderid"] = order_no
        if transaction_id:
            params["transaction_id"] = transaction_id

        url = f"{self.config.gateway_url}/query"
        return self._do_request(url, params)

    def close_order(self, order_no: str) -> ResponseData:
        """
        关闭订单接口
        :param order_no: 商户订单号
        :return: 关闭结果
        """
        params = self._build_common_params()
        params["orderid"] = order_no

        url = f"{self.config.gateway_url}/cancel"
        return self._do_request(url, params)

    # ==================== 退款接口 ====================

    def refund(
        self,
        order_no: str,
        refund_amount: float,
        refund_no: Optional[str] = None,
        **kwargs
    ) -> ResponseData:
        """
        申请退款接口
        :param order_no: 商户订单号
        :param refund_amount: 退款金额
        :param refund_no: 退款单号
        :param kwargs: 其他参数
        :return: 退款结果
        """
        params = self._build_common_params()
        params.update({
            "orderid": order_no,
            "amount": str(refund_amount),
        })

        if refund_no:
            params["refundno"] = refund_no

        params.update(kwargs)

        url = f"{self.config.gateway_url}/refund"
        return self._do_request(url, params)

    def query_refund(self, refund_no: str) -> ResponseData:
        """
        查询退款接口
        :param refund_no: 退款单号
        :return: 查询结果
        """
        params = self._build_common_params()
        params["refundno"] = refund_no

        url = f"{self.config.gateway_url}/queryrefund"
        return self._do_request(url, params)

    # ==================== 通知处理 ====================

    def verify_notify(self, data: Dict[str, Any], signature: str) -> bool:
        """验证异步通知"""
        if not self.config.api_key:
            logger.warning("API密钥未配置,无法验签")
            return False

        return self._verify_response(data, signature)
