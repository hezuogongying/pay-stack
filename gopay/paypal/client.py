"""
PayPal支付客户端
支持PayPal支付、订单、订阅等完整功能
"""

import logging
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin

from gopay.config import PaymentConfig
from gopay.utils.datastructure import BodyMap, ResponseData
from gopay.http import HttpClient


logger = logging.getLogger(__name__)


class PayPalConfig(PaymentConfig):
    """PayPal配置"""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        sandbox: bool = True,
        timeout: int = 30,
        **kwargs
    ):
        """
        初始化PayPal配置

        Args:
            client_id: PayPal客户端ID
            client_secret: PayPal客户端密钥
            sandbox: 是否使用沙箱环境(True=沙箱, False=生产环境)
            timeout: 请求超时时间(秒)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.sandbox = sandbox
        self.timeout = timeout

        # 设置网关URL
        if sandbox:
            self.gateway_url = "https://api-m.sandbox.paypal.com"
        else:
            self.gateway_url = "https://api-m.paypal.com"

        super().__init__(gateway_url=self.gateway_url, **kwargs)

    def validate(self):
        """验证配置"""
        if not self.client_id:
            raise ValueError("client_id不能为空")
        if not self.client_secret:
            raise ValueError("client_secret不能为空")


class PayPalClient:
    """PayPal客户端 - 支持支付、订单、订阅等完整功能"""

    def __init__(self, config: PayPalConfig):
        """
        初始化PayPal客户端

        Args:
            config: PayPal配置对象
        """
        self.config = config
        self.config.validate()
        self.http_client = HttpClient(
            timeout=config.timeout,
            max_retries=3,
            retry_interval=1
        )
        self._access_token: Optional[str] = None

    def _get_access_token(self) -> str:
        """
        获取访问令牌

        Returns:
            str: 访问令牌
        """
        if self._access_token:
            return self._access_token

        url = urljoin(self.config.gateway_url, "/v1/oauth2/token")

        try:
            response = self.http_client.post(
                url=url,
                data={"grant_type": "client_credentials"},
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                    "Accept-Language": "en_US"
                },
                auth=(self.config.client_id, self.config.client_secret)
            )

            self._access_token = response.get("access_token")
            return self._access_token

        except Exception as e:
            logger.error(f"获取PayPal访问令牌失败: {str(e)}")
            raise

    def _do_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> ResponseData:
        """
        执行HTTP请求

        Args:
            method: HTTP方法(GET, POST, PUT, PATCH, DELETE)
            endpoint: API端点
            data: 请求体数据
            params: URL查询参数

        Returns:
            ResponseData: 响应数据
        """
        url = urljoin(self.config.gateway_url, endpoint)
        access_token = self._get_access_token()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        try:
            if method == "GET":
                response = self.http_client.get(url=url, params=params, headers=headers)
            elif method == "POST":
                response = self.http_client.post(url=url, json=data, headers=headers)
            elif method == "PUT":
                response = self.http_client.put(url=url, json=data, headers=headers)
            elif method == "PATCH":
                response = self.http_client.patch(url=url, json=data, headers=headers)
            elif method == "DELETE":
                response = self.http_client.delete(url=url, headers=headers)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")

            return ResponseData(
                code=str(response.get("status", "0")),
                msg=response.get("error", "Success"),
                data=response
            )

        except Exception as e:
            logger.error(f"PayPal请求失败: {str(e)}")
            return ResponseData(
                code="-1",
                msg=str(e),
                data={}
            )

    # ==================== 支付相关 API ====================

    def create_payment(self, payment_data: Dict[str, Any]) -> ResponseData:
        """
        创建支付(已废弃,使用create_order)

        Args:
            payment_data: 支付数据

        Returns:
            ResponseData: 支付创建结果
        """
        return self._do_request("POST", "/v1/payments/payment", payment_data)

    def payment_authorize(self, payment_id: str, data: Dict[str, Any]) -> ResponseData:
        """
        授权支付

        Args:
            payment_id: 支付ID
            data: 授权数据

        Returns:
            ResponseData: 授权结果
        """
        return self._do_request("POST", f"/v1/payments/payment/{payment_id}/authorize", data)

    def payment_capture(self, authorization_id: str, data: Dict[str, Any]) -> ResponseData:
        """
        捕获支付

        Args:
            authorization_id: 授权ID
            data: 捕获数据,包括amount等

        Returns:
            ResponseData: 捕获结果
        """
        return self._do_request("POST", f"/v1/payments/authorization/{authorization_id}/capture", data)

    def payment_execute(self, payment_id: str, payer_id: str) -> ResponseData:
        """
        执行支付

        Args:
            payment_id: 支付ID
            payer_id: 支付者ID

        Returns:
            ResponseData: 执行结果
        """
        return self._do_request("POST", f"/v1/payments/payment/{payment_id}/execute", {
            "payer_id": payer_id
        })

    def get_payment(self, payment_id: str) -> ResponseData:
        """
        获取支付详情

        Args:
            payment_id: 支付ID

        Returns:
            ResponseData: 支付详情
        """
        return self._do_request("GET", f"/v1/payments/payment/{payment_id}")

    def list_payments(self, params: Optional[Dict[str, Any]] = None) -> ResponseData:
        """
        列出支付

        Args:
            params: 查询参数

        Returns:
            ResponseData: 支付列表
        """
        return self._do_request("GET", "/v1/payments/payment", params=params)

    # ==================== 订单相关 API ====================

    def create_order(self, order_data: Dict[str, Any]) -> ResponseData:
        """
        创建订单

        Args:
            order_data: 订单数据

        Returns:
            ResponseData: 订单创建结果
        """
        return self._do_request("POST", "/v2/checkout/orders", order_data)

    def get_order(self, order_id: str) -> ResponseData:
        """
        获取订单详情

        Args:
            order_id: 订单ID

        Returns:
            ResponseData: 订单详情
        """
        return self._do_request("GET", f"/v2/checkout/orders/{order_id}")

    def update_order(self, order_id: str, data: List[Dict[str, Any]]) -> ResponseData:
        """
        更新订单

        Args:
            order_id: 订单ID
            data: 更新数据

        Returns:
            ResponseData: 更新结果
        """
        return self._do_request("PATCH", f"/v2/checkout/orders/{order_id}", data)

    def authorize_order(self, order_id: str, data: Dict[str, Any]) -> ResponseData:
        """
        授权订单

        Args:
            order_id: 订单ID
            data: 授权数据

        Returns:
            ResponseData: 授权结果
        """
        return self._do_request("POST", f"/v2/checkout/orders/{order_id}/authorize", data)

    def capture_order(self, order_id: str, data: Optional[Dict[str, Any]] = None) -> ResponseData:
        """
        捕获订单

        Args:
            order_id: 订单ID
            data: 捕获数据(可选)

        Returns:
            ResponseData: 捕获结果
        """
        return self._do_request("POST", f"/v2/checkout/orders/{order_id}/capture", data)

    # ==================== 订阅相关 API ====================

    def create_subscription(self, subscription_data: Dict[str, Any]) -> ResponseData:
        """
        创建订阅

        Args:
            subscription_data: 订阅数据

        Returns:
            ResponseData: 订阅创建结果
        """
        return self._do_request("POST", "/v1/billing/subscriptions", subscription_data)

    def get_subscription(self, subscription_id: str) -> ResponseData:
        """
        获取订阅详情

        Args:
            subscription_id: 订阅ID

        Returns:
            ResponseData: 订阅详情
        """
        return self._do_request("GET", f"/v1/billing/subscriptions/{subscription_id}")

    def update_subscription(
        self,
        subscription_id: str,
        data: Dict[str, Any]
    ) -> ResponseData:
        """
        更新订阅

        Args:
            subscription_id: 订阅ID
            data: 更新数据

        Returns:
            ResponseData: 更新结果
        """
        return self._do_request("PATCH", f"/v1/billing/subscriptions/{subscription_id}", data)

    def cancel_subscription(
        self,
        subscription_id: str,
        reason: str
    ) -> ResponseData:
        """
        取消订阅

        Args:
            subscription_id: 订阅ID
            reason: 取消原因

        Returns:
            ResponseData: 取消结果
        """
        return self._do_request("POST", f"/v1/billing/subscriptions/{subscription_id}/cancel", {
            "reason": reason
        })

    def activate_subscription(
        self,
        subscription_id: str
    ) -> ResponseData:
        """
        激活订阅

        Args:
            subscription_id: 订阅ID

        Returns:
            ResponseData: 激活结果
        """
        return self._do_request("POST", f"/v1/billing/subscriptions/{subscription_id}/activate")

    def suspend_subscription(
        self,
        subscription_id: str,
        reason: str
    ) -> ResponseData:
        """
        暂停订阅

        Args:
            subscription_id: 订阅ID
            reason: 暂停原因

        Returns:
            ResponseData: 暂停结果
        """
        return self._do_request("POST", f"/v1/billing/subscriptions/{subscription_id}/suspend", {
            "reason": reason
        })

    def capture_subscription_payment(
        self,
        subscription_id: str,
        data: Dict[str, Any]
    ) -> ResponseData:
        """
        捕获订阅支付

        Args:
            subscription_id: 订阅ID
            data: 支付数据

        Returns:
            ResponseData: 捕获结果
        """
        return self._do_request("POST", f"/v1/billing/subscriptions/{subscription_id}/capture", data)

    def revise_subscription(
        self,
        subscription_id: str,
        data: Dict[str, Any]
    ) -> ResponseData:
        """
        修订订阅

        Args:
            subscription_id: 订阅ID
            data: 修订数据

        Returns:
            ResponseData: 修订结果
        """
        return self._do_request("POST", f"/v1/billing/subscriptions/{subscription_id}/revise", data)

    # ==================== 计划相关 API ====================

    def create_plan(self, plan_data: Dict[str, Any]) -> ResponseData:
        """
        创建计费计划

        Args:
            plan_data: 计划数据

        Returns:
            ResponseData: 计划创建结果
        """
        return self._do_request("POST", "/v1/billing/plans", plan_data)

    def get_plan(self, plan_id: str) -> ResponseData:
        """
        获取计费计划详情

        Args:
            plan_id: 计划ID

        Returns:
            ResponseData: 计划详情
        """
        return self._do_request("GET", f"/v1/billing/plans/{plan_id}")

    def list_plans(self, params: Optional[Dict[str, Any]] = None) -> ResponseData:
        """
        列出计费计划

        Args:
            params: 查询参数

        Returns:
            ResponseData: 计划列表
        """
        return self._do_request("GET", "/v1/billing/plans", params=params)

    def update_plan(
        self,
        plan_id: str,
        data: Dict[str, Any]
    ) -> ResponseData:
        """
        更新计费计划

        Args:
            plan_id: 计划ID
            data: 更新数据

        Returns:
            ResponseData: 更新结果
        """
        return self._do_request("PATCH", f"/v1/billing/plans/{plan_id}", data)

    def activate_plan(self, plan_id: str) -> ResponseData:
        """
        激活计费计划

        Args:
            plan_id: 计划ID

        Returns:
            ResponseData: 激活结果
        """
        return self._do_request("POST", f"/v1/billing/plans/{plan_id}/activate")

    def deactivate_plan(self, plan_id: str) -> ResponseData:
        """
        停用计费计划

        Args:
            plan_id: 计划ID

        Returns:
            ResponseData: 停用结果
        """
        return self._do_request("POST", f"/v1/billing/plans/{plan_id}/deactivate")

    # ==================== 退款相关 API ====================

    def refund_payment(self, data: Dict[str, Any]) -> ResponseData:
        """
        退款

        Args:
            data: 退款数据

        Returns:
            ResponseData: 退款结果
        """
        return self._do_request("POST", "/v1/payments/sale/{sale_id}/refund", data)

    def get_refund(self, refund_id: str) -> ResponseData:
        """
        获取退款详情

        Args:
            refund_id: 退款ID

        Returns:
            ResponseData: 退款详情
        """
        return self._do_request("GET", f"/v1/payments/refund/{refund_id}")

    def list_refunds(self, params: Optional[Dict[str, Any]] = None) -> ResponseData:
        """
        列出退款

        Args:
            params: 查询参数

        Returns:
            ResponseData: 退款列表
        """
        return self._do_request("GET", "/v1/payments/refund", params=params)
