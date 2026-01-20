"""
扫呗支付API处理器
提供扫呗支付的HTTP API接口
"""

import logging
from typing import Dict, Any

from gopay.saobei import SaobeiClient
from gopay.api.handlers.base import BaseApiHandler
from gopay.api.response import ApiResponse
from gopay.utils.datastructure import BodyMap


logger = logging.getLogger(__name__)


class SaobeiApiHandler(BaseApiHandler):
    """
    扫呗支付API处理器

    遵循单一职责原则(SRP): 只处理扫呗支付相关的API请求
    """

    def __init__(self, client: SaobeiClient):
        """
        初始化扫呗支付API处理器

        Args:
            client: 扫呗支付客户端实例
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
                body_map.put(key, value)
        return body_map

    def create_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        创建订单 (小程序支付)

        Args:
            params: 订单参数
                - out_trade_no: 商户订单号
                - total_fee: 支付金额
                - body: 商品描述
                - openid: 用户标识
                - type: 支付类型 (wxpay/alipay)

        Returns:
            ApiResponse: API响应
        """
        def _create():
            body_map = self._convert_params_to_bodymap(params)
            result = self.client.mini_pay(body_map)

            if result.code == "0":
                return ApiResponse.success(result.data, "订单创建成功")
            else:
                return ApiResponse.error(result.msg or "订单创建失败")

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

            body_map = BodyMap().put("out_trade_no", out_trade_no)
            result = self.client.query(body_map)

            if result.code == "0":
                return ApiResponse.success(result.data, "查询成功")
            else:
                return ApiResponse.error(result.msg or "查询失败")

        return self._execute_with_hooks("query_order", _query)

    def close_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        关闭订单

        Args:
            params: 订单参数
                - out_trade_no: 商户订单号
                - type: 支付类型

        Returns:
            ApiResponse: API响应
        """
        def _close():
            body_map = self._convert_params_to_bodymap(params)
            result = self.client.close_order(body_map)

            if result.code == "0":
                return ApiResponse.success(result.data, "订单关闭成功")
            else:
                return ApiResponse.error(result.msg or "订单关闭失败")

        return self._execute_with_hooks("close_order", _close)

    def refund(self, params: Dict[str, Any]) -> ApiResponse:
        """
        申请退款

        Args:
            params: 退款参数
                - out_trade_no: 商户订单号
                - out_refund_no: 退款单号
                - refund_fee: 退款金额
                - total_fee: 总金额
                - type: 支付类型

        Returns:
            ApiResponse: API响应
        """
        def _refund():
            body_map = self._convert_params_to_bodymap(params)
            result = self.client.refund(body_map)

            if result.code == "0":
                return ApiResponse.success(result.data, "退款申请成功")
            else:
                return ApiResponse.error(result.msg or "退款申请失败")

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

            body_map = BodyMap().put("out_refund_no", out_refund_no)
            result = self.client.query_refund(body_map)

            if result.code == "0":
                return ApiResponse.success(result.data, "退款查询成功")
            else:
                return ApiResponse.error(result.msg or "退款查询失败")

        return self._execute_with_hooks("query_refund", _query_refund)

    def cancel_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        撤销订单

        Args:
            params: 订单参数
                - out_trade_no: 商户订单号
                - type: 支付类型

        Returns:
            ApiResponse: API响应
        """
        def _cancel():
            body_map = self._convert_params_to_bodymap(params)
            result = self.client.cancel_order(body_map)

            if result.code == "0":
                return ApiResponse.success(result.data, "订单撤销成功")
            else:
                return ApiResponse.error(result.msg or "订单撤销失败")

        return self._execute_with_hooks("cancel_order", _cancel)

    def barcode_pay(self, params: Dict[str, Any]) -> ApiResponse:
        """
        付款码支付

        Args:
            params: 支付参数
                - out_trade_no: 商户订单号
                - total_fee: 支付金额
                - body: 商品描述
                - auth_code: 支付授权码
                - type: 支付类型

        Returns:
            ApiResponse: API响应
        """
        def _barcode_pay():
            body_map = self._convert_params_to_bodymap(params)
            result = self.client.barcode_pay(body_map)

            if result.code == "0":
                return ApiResponse.success(result.data, "支付成功")
            else:
                return ApiResponse.error(result.msg or "支付失败")

        return self._execute_with_hooks("barcode_pay", _barcode_pay)

    def get_qrcode(self, params: Dict[str, Any]) -> ApiResponse:
        """
        获取支付二维码

        Args:
            params: 二维码参数
                - out_trade_no: 商户订单号
                - total_fee: 支付金额
                - body: 商品描述
                - type: 支付类型

        Returns:
            ApiResponse: API响应
        """
        def _get_qrcode():
            body_map = self._convert_params_to_bodymap(params)
            result = self.client.get_pay_qrcode(body_map)

            if result.code == "0":
                return ApiResponse.success(result.data, "二维码生成成功")
            else:
                return ApiResponse.error(result.msg or "二维码生成失败")

        return self._execute_with_hooks("get_qrcode", _get_qrcode)
