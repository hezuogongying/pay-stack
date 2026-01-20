"""
GoPay API服务模块
提供将支付功能封装为HTTP API的能力

遵循SOLID原则:
- 单一职责: 每个路由处理器专注于单一支付操作
- 开闭原则: 通过基类扩展,无需修改现有代码
- 里氏替换: 所有处理器可互换使用
- 接口隔离: 细分的路由接口
- 依赖倒置: 依赖抽象基类而非具体实现
"""

from gopay.api.server import PayApiServer
from gopay.api.handlers import (
    AlipayApiHandler,
    WechatApiHandler,
    ApplePayApiHandler,
    PayPalApiHandler,
    SaobeiApiHandler,
)
from gopay.api.middleware import ErrorHandler, AuthMiddleware
from gopay.api.response import ApiResponse, ApiError

__all__ = [
    "PayApiServer",
    "AlipayApiHandler",
    "WechatApiHandler",
    "ApplePayApiHandler",
    "PayPalApiHandler",
    "SaobeiApiHandler",
    "ErrorHandler",
    "AuthMiddleware",
    "ApiResponse",
    "ApiError",
]
