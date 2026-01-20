"""
聚合支付API处理器
统一处理多种支付渠道的API请求

遵循SOLID原则:
- 单一职责(SRP): 专注于聚合支付的路由和分发
- 开闭原则(OCP): 可扩展新的支付渠道
- 里氏替换(LSP): 可替换为其他聚合实现
- 接口隔离(ISP): 提供最小必要接口
- 依赖倒置(DIP): 依赖抽象的BaseApiHandler
"""

import logging
from typing import Dict, Any, Optional, Type
from enum import Enum

from gopay.api.handlers.base import BaseApiHandler
from gopay.api.response import ApiResponse, ResponseCode


logger = logging.getLogger(__name__)


class PaymentChannel(str, Enum):
    """支付渠道枚举"""
    ALIPAY = "alipay"
    WECHAT = "wechat"
    APPLE_PAY = "apple_pay"
    PAYPAL = "paypal"
    SAOBEI = "saobei"
    QQ = "qq"
    ALLINPAY = "allinpay"
    LAKALA = "lakala"


class AggregatedPayHandler:
    """
    聚合支付处理器

    遵循单一职责原则(SRP): 负责路由和分发支付请求到对应的支付渠道
    """

    def __init__(self):
        """初始化聚合支付处理器"""
        self._handlers: Dict[str, BaseApiHandler] = {}

    def register_handler(
        self,
        channel: str,
        handler: BaseApiHandler
    ):
        """
        注册支付渠道处理器

        Args:
            channel: 支付渠道标识
            handler: API处理器实例
        """
        self._handlers[channel] = handler
        logger.info(f"注册支付渠道: {channel}")

    def get_handler(self, channel: str) -> Optional[BaseApiHandler]:
        """
        获取支付渠道处理器

        Args:
            channel: 支付渠道标识

        Returns:
            Optional[BaseApiHandler]: 处理器实例,如果不存在返回None
        """
        return self._handlers.get(channel)

    def create_order(
        self,
        channel: str,
        params: Dict[str, Any]
    ) -> ApiResponse:
        """
        创建订单 (聚合接口)

        Args:
            channel: 支付渠道
            params: 订单参数

        Returns:
            ApiResponse: API响应
        """
        handler = self.get_handler(channel)
        if not handler:
            return ApiResponse.error(f"不支持的支付渠道: {channel}")

        return handler.create_order(params)

    def query_order(
        self,
        channel: str,
        params: Dict[str, Any]
    ) -> ApiResponse:
        """
        查询订单 (聚合接口)

        Args:
            channel: 支付渠道
            params: 查询参数

        Returns:
            ApiResponse: API响应
        """
        handler = self.get_handler(channel)
        if not handler:
            return ApiResponse.error(f"不支持的支付渠道: {channel}")

        return handler.query_order(params)

    def close_order(
        self,
        channel: str,
        params: Dict[str, Any]
    ) -> ApiResponse:
        """
        关闭订单 (聚合接口)

        Args:
            channel: 支付渠道
            params: 订单参数

        Returns:
            ApiResponse: API响应
        """
        handler = self.get_handler(channel)
        if not handler:
            return ApiResponse.error(f"不支持的支付渠道: {channel}")

        return handler.close_order(params)

    def refund(
        self,
        channel: str,
        params: Dict[str, Any]
    ) -> ApiResponse:
        """
        申请退款 (聚合接口)

        Args:
            channel: 支付渠道
            params: 退款参数

        Returns:
            ApiResponse: API响应
        """
        handler = self.get_handler(channel)
        if not handler:
            return ApiResponse.error(f"不支持的支付渠道: {channel}")

        return handler.refund(params)

    def query_refund(
        self,
        channel: str,
        params: Dict[str, Any]
    ) -> ApiResponse:
        """
        查询退款 (聚合接口)

        Args:
            channel: 支付渠道
            params: 查询参数

        Returns:
            ApiResponse: API响应
        """
        handler = self.get_handler(channel)
        if not handler:
            return ApiResponse.error(f"不支持的支付渠道: {channel}")

        return handler.query_refund(params)

    def cancel_order(
        self,
        channel: str,
        params: Dict[str, Any]
    ) -> ApiResponse:
        """
        撤销订单 (聚合接口)

        Args:
            channel: 支付渠道
            params: 订单参数

        Returns:
            ApiResponse: API响应
        """
        handler = self.get_handler(channel)
        if not handler:
            return ApiResponse.error(f"不支持的支付渠道: {channel}")

        return handler.cancel_order(params)

    def supported_channels(self) -> list:
        """
        获取支持的支付渠道列表

        Returns:
            list: 支付渠道标识列表
        """
        return list(self._handlers.keys())

    def is_supported(self, channel: str) -> bool:
        """
        检查支付渠道是否支持

        Args:
            channel: 支付渠道标识

        Returns:
            bool: 是否支持
        """
        return channel in self._handlers
