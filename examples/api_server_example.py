"""
GoPay API服务器使用示例
展示如何将GoPay支付功能封装为HTTP API服务

支持多种Web框架:Flask, FastAPI
支持聚合支付:统一接口处理多种支付渠道
"""

from gopay import (
    AlipayClient,
    WechatClient,
    ApplePayClient,
    PayPalClient,
    SaobeiClient,
)
from gopay.config import (
    AlipayConfig,
    WechatConfig,
    ApplePayConfig,
    PayPalConfig,
    SaobeiConfig,
)
from gopay.api import PayApiServer
from gopay.api.handlers import (
    AlipayApiHandler,
    WechatApiHandler,
    ApplePayApiHandler,
    PayPalApiHandler,
    SaobeiApiHandler,
)
from gopay.api.middleware import (
    ErrorHandler,
    AuthMiddleware,
    LoggingMiddleware,
    RateLimiter,
)


def create_flask_api_server():
    """
    创建Flask API服务器示例

    Returns:
        PayApiServer: API服务器实例
    """
    print("=" * 60)
    print("创建Flask API服务器")
    print("=" * 60)

    # 1. 创建配置
    alipay_config = AlipayConfig(
        app_id="your_app_id",
        app_private_key="your_app_private_key",
        alipay_public_key="alipay_public_key",
        is_sandbox=True,
    )

    wechat_config = WechatConfig(
        app_id="your_app_id",
        mch_id="your_mch_id",
        api_key="your_api_key",
        is_sandbox=True,
    )

    # 2. 创建客户端
    alipay_client = AlipayClient(alipay_config)
    wechat_client = WechatClient(wechat_config)

    # 3. 创建API处理器
    alipay_handler = AlipayApiHandler(alipay_client)
    wechat_handler = WechatApiHandler(wechat_client)

    # 4. 创建API服务器
    server = PayApiServer(framework="flask")

    # 5. 注册支付渠道
    server.register_payment_channel("alipay", alipay_handler)
    server.register_payment_channel("wechat", wechat_handler)

    # 6. 添加中间件
    server.add_middleware(ErrorHandler())
    server.add_middleware(LoggingMiddleware())

    # 可选: 添加认证中间件
    # auth_middleware = AuthMiddleware(api_keys=["your_api_key_1", "your_api_key_2"])
    # server.add_middleware(auth_middleware)

    # 可选: 添加限流中间件
    # rate_limiter = RateLimiter(max_requests=100, window=60)
    # server.add_middleware(rate_limiter)

    print("\n✅ Flask API服务器创建成功!")
    print("支持的支付渠道:", server.aggregated_handler.supported_channels())

    return server


def create_fastapi_server():
    """
    创建FastAPI服务器示例

    Returns:
        PayApiServer: API服务器实例
    """
    print("=" * 60)
    print("创建FastAPI服务器")
    print("=" * 60)

    # 1. 创建配置和客户端 (同上)
    alipay_config = AlipayConfig(
        app_id="your_app_id",
        app_private_key="your_app_private_key",
        alipay_public_key="alipay_public_key",
        is_sandbox=True,
    )

    wechat_config = WechatConfig(
        app_id="your_app_id",
        mch_id="your_mch_id",
        api_key="your_api_key",
        is_sandbox=True,
    )

    # 2. 创建客户端
    alipay_client = AlipayClient(alipay_config)
    wechat_client = WechatClient(wechat_config)

    # 3. 创建API处理器
    alipay_handler = AlipayApiHandler(alipay_client)
    wechat_handler = WechatApiHandler(wechat_client)

    # 4. 创建API服务器
    server = PayApiServer(framework="fastapi")

    # 5. 注册支付渠道
    server.register_payment_channel("alipay", alipay_handler)
    server.register_payment_channel("wechat", wechat_handler)

    # 6. 添加中间件
    server.add_middleware(ErrorHandler())
    server.add_middleware(LoggingMiddleware())

    print("\n✅ FastAPI服务器创建成功!")
    print("支持的支付渠道:", server.aggregated_handler.supported_channels())

    return server


def create_aggregated_payment_server():
    """
    创建聚合支付服务器示例
    统一接口支持多种支付渠道

    Returns:
        PayApiServer: API服务器实例
    """
    print("=" * 60)
    print("创建聚合支付服务器")
    print("=" * 60)

    # 1. 创建所有支付渠道的配置和客户端
    configs = {
        "alipay": AlipayConfig(
            app_id="alipay_app_id",
            app_private_key="alipay_private_key",
            alipay_public_key="alipay_public_key",
            is_sandbox=True,
        ),
        "wechat": WechatConfig(
            app_id="wechat_app_id",
            mch_id="wechat_mch_id",
            api_key="wechat_api_key",
            is_sandbox=True,
        ),
        "apple_pay": ApplePayConfig(
            app_shared_secret="apple_shared_secret",
            sandbox=True,
        ),
        "paypal": PayPalConfig(
            client_id="paypal_client_id",
            client_secret="paypal_client_secret",
            sandbox=True,
        ),
        "saobei": SaobeiConfig(
            merchant_id="saobei_merchant_id",
            terminal_id="saobei_terminal_id",
            key="saobei_key",
        ),
    }

    # 2. 创建客户端
    clients = {
        "alipay": AlipayClient(configs["alipay"]),
        "wechat": WechatClient(configs["wechat"]),
        "apple_pay": ApplePayClient(configs["apple_pay"]),
        "paypal": PayPalClient(configs["paypal"]),
        "saobei": SaobeiClient(configs["saobei"]),
    }

    # 3. 创建API处理器
    handlers = {
        "alipay": AlipayApiHandler(clients["alipay"]),
        "wechat": WechatApiHandler(clients["wechat"]),
        "apple_pay": ApplePayApiHandler(clients["apple_pay"]),
        "paypal": PayPalApiHandler(clients["paypal"]),
        "saobei": SaobeiApiHandler(clients["saobei"]),
    }

    # 4. 创建API服务器
    server = PayApiServer(framework="flask")

    # 5. 注册所有支付渠道
    for channel, handler in handlers.items():
        server.register_payment_channel(channel, handler)

    # 6. 添加认证和限流中间件
    auth_middleware = AuthMiddleware(api_keys=["your_api_key"])
    rate_limiter = RateLimiter(max_requests=100, window=60)

    server.add_middleware(ErrorHandler())
    server.add_middleware(auth_middleware)
    server.add_middleware(rate_limiter)
    server.add_middleware(LoggingMiddleware())

    print("\n✅ 聚合支付服务器创建成功!")
    print("支持的支付渠道:", server.aggregated_handler.supported_channels())
    print("\n聚合支付优势:")
    print("- ✅ 统一的API接口")
    print("- ✅ 支持多种支付渠道")
    print("- ✅ 简化客户端集成")
    print("- ✅ 灵活的渠道切换")

    return server


def run_server_example():
    """运行API服务器示例"""

    print("\n" + "=" * 60)
    print("GoPay API服务器示例")
    print("=" * 60)

    # 选择要创建的服务器类型
    server_type = input("\n选择服务器类型 (1:Flask, 2:FastAPI, 3:聚合支付): ").strip()

    if server_type == "1":
        server = create_flask_api_server()
    elif server_type == "2":
        server = create_fastapi_server()
    elif server_type == "3":
        server = create_aggregated_payment_server()
    else:
        print("❌ 无效的选择")
        return

    # 启动服务器
    print("\n" + "=" * 60)
    print("API端点说明:")
    print("=" * 60)
    print("""
可用的API端点:

1. 创建订单:
   POST /api/v1/pay/create_order
   {
       "channel": "alipay",
       "params": {
           "out_trade_no": "ORDER001",
           "total_amount": "0.01",
           "subject": "测试商品"
       }
   }

2. 查询订单:
   POST /api/v1/pay/query_order
   {
       "channel": "alipay",
       "params": {
           "out_trade_no": "ORDER001"
       }
   }

3. 关闭订单:
   POST /api/v1/pay/close_order
   {
       "channel": "alipay",
       "params": {
           "out_trade_no": "ORDER001"
       }
   }

4. 申请退款:
   POST /api/v1/pay/refund
   {
       "channel": "alipay",
       "params": {
           "out_trade_no": "ORDER001",
           "refund_amount": "0.01",
           "refund_no": "REFUND001"
       }
   }

5. 查询退款:
   POST /api/v1/pay/query_refund
   {
       "channel": "alipay",
       "params": {
           "out_trade_no": "ORDER001",
           "refund_no": "REFUND001"
       }
   }

6. 健康检查:
   GET /api/v1/health

7. 支持的渠道:
   GET /api/v1/channels

响应格式:
{
    "code": "0",          # "0"表示成功
    "msg": "Success",
    "data": {...},
    "trace_id": "...",     # 追踪ID
    "timestamp": 1234567890
}
    """)

    print("\n" + "=" * 60)
    print("启动服务器...")
    print("=" * 60)

    try:
        server.start(host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("\n\n服务器已停止")
        server.stop()


def api_call_example():
    """API调用示例"""

    print("\n" + "=" * 60)
    print("API调用示例 (使用requests库)")
    print("=" * 60)

    example_code = """
import requests

# API基础URL
BASE_URL = "http://localhost:8000"

# 1. 创建订单
response = requests.post(f"{BASE_URL}/api/v1/pay/create_order", json={
    "channel": "alipay",
    "params": {
        "out_trade_no": "ORDER20250120001",
        "total_amount": "0.01",
        "subject": "测试商品"
    }
})

result = response.json()
if result["code"] == "0":
    print("订单创建成功:", result["data"])
else:
    print("订单创建失败:", result["msg"])

# 2. 查询订单
response = requests.post(f"{BASE_URL}/api/v1/pay/query_order", json={
    "channel": "alipay",
    "params": {
        "out_trade_no": "ORDER20250120001"
    }
})

result = response.json()
print("订单状态:", result)

# 3. 申请退款
response = requests.post(f"{BASE_URL}/api/v1/pay/refund", json={
    "channel": "alipay",
    "params": {
        "out_trade_no": "ORDER20250120001",
        "refund_amount": "0.01",
        "refund_no": "REFUND20250120001"
    }
})

result = response.json()
if result["code"] == "0":
    print("退款申请成功:", result["data"])

# 4. 使用聚合支付切换渠道
# 只需要修改channel参数即可
channels = ["alipay", "wechat", "apple_pay", "paypal", "saobei"]

for channel in channels:
    response = requests.post(f"{BASE_URL}/api/v1/pay/create_order", json={
        "channel": channel,
        "params": {
            # ... 各渠道的参数
        }
    })
    print(f"{channel} 创建订单结果:", response.json())
"""

    print(example_code)

    print("\n" + "=" * 60)
    print("聚合支付优势:")
    print("=" * 60)
    print("""
✅ 统一接口
   - 所有支付渠道使用相同的API格式
   - 无需学习不同渠道的差异

✅ 简化集成
   - 客户端只需对接一个API
   - 服务端负责处理渠道差异

✅ 灵活切换
   - 随时切换支付渠道
   - 根据业务需求选择最优渠道

✅ 易于扩展
   - 新增支付渠道不影响现有代码
   - 遵循开闭原则(OCP)

✅ 统一管理
   - 统一的日志记录
   - 统一的错误处理
   - 统一的认证授权
""")


# ==================== 主程序 ====================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("GoPay API服务器使用示例")
    print("=" * 60)

    print("\n请选择:")
    print("1. 启动API服务器")
    print("2. 查看API调用示例")

    choice = input("\n请输入选择 (1/2): ").strip()

    if choice == "1":
        run_server_example()
    elif choice == "2":
        api_call_example()
    else:
        print("❌ 无效的选择")

    print("\n" + "=" * 60)
    print("示例程序运行完成!")
    print("=" * 60)
