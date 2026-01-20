"""
GoPay - Python支付SDK
支持微信、支付宝、QQ、通联支付、拉卡拉、Apple Pay、PayPal、扫呗等多种支付方式

遵循SOLID原则设计:
- 单一职责原则(SRP): 每个模块专注于单一支付渠道
- 开闭原则(OCP): 通过抽象类扩展,无需修改现有代码
- 里氏替换原则(LSP): 所有支付客户端可互换使用
- 接口隔离原则(ISP): 细分接口,避免依赖不需要的方法
- 依赖倒置原则(DIP): 依赖抽象而非具体实现
"""

__version__ = "1.0.0"
__author__ = "GoPay Team"

from gopay.client import PaymentClient
from gopay.config import PaymentConfig
from gopay.exceptions import (
    GoPayError,
    ConfigError,
    SignError,
    PaymentError,
    NetworkError,
)

# 支付渠道
from gopay.alipay import AlipayClient
from gopay.wechat import WechatClient
from gopay.qq import QQClient
from gopay.allinpay import AllinPayClient, AllinPayConfig
from gopay.lakala import LakalaClient, LakalaConfig
from gopay.apple import ApplePayClient, ApplePayConfig
from gopay.paypal import PayPalClient, PayPalConfig
from gopay.saobei import SaobeiClient, SaobeiConfig

# API服务模块
from gopay.api import (
    PayApiServer,
    AlipayApiHandler,
    WechatApiHandler,
    ApplePayApiHandler,
    PayPalApiHandler,
    SaobeiApiHandler,
    ErrorHandler,
    AuthMiddleware,
)

__all__ = [
    # 客户端和配置
    "PaymentClient",
    "PaymentConfig",
    # 支付渠道
    "AlipayClient",
    "WechatClient",
    "QQClient",
    "AllinPayClient",
    "AllinPayConfig",
    "LakalaClient",
    "LakalaConfig",
    "ApplePayClient",
    "ApplePayConfig",
    "PayPalClient",
    "PayPalConfig",
    "SaobeiClient",
    "SaobeiConfig",
    # API服务
    "PayApiServer",
    "AlipayApiHandler",
    "WechatApiHandler",
    "ApplePayApiHandler",
    "PayPalApiHandler",
    "SaobeiApiHandler",
    "ErrorHandler",
    "AuthMiddleware",
    # 异常
    "GoPayError",
    "ConfigError",
    "SignError",
    "PaymentError",
    "NetworkError",
    # 版本
    "__version__",
]
