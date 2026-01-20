"""
支付宝API处理器
提供支付宝支付的HTTP API接口
"""

import logging
from typing import Dict, Any

from gopay.alipay import AlipayClient
from gopay.api.handlers.base import BaseApiHandler
from gopay.api.response import ApiResponse
from gopay.utils.datastructure import BodyMap


logger = logging.getLogger(__name__)


class AlipayApiHandler(BaseApiHandler):
    """
    支付宝API处理器

    遵循单一职责原则(SRP): 只处理支付宝相关的API请求
    """

    def __init__(self, client: AlipayClient):
        """
        初始化支付宝API处理器

        Args:
            client: 支付宝客户端实例
        """
        super().__init__(client)

    def _convert_params_to_bodymap(self, params: Dict[str, Any]) -> BodyMap:
        """
        将字典参数转换为BodyMap

        Args:
            params: 字典参数

        Returns:
            BodyMap: BodyMap对象
        """
        body_map = BodyMap()
        for key, value in params.items():
            if value is not None:
                body_map.set(key, value)
        return body_map

    def create_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        创建订单

        Args:
            params: 订单参数
                - out_trade_no: 商户订单号
                - total_amount: 订单金额
                - subject: 订单标题
                - buyer_id: 买家ID (可选)

        Returns:
            ApiResponse: API响应
        """
        def _create():
            body_map = self._convert_params_to_bodymap(params)
            result = self.client.trade_create(body_map)

            if result.success:
                return ApiResponse.success(result.data, "订单创建成功")
            else:
                return ApiResponse.error(result.error or "订单创建失败")

        return self._execute_with_hooks("create_order", _create)

    def query_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        查询订单

        Args:
            params: 查询参数
                - out_trade_no: 商户订单号

        Returns:
            ApiResponse: API响应
        """
        def _query():
            out_trade_no = params.get("out_trade_no")
            if not out_trade_no:
                return ApiResponse.invalid_params("缺少订单号")

            result = self.client.query_order(order_no=out_trade_no)

            if result.success:
                return ApiResponse.success(result.data, "查询成功")
            else:
                return ApiResponse.error(result.error or "查询失败")

        return self._execute_with_hooks("query_order", _query)

    def close_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        关闭订单

        Args:
            params: 订单参数
                - out_trade_no: 商户订单号

        Returns:
            ApiResponse: API响应
        """
        def _close():
            out_trade_no = params.get("out_trade_no")
            if not out_trade_no:
                return ApiResponse.invalid_params("缺少订单号")

            result = self.client.close_order(out_trade_no)

            if result.success:
                return ApiResponse.success(result.data, "订单关闭成功")
            else:
                return ApiResponse.error(result.error or "订单关闭失败")

        return self._execute_with_hooks("close_order", _close)

    def refund(self, params: Dict[str, Any]) -> ApiResponse:
        """
        申请退款

        Args:
            params: 退款参数
                - out_trade_no: 商户订单号
                - refund_amount: 退款金额
                - refund_no: 退款单号

        Returns:
            ApiResponse: API响应
        """
        def _refund():
            out_trade_no = params.get("out_trade_no")
            refund_amount = params.get("refund_amount")
            refund_no = params.get("refund_no")

            if not all([out_trade_no, refund_amount, refund_no]):
                return ApiResponse.invalid_params("缺少必要参数")

            result = self.client.refund(
                order_no=out_trade_no,
                refund_amount=float(refund_amount),
                refund_no=refund_no,
            )

            if result.success:
                return ApiResponse.success(result.data, "退款申请成功")
            else:
                return ApiResponse.error(result.error or "退款申请失败")

        return self._execute_with_hooks("refund", _refund)

    def query_refund(self, params: Dict[str, Any]) -> ApiResponse:
        """
        查询退款

        Args:
            params: 查询参数
                - out_trade_no: 商户订单号
                - refund_no: 退款单号

        Returns:
            ApiResponse: API响应
        """
        def _query_refund():
            out_trade_no = params.get("out_trade_no")
            refund_no = params.get("refund_no")

            if not all([out_trade_no, refund_no]):
                return ApiResponse.invalid_params("缺少必要参数")

            result = self.client.query_refund(
                order_no=out_trade_no,
                refund_no=refund_no,
            )

            if result.success:
                return ApiResponse.success(result.data, "退款查询成功")
            else:
                return ApiResponse.error(result.error or "退款查询失败")

        return self._execute_with_hooks("query_refund", _query_refund)

    def cancel_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        撤销订单

        Args:
            params: 订单参数
                - out_trade_no: 商户订单号

        Returns:
            ApiResponse: API响应
        """
        def _cancel():
            out_trade_no = params.get("out_trade_no")
            if not out_trade_no:
                return ApiResponse.invalid_params("缺少订单号")

            result = self.client.trade_cancel(out_trade_no)

            if result.success:
                return ApiResponse.success(result.data, "订单撤销成功")
            else:
                return ApiResponse.error(result.error or "订单撤销失败")

        return self._execute_with_hooks("cancel_order", _cancel)

    def page_pay(self, params: Dict[str, Any]) -> ApiResponse:
        """
        PC网站支付

        Args:
            params: 支付参数
                - out_trade_no: 商户订单号
                - total_amount: 订单金额
                - subject: 订单标题
                - return_url: 同步返回地址

        Returns:
            ApiResponse: API响应,包含支付URL
        """
        def _page_pay():
            body_map = self._convert_params_to_bodymap(params)
            result = self.client.trade_page_pay(body_map)

            if result.success:
                return ApiResponse.success(result.data, "支付链接生成成功")
            else:
                return ApiResponse.error(result.error or "支付链接生成失败")

        return self._execute_with_hooks("page_pay", _page_pay)

    def wap_pay(self, params: Dict[str, Any]) -> ApiResponse:
        """
        手机网站支付

        Args:
            params: 支付参数

        Returns:
            ApiResponse: API响应,包含支付URL
        """
        def _wap_pay():
            body_map = self._convert_params_to_bodymap(params)
            result = self.client.trade_wap_pay(body_map)

            if result.success:
                return ApiResponse.success(result.data, "支付链接生成成功")
            else:
                return ApiResponse.error(result.error or "支付链接生成失败")

        return self._execute_with_hooks("wap_pay", _wap_pay)

    def transfer(self, params: Dict[str, Any]) -> ApiResponse:
        """
        单笔转账

        Args:
            params: 转账参数
                - out_biz_no: 商户转账唯一订单号
                - payee_account: 收款方账户
                - amount: 转账金额
                - payer_show_name: 付款方显示名

        Returns:
            ApiResponse: API响应
        """
        def _transfer():
            body_map = self._convert_params_to_bodymap(params)
            result = self.client.fund_trans_uni_transfer(body_map)

            if result.success:
                return ApiResponse.success(result.data, "转账成功")
            else:
                return ApiResponse.error(result.error or "转账失败")

        return self._execute_with_hooks("transfer", _transfer)
