"""
Apple Pay API处理器
提供Apple Pay的HTTP API接口
"""

import logging
from typing import Dict, Any

from gopay.apple import ApplePayClient
from gopay.api.handlers.base import BaseApiHandler
from gopay.api.response import ApiResponse


logger = logging.getLogger(__name__)


class ApplePayApiHandler(BaseApiHandler):
    """
    Apple Pay API处理器

    遵循单一职责原则(SRP): 只处理Apple Pay相关的API请求
    """

    def __init__(self, client: ApplePayClient):
        """
        初始化Apple Pay API处理器

        Args:
            client: Apple Pay客户端实例
        """
        super().__init__(client)

    def create_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        Apple Pay不直接创建订单,返回不支持

        Args:
            params: 订单参数

        Returns:
            ApiResponse: API响应
        """
        return ApiResponse.not_found("Apple Pay不支持此操作,请使用verify_receipt验证收据")

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

            result = self.client.look_up_order_id(order_id)

            if result.code == "0":
                return ApiResponse.success(result.data, "查询成功")
            else:
                return ApiResponse.error(result.msg or "查询失败")

        return self._execute_with_hooks("query_order", _query)

    def close_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        Apple Pay不支持关闭订单

        Args:
            params: 订单参数

        Returns:
            ApiResponse: API响应
        """
        return ApiResponse.not_found("Apple Pay不支持此操作")

    def refund(self, params: Dict[str, Any]) -> ApiResponse:
        """
        Apple Pay不支持直接退款,需通过App Store Connect

        Args:
            params: 退款参数

        Returns:
            ApiResponse: API响应
        """
        return ApiResponse.not_found("Apple Pay不支持此操作,请在App Store Connect中处理退款")

    def query_refund(self, params: Dict[str, Any]) -> ApiResponse:
        """
        查询退款历史

        Args:
            params: 查询参数

        Returns:
            ApiResponse: API响应
        """
        def _query_refund():
            result = self.client.get_refund_history(params)

            if result.code == "0":
                return ApiResponse.success(result.data, "退款查询成功")
            else:
                return ApiResponse.error(result.msg or "退款查询失败")

        return self._execute_with_hooks("query_refund", _query_refund)

    def verify_receipt(self, params: Dict[str, Any]) -> ApiResponse:
        """
        验证收据

        Args:
            params: 验证参数
                - receipt_data: 收据数据(Base64编码)
                - password: App共享密钥(可选)
                - exclude_old_transactions: 是否排除旧交易(可选)

        Returns:
            ApiResponse: API响应
        """
        def _verify():
            receipt_data = params.get("receipt_data")
            if not receipt_data:
                return ApiResponse.invalid_params("缺少收据数据")

            password = params.get("password")
            exclude_old_transactions = params.get("exclude_old_transactions", False)

            result = self.client.verify_receipt(
                receipt_data=receipt_data,
                password=password,
                exclude_old_transactions=exclude_old_transactions
            )

            if result.code == "0":
                return ApiResponse.success(result.data, "收据验证成功")
            else:
                return ApiResponse.error(result.msg or "收据验证失败")

        return self._execute_with_hooks("verify_receipt", _verify)

    def get_subscription_status(self, params: Dict[str, Any]) -> ApiResponse:
        """
        获取订阅状态

        Args:
            params: 查询参数
                - order_id: 订单ID

        Returns:
            ApiResponse: API响应
        """
        def _get_status():
            order_id = params.get("order_id")
            if not order_id:
                return ApiResponse.invalid_params("缺少订单ID")

            result = self.client.get_all_subscription_statuses(order_id)

            if result.code == "0":
                return ApiResponse.success(result.data, "查询成功")
            else:
                return ApiResponse.error(result.msg or "查询失败")

        return self._execute_with_hooks("get_subscription_status", _get_status)

    def get_transaction_history(self, params: Dict[str, Any]) -> ApiResponse:
        """
        获取交易历史

        Args:
            params: 查询参数
                - start_date: 开始日期
                - end_date: 结束日期
                - product_id: 产品ID(可选)

        Returns:
            ApiResponse: API响应
        """
        def _get_history():
            result = self.client.get_transaction_history_v2(params)

            if result.code == "0":
                return ApiResponse.success(result.data, "查询成功")
            else:
                return ApiResponse.error(result.msg or "查询失败")

        return self._execute_with_hooks("get_transaction_history", _get_history)
