"""
PayPal API处理器
提供PayPal的HTTP API接口
"""

import logging
from typing import Dict, Any

from gopay.paypal import PayPalClient
from gopay.api.handlers.base import BaseApiHandler
from gopay.api.response import ApiResponse


logger = logging.getLogger(__name__)


class PayPalApiHandler(BaseApiHandler):
    """
    PayPal API处理器

    遵循单一职责原则(SRP): 只处理PayPal相关的API请求
    """

    def __init__(self, client: PayPalClient):
        """
        初始化PayPal API处理器

        Args:
            client: PayPal客户端实例
        """
        super().__init__(client)

    def create_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        创建订单

        Args:
            params: 订单参数
                - intent: 意图 (CAPTURE, AUTHORIZE)
                - purchase_units: 购买单元列表

        Returns:
            ApiResponse: API响应
        """
        def _create():
            intent = params.get("intent", "CAPTURE")
            purchase_units = params.get("purchase_units", [])

            if not purchase_units:
                return ApiResponse.invalid_params("缺少购买单元")

            order_data = {
                "intent": intent,
                "purchase_units": purchase_units
            }

            result = self.client.create_order(order_data)

            if result.code == "0" or result.code == "201":
                return ApiResponse.success(result.data, "订单创建成功")
            else:
                return ApiResponse.error(result.msg or "订单创建失败")

        return self._execute_with_hooks("create_order", _create)

    def query_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        查询订单

        Args:
            params: 查询参数
                - order_id: 订单ID

        Returns:
            ApiResponse: API响应
        """
        def _query():
            order_id = params.get("order_id")
            if not order_id:
                return ApiResponse.invalid_params("缺少订单ID")

            result = self.client.get_order(order_id)

            if result.code == "0" or result.code == "200":
                return ApiResponse.success(result.data, "查询成功")
            else:
                return ApiResponse.error(result.msg or "查询失败")

        return self._execute_with_hooks("query_order", _query)

    def close_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        PayPal不支持关闭订单

        Args:
            params: 订单参数

        Returns:
            ApiResponse: API响应
        """
        return ApiResponse.not_found("PayPal不支持此操作")

    def refund(self, params: Dict[str, Any]) -> ApiResponse:
        """
        申请退款

        Args:
            params: 退款参数
                - amount: 金额
                - currency_code: 货币代码

        Returns:
            ApiResponse: API响应
        """
        def _refund():
            amount = params.get("amount")
            currency_code = params.get("currency_code", "USD")

            if not amount:
                return ApiResponse.invalid_params("缺少退款金额")

            refund_data = {
                "amount": {
                    "value": str(amount),
                    "currency_code": currency_code
                }
            }

            result = self.client.refund_payment(refund_data)

            if result.code == "0" or result.code == "201":
                return ApiResponse.success(result.data, "退款申请成功")
            else:
                return ApiResponse.error(result.msg or "退款申请失败")

        return self._execute_with_hooks("refund", _refund)

    def query_refund(self, params: Dict[str, Any]) -> ApiResponse:
        """
        查询退款

        Args:
            params: 查询参数
                - refund_id: 退款ID

        Returns:
            ApiResponse: API响应
        """
        def _query_refund():
            refund_id = params.get("refund_id")
            if not refund_id:
                return ApiResponse.invalid_params("缺少退款ID")

            result = self.client.get_refund(refund_id)

            if result.code == "0" or result.code == "200":
                return ApiResponse.success(result.data, "退款查询成功")
            else:
                return ApiResponse.error(result.msg or "退款查询失败")

        return self._execute_with_hooks("query_refund", _query_refund)

    def capture_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        捕获订单支付

        Args:
            params: 捕获参数
                - order_id: 订单ID

        Returns:
            ApiResponse: API响应
        """
        def _capture():
            order_id = params.get("order_id")
            if not order_id:
                return ApiResponse.invalid_params("缺少订单ID")

            result = self.client.capture_order(order_id)

            if result.code == "0" or result.code == "201":
                return ApiResponse.success(result.data, "支付捕获成功")
            else:
                return ApiResponse.error(result.msg or "支付捕获失败")

        return self._execute_with_hooks("capture_order", _capture)

    def create_subscription(self, params: Dict[str, Any]) -> ApiResponse:
        """
        创建订阅

        Args:
            params: 订阅参数
                - plan_id: 计划ID

        Returns:
            ApiResponse: API响应
        """
        def _create():
            plan_id = params.get("plan_id")
            if not plan_id:
                return ApiResponse.invalid_params("缺少计划ID")

            subscription_data = {"plan_id": plan_id}
            result = self.client.create_subscription(subscription_data)

            if result.code == "0" or result.code == "201":
                return ApiResponse.success(result.data, "订阅创建成功")
            else:
                return ApiResponse.error(result.msg or "订阅创建失败")

        return self._execute_with_hooks("create_subscription", _create)
