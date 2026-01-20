"""
微信支付API处理器
提供微信支付的HTTP API接口
"""

import logging
from typing import Dict, Any

from gopay.wechat import WechatClient
from gopay.api.handlers.base import BaseApiHandler
from gopay.api.response import ApiResponse


logger = logging.getLogger(__name__)


class WechatApiHandler(BaseApiHandler):
    """
    微信支付API处理器

    遵循单一职责原则(SRP): 只处理微信支付相关的API请求
    """

    def __init__(self, client: WechatClient):
        """
        初始化微信支付API处理器

        Args:
            client: 微信支付客户端实例
        """
        super().__init__(client)

    def create_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        创建订单 (统一下单)

        Args:
            params: 订单参数
                - body: 商品描述
                - out_trade_no: 商户订单号
                - total_fee: 订单金额(分)
                - spbill_create_ip: 终端IP
                - trade_type: 交易类型 (JSAPI, NATIVE, APP等)
                - openid: 用户标识 (JSAPI时需要)

        Returns:
            ApiResponse: API响应
        """
        def _create():
            body = params.get("body")
            out_trade_no = params.get("out_trade_no")
            total_fee = params.get("total_fee")
            spbill_create_ip = params.get("spbill_create_ip", "127.0.0.1")
            trade_type = params.get("trade_type", "NATIVE")
            openid = params.get("openid")

            if not all([body, out_trade_no, total_fee]):
                return ApiResponse.invalid_params("缺少必要参数")

            if trade_type == "JSAPI" and not openid:
                return ApiResponse.invalid_params("JSAPI支付需要openid")

            result = self.client.unified_order(
                body=body,
                out_trade_no=out_trade_no,
                total_fee=int(total_fee),
                spbill_create_ip=spbill_create_ip,
                trade_type=trade_type,
                openid=openid,
            )

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
                - out_refund_no: 退款单号
                - total_fee: 订单金额
                - refund_fee: 退款金额

        Returns:
            ApiResponse: API响应
        """
        def _refund():
            out_trade_no = params.get("out_trade_no")
            out_refund_no = params.get("out_refund_no")
            total_fee = params.get("total_fee")
            refund_fee = params.get("refund_fee")

            if not all([out_trade_no, out_refund_no, total_fee, refund_fee]):
                return ApiResponse.invalid_params("缺少必要参数")

            result = self.client.refund(
                out_trade_no=out_trade_no,
                out_refund_no=out_refund_no,
                total_fee=int(total_fee),
                refund_fee=int(refund_fee),
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
                - out_refund_no: 退款单号

        Returns:
            ApiResponse: API响应
        """
        def _query_refund():
            out_refund_no = params.get("out_refund_no")
            if not out_refund_no:
                return ApiResponse.invalid_params("缺少退款单号")

            result = self.client.query_refund(out_refund_no=out_refund_no)

            if result.success:
                return ApiResponse.success(result.data, "退款查询成功")
            else:
                return ApiResponse.error(result.error or "退款查询失败")

        return self._execute_with_hooks("query_refund", _query_refund)

    def create_refund(self, params: Dict[str, Any]) -> ApiResponse:
        """
        发起退款 (别名方法)

        Args:
            params: 退款参数

        Returns:
            ApiResponse: API响应
        """
        return self.refund(params)
