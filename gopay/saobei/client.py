"""
扫呗支付客户端
支持微信、支付宝扫码支付等
"""

import logging
from typing import Optional, Dict, Any

from gopay.config import PaymentConfig
from gopay.utils.datastructure import BodyMap, ResponseData
from gopay.http import HttpClient
from gopay.utils.signer import sign_params


logger = logging.getLogger(__name__)


class SaobeiConfig(PaymentConfig):
    """扫呗支付配置"""

    def __init__(
        self,
        merchant_id: str,
        terminal_id: str,
        key: str,
        gateway_url: str = "https://pay.so-pay.cn",
        timeout: int = 30,
        **kwargs
    ):
        """
        初始化扫呗配置

        Args:
            merchant_id: 商户号
            terminal_id: 终端号
            key: 商户密钥
            gateway_url: 网关地址
            timeout: 请求超时时间(秒)
        """
        self.merchant_id = merchant_id
        self.terminal_id = terminal_id
        self.key = key
        self.timeout = timeout

        super().__init__(gateway_url=gateway_url, **kwargs)

    def validate(self):
        """验证配置"""
        if not self.merchant_id:
            raise ValueError("merchant_id不能为空")
        if not self.terminal_id:
            raise ValueError("terminal_id不能为空")
        if not self.key:
            raise ValueError("key不能为空")


class SaobeiClient:
    """扫呗支付客户端"""

    def __init__(self, config: SaobeiConfig):
        """
        初始化扫呗客户端

        Args:
            config: 扫呗配置对象
        """
        self.config = config
        self.config.validate()
        self.http_client = HttpClient(
            timeout=config.timeout,
            max_retries=3,
            retry_interval=1
        )

    def _build_common_params(self) -> Dict[str, Any]:
        """
        构建公共参数

        Returns:
            Dict: 公共参数
        """
        return {
            "merchant_id": self.config.merchant_id,
            "terminal_id": self.config.terminal_id,
        }

    def _do_request(
        self,
        endpoint: str,
        params: Dict[str, Any]
    ) -> ResponseData:
        """
        执行HTTP请求

        Args:
            endpoint: API端点
            params: 请求参数

        Returns:
            ResponseData: 响应数据
        """
        url = f"{self.config.gateway_url}{endpoint}"

        # 添加签名
        signed_params = sign_params(
            params=params,
            sign_type="MD5",
            key=self.config.key
        )

        try:
            response = self.http_client.post(
                url=url,
                json=signed_params,
                headers={"Content-Type": "application/json"}
            )

            return ResponseData(
                code=str(response.get("code", "0")),
                msg=response.get("msg", response.get("message", "Success")),
                data=response
            )

        except Exception as e:
            logger.error(f"扫呗请求失败: {str(e)}")
            return ResponseData(
                code="-1",
                msg=str(e),
                data={}
            )

    def mini_pay(self, params: BodyMap) -> ResponseData:
        """
        小程序支付

        Args:
            params: 支付参数
                - out_trade_no: 商户订单号
                - total_fee: 支付金额
                - body: 商品描述
                - attach: 附加数据
                - openid: 用户标识
                - type: 支付类型(微信/支付宝)

        Returns:
            ResponseData: 支付结果
        """
        params_dict = params.to_dict()
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = "/api/miniPay"
        return self._do_request(url, request_params)

    def barcode_pay(self, params: BodyMap) -> ResponseData:
        """
        付款码支付(刷卡支付)

        Args:
            params: 支付参数
                - out_trade_no: 商户订单号
                - total_fee: 支付金额
                - body: 商品描述
                - auth_code: 支付授权码(付款码)
                - type: 支付类型(微信/支付宝)

        Returns:
            ResponseData: 支付结果
        """
        params_dict = params.to_dict()
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = "/api/barcodePay"
        return self._do_request(url, request_params)

    def query(self, params: BodyMap) -> ResponseData:
        """
        支付查询

        Args:
            params: 查询参数
                - out_trade_no: 商户订单号

        Returns:
            ResponseData: 查询结果
        """
        params_dict = params.to_dict()
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = "/api/query"
        return self._do_request(url, request_params)

    def refund(self, params: BodyMap) -> ResponseData:
        """
        申请退款

        Args:
            params: 退款参数
                - out_trade_no: 商户订单号
                - out_refund_no: 退款单号
                - refund_fee: 退款金额
                - total_fee: 总金额
                - type: 支付类型(微信/支付宝)

        Returns:
            ResponseData: 退款结果
        """
        params_dict = params.to_dict()
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = "/api/refund"
        return self._do_request(url, request_params)

    def query_refund(self, params: BodyMap) -> ResponseData:
        """
        退款查询

        Args:
            params: 查询参数
                - out_refund_no: 退款单号

        Returns:
            ResponseData: 查询结果
        """
        params_dict = params.to_dict()
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = "/api/refundQuery"
        return self._do_request(url, request_params)

    def close_order(self, params: BodyMap) -> ResponseData:
        """
        关闭订单

        Args:
            params: 关闭参数
                - out_trade_no: 商户订单号
                - type: 支付类型(微信/支付宝)

        Returns:
            ResponseData: 关闭结果
        """
        params_dict = params.to_dict()
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = "/api/closeOrder"
        return self._do_request(url, request_params)

    def cancel_order(self, params: BodyMap) -> ResponseData:
        """
        撤销订单

        Args:
            params: 撤销参数
                - out_trade_no: 商户订单号
                - type: 支付类型(微信/支付宝)

        Returns:
            ResponseData: 撤销结果
        """
        params_dict = params.to_dict()
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = "/api/cancelOrder"
        return self._do_request(url, request_params)

    def get_pay_qrcode(self, params: BodyMap) -> ResponseData:
        """
        获取支付二维码

        Args:
            params: 二维码参数
                - out_trade_no: 商户订单号
                - total_fee: 支付金额
                - body: 商品描述
                - type: 支付类型(微信/支付宝)
                - attach: 附加数据

        Returns:
            ResponseData: 二维码数据
        """
        params_dict = params.to_dict()
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = "/api/getPayQrcode"
        return self._do_request(url, request_params)
