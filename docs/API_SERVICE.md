# GoPay API服务功能说明

## 概述

Pay-Stack Python SDK提供完整的API服务功能,允许将支付功能快速封装为HTTP REST API,支持微服务架构和聚合支付场景。

遵循**SOLID原则**设计:
- ✅ 单一职责原则(SRP): 每个模块专注于单一功能
- ✅ 开闭原则(OCP): 通过继承和组合扩展功能
- ✅ 里氏替换原则(LSP): 所有处理器可互换
- ✅ 接口隔离原则(ISP): 最小化接口依赖
- ✅ 依赖倒置原则(DIP): 依赖抽象而非具体实现

---

## 架构设计

### 核心组件

```
gopay/api/
├── __init__.py              # API模块导出
├── server.py                # API服务器(Flask/FastAPI)
├── response.py              # 统一响应格式
├── middleware.py            # 中间件(认证/日志/限流)
└── handlers/                # API处理器
    ├── __init__.py
    ├── base.py              # 基础处理器(抽象类)
    ├── alipay.py            # 支付宝处理器
    ├── wechat.py            # 微信支付处理器
    ├── apple_pay.py         # Apple Pay处理器
    ├── paypal.py            # PayPal处理器
    ├── saobei.py            # 扫呗处理器
    └── aggregated.py        # 聚合支付处理器
```

### 设计模式

1. **策略模式**: 不同的Web框架(Flask/FastAPI)实现相同接口
2. **装饰器模式**: 中间件使用装饰器模式增强功能
3. **工厂模式**: 通过注册机制创建处理器
4. **责任链模式**: 中间件链式处理请求

---

## 功能特性

### 1. 统一响应格式

所有API返回统一的JSON格式:

```json
{
    "code": "0",           // "0"表示成功,其他表示错误
    "msg": "Success",      // 响应消息
    "data": {...},         // 响应数据(可选)
    "trace_id": "...",     // 追踪ID(可选)
    "timestamp": 1234567890 // 时间戳(可选)
}
```

**优势**:
- ✅ 统一的错误处理
- ✅ 便于日志追踪
- ✅ 客户端友好

### 2. 多框架支持

支持两种主流Python Web框架:

#### Flask框架

```python
from gopay.api import PayApiServer

server = PayApiServer(framework="flask")
server.start(host="0.0.0.0", port=8000)
```

#### FastAPI框架

```python
from gopay.api import PayApiServer

server = PayApiServer(framework="fastapi")
server.start(host="0.0.0.0", port=8000)
```

**优势**:
- ✅ 灵活选择框架
- ✅ 无需修改业务代码
- ✅ 易于切换

### 3. 聚合支付

通过统一的接口处理多种支付渠道:

```python
from gopay.api.handlers import AggregatedPayHandler

aggregated = AggregatedPayHandler()
aggregated.register_handler("alipay", alipay_handler)
aggregated.register_handler("wechat", wechat_handler)

# 统一的API调用
result = aggregated.create_order("alipay", {...})
result = aggregated.create_order("wechat", {...})
```

**优势**:
- ✅ 统一接口
- ✅ 简化客户端集成
- ✅ 灵活切换渠道

### 4. 中间件系统

提供多种中间件功能:

#### 错误处理中间件

```python
from gopay.api.middleware import ErrorHandler

server.add_middleware(ErrorHandler())
```

- ✅ 自动捕获异常
- ✅ 统一错误响应
- ✅ 详细错误日志

#### 认证中间件

```python
from gopay.api.middleware import AuthMiddleware

auth = AuthMiddleware(api_keys=["key1", "key2"])
server.add_middleware(auth)
```

- ✅ API密钥验证
- ✅ 动态添加/删除密钥
- ✅ 安全保护

#### 日志中间件

```python
from gopay.api.middleware import LoggingMiddleware

server.add_middleware(LoggingMiddleware())
```

- ✅ 请求日志记录
- ✅ 响应日志记录
- ✅ 性能统计

#### 限流中间件

```python
from gopay.api.middleware import RateLimiter

rate_limiter = RateLimiter(max_requests=100, window=60)
server.add_middleware(rate_limiter)
```

- ✅ 防止API滥用
- ✅ 可配置限流策略
- ✅ 自动清理过期记录

**优势**:
- ✅ 模块化设计
- ✅ 可组合使用
- ✅ 易于扩展

### 5. 钩子系统

支持在关键操作前后插入自定义逻辑:

```python
# 定义钩子函数
def before_create_order(trace_id, params):
    print(f"创建订单前: {trace_id}, 参数: {params}")

def after_create_order(trace_id, result, success):
    print(f"创建订单后: {trace_id}, 成功: {success}, 结果: {result}")

# 注册钩子
handler.register_hook("before_create_order", before_create_order)
handler.register_hook("after_create_order", after_create_order)
```

**优势**:
- ✅ 灵活的扩展点
- ✅ 无需修改核心代码
- ✅ 支持异步操作

---

## API端点

服务器启动后提供以下REST API端点:

| 端点 | 方法 | 说明 | 参数 |
|------|------|------|------|
| `/api/v1/pay/create_order` | POST | 创建订单 | channel, params |
| `/api/v1/pay/query_order` | POST | 查询订单 | channel, params |
| `/api/v1/pay/close_order` | POST | 关闭订单 | channel, params |
| `/api/v1/pay/refund` | POST | 申请退款 | channel, params |
| `/api/v1/pay/query_refund` | POST | 查询退款 | channel, params |
| `/api/v1/pay/cancel_order` | POST | 撤销订单 | channel, params |
| `/api/v1/health` | GET | 健康检查 | - |
| `/api/v1/channels` | GET | 支持的渠道 | - |

### 请求格式

```json
{
    "channel": "alipay",
    "params": {
        // 渠道特定的参数
    }
}
```

### 响应格式

```json
{
    "code": "0",
    "msg": "Success",
    "data": {
        // 响应数据
    },
    "trace_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": 1737331200
}
```

---

## 使用场景

### 1. 微服务架构

将支付功能独立为微服务:

```python
# 支付服务
payment_service = PayApiServer(framework="flask")
payment_service.register_payment_channel("alipay", alipay_handler)
payment_service.register_payment_channel("wechat", wechat_handler)
payment_service.start(port=8001)
```

**优势**:
- ✅ 服务解耦
- ✅ 独立部署
- ✅ 技术栈灵活

### 2. 聚合支付平台

统一处理多种支付渠道:

```python
# 支持所有支付渠道
for channel in ["alipay", "wechat", "apple_pay", "paypal"]:
    handler = create_handler(channel)
    server.register_payment_channel(channel, handler)
```

**优势**:
- ✅ 统一入口
- ✅ 简化集成
- ✅ 便于管理

### 3. B2B SaaS平台

为多个商户提供支付服务:

```python
# 每个商户独立的API密钥
merchant_auth = AuthMiddleware(api_keys=merchant_api_keys)
server.add_middleware(merchant_auth)

# 限流保护每个商户
merchant_rate_limiter = RateLimiter(max_requests=1000, window=3600)
server.add_middleware(merchant_rate_limiter)
```

**优势**:
- ✅ 多租户支持
- ✅ 安全隔离
- ✅ 资源保护

---

## 最佳实践

### 1. 安全配置

```python
# 生产环境建议
server = PayApiServer(framework="flask")
server.add_middleware(ErrorHandler())
server.add_middleware(AuthMiddleware(api_keys=get_api_keys_from_db()))
server.add_middleware(RateLimiter(max_requests=100, window=60))
server.add_middleware(LoggingMiddleware())

# 使用HTTPS
server.start(host="0.0.0.0", port=443, ssl_context="adheme")
```

### 2. 监控和日志

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('payment_api.log'),
        logging.StreamHandler()
    ]
)

# 添加日志中间件
server.add_middleware(LoggingMiddleware())
```

### 3. 错误处理

```python
# 自定义错误处理
def custom_error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            logger.error(f"验证错误: {e}")
            return ApiResponse.invalid_params(str(e))
        except AuthenticationError as e:
            logger.error(f"认证错误: {e}")
            return ApiResponse.unauthorized(str(e))
        except Exception as e:
            logger.error(f"未知错误: {e}", exc_info=True)
            return ApiResponse.server_error("内部服务器错误")
    return wrapper
```

### 4. 性能优化

```python
# 使用连接池
from gopay.http import HttpClient

http_client = HttpClient(
    timeout=30,
    max_retries=3,
    pool_connections=100,
    pool_maxsize=100
)
```

---

## 扩展性

### 添加新的支付渠道

```python
from gopay.api.handlers.base import BaseApiHandler

class CustomPayApiHandler(BaseApiHandler):
    def create_order(self, params):
        # 实现创建订单逻辑
        pass

    def query_order(self, params):
        # 实现查询订单逻辑
        pass

    # ... 实现其他方法

# 注册新渠道
server.register_payment_channel("custom", CustomPayApiHandler(client))
```

### 自定义中间件

```python
from gopay.api.middleware import MiddlewareChain

class CustomMiddleware:
    def handle(self, func):
        def wrapper(*args, **kwargs):
            # 前置处理
            result = func(*args, **kwargs)
            # 后置处理
            return result
        return wrapper

server.add_middleware(CustomMiddleware())
```

---

## 完整示例

详见: [examples/api_server_example.py](../examples/api_server_example.py)

---

## 对比传统方式

| 特性 | 传统方式 | API服务方式 |
|------|---------|------------|
| **部署方式** | 集成到业务代码 | 独立微服务 |
| **技术栈** | 绑定特定框架 | 灵活选择 |
| **多渠道支持** | 分散在多处 | 统一聚合 |
| **扩展性** | 需修改核心代码 | 即插即用 |
| **维护成本** | 高 | 低 |
| **安全隔离** | 困难 | 容易 |

---

## 总结

GoPay API服务提供了:

✅ **完整的功能**: 支持所有支付渠道
✅ **灵活的架构**: 遵循SOLID原则
✅ **易于使用**: 简单的API接口
✅ **生产就绪**: 完善的中间件支持
✅ **高度扩展**: 支持自定义和扩展

**适用场景**:
- 微服务架构
- 聚合支付平台
- B2B SaaS平台
- 多租户系统
- API服务提供商

---

**更新时间**: 2025-01-20
