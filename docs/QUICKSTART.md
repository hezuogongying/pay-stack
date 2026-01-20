# Pay-Stack Python SDK - 快速开始指南

## 安装

```bash
pip install pay-stack
```

或从源码安装:

```bash
git clone https://github.com/your-org/pay-stack.git
cd pay-stack
pip install -e .
```

## 5分钟快速上手

### 支付宝支付

```python
from gopay.alipay import AlipayClient
from gopay.config import AlipayConfig
from gopay.utils import BodyMap

# 1. 配置(使用沙箱环境测试)
config = AlipayConfig(
    app_id="2021000000000000",
    app_private_key="""-----BEGIN RSA PRIVATE KEY-----
    你的应用私钥
    -----END RSA PRIVATE KEY-----""",
    alipay_public_key="""-----BEGIN PUBLIC KEY-----
    支付宝公钥
    -----END PUBLIC KEY-----""",
    is_sandbox=True,  # 沙箱环境
)

# 2. 创建客户端
client = AlipayClient(config)

# 3. 创建PC网站支付
params = BodyMap()
params.set("out_trade_no", "ORDER_001")
params.set("total_amount", "0.01")
params.set("subject", "测试商品")

result = client.trade_page_pay(params)
if result.success:
    print("支付链接:", result.data["pay_url"])

# 4. 查询订单
result = client.query_order(order_no="ORDER_001")
if result.success:
    print("订单状态:", result.data["trade_status"])

# 5. 申请退款
result = client.refund(
    order_no="ORDER_001",
    refund_amount=0.01,
    refund_no="REFUND_001",
)
if result.success:
    print("退款成功")
```

### 微信支付

```python
from gopay.wechat import WechatClient
from gopay.config import WechatConfig

# 1. 配置
config = WechatConfig(
    app_id="wx0000000000000000",
    mch_id="10000000",
    api_key="your_api_key_32_characters",
)

# 2. 创建客户端
client = WechatClient(config)

# 3. 创建NATIVE支付
result = client.unified_order(
    body="测试商品",
    out_trade_no="ORDER_001",
    total_fee=1,  # 单位:分
    spbill_create_ip="127.0.0.1",
    trade_type="NATIVE",
)

if result.success:
    print("二维码链接:", result.data["code_url"])

# 4. 查询订单
result = client.query_order(order_no="ORDER_001")
if result.success:
    print("订单状态:", result.data["trade_state"])
```

### 处理支付通知(FastAPI示例)

```python
from fastapi import FastAPI, Request
from gopay.notify import AlipayNotifyHandler, NotifyProcessor

app = FastAPI()

# 创建通知处理器
handler = AlipayNotifyHandler(
    public_key="支付宝公钥",
    sign_type="RSA2"
)
processor = NotifyProcessor(handler)

@app.post("/notify/alipay")
async def alipay_notify(request: Request):
    """支付宝异步通知"""
    raw_data = await request.body()

    # 定义业务处理函数
    def handle_notify(data):
        print("收到通知:", data)
        # 处理业务逻辑
        # 返回True表示处理成功
        return True

    # 处理通知
    response = processor.process(raw_data, handle_notify)
    return response
```

### 处理支付通知(Flask示例)

```python
from flask import Flask, request
from gopay.notify import WechatNotifyHandler, NotifyProcessor

app = Flask(__name__)

# 创建通知处理器
handler = WechatNotifyHandler(
    api_key="your_api_key",
    sign_type="HMAC-SHA256"
)
processor = NotifyProcessor(handler)

@app.route("/notify/wechat", methods=["POST"])
def wechat_notify():
    """微信异步通知"""
    raw_data = request.data

    # 定义业务处理函数
    def handle_notify(data):
        print("收到通知:", data)
        # 处理业务逻辑
        return True

    # 处理通知
    response = processor.process(raw_data, handle_notify)
    return response
```

## 配置方式

### 方式1: 代码直接配置

```python
from gopay.config import AlipayConfig

config = AlipayConfig(
    app_id="your_app_id",
    app_private_key="your_private_key",
    alipay_public_key="alipay_public_key",
    notify_url="https://your-site.com/notify",
    is_sandbox=False,
)
```

### 方式2: 从字典配置

```python
config_dict = {
    "app_id": "your_app_id",
    "app_private_key": "your_private_key",
    "alipay_public_key": "alipay_public_key",
}

config = AlipayConfig.from_dict(config_dict)
```

### 方式3: 从配置文件

```python
# config.json
{
    "app_id": "your_app_id",
    "app_private_key": "your_private_key",
    "alipay_public_key": "alipay_public_key"
}

# 代码中
config = AlipayConfig.from_file("config.json")
```

## BodyMap 使用技巧

### 链式调用

```python
params = BodyMap()
params.set("out_trade_no", "ORDER_001") \
      .set("total_amount", "0.01") \
      .set("subject", "测试商品")
```

### 自动过滤空值

```python
params = BodyMap()
params.set("key1", "value1")
params.set("key2", None)  # 不会被添加
params.set("key3", "")    # 不会被添加
```

### 转换为不同格式

```python
params = BodyMap()
params.set("key1", "value1")

# 转为字典
data = params.to_dict()

# 转为JSON
json_str = params.to_json()

# 转为URL参数
url_params = params.to_url_params()

# 编码签名参数
sign_params = params.encode_wechat_sign_params()
```

## 常见问题

### 1. 如何获取支付宝密钥?

1. 登录支付宝开放平台
2. 创建应用并上传应用公钥
3. 获取支付宝公钥
4. 在代码中配置应用私钥和支付宝公钥

### 2. 微信支付金额单位是什么?

微信支付金额单位是**分**,需要转换:
```python
# 0.01元 = 1分
total_fee = int(0.01 * 100)  # 1
```

### 3. 如何切换沙箱/正式环境?

```python
# 支付宝
config = AlipayConfig(
    ...
    is_sandbox=True,  # True=沙箱, False=正式
)

# 微信
config = WechatConfig(
    ...
    is_sandbox=True,  # True=沙箱, False=正式
)
```

### 4. 如何处理证书?

```python
config = WechatConfig(
    ...
    cert_path="/path/to/cert.pem",  # 证书路径
    key_path="/path/to/key.pem",    # 私钥路径
)

# 或者直接传入证书内容
config = WechatConfig(
    ...
    cert_pem="证书内容",
    key_pem="私钥内容",
)
```

### 5. 如何查看详细日志?

```python
import logging

# 配置日志级别
logging.basicConfig(level=logging.DEBUG)

config = AlipayConfig(
    ...
    enable_log=True,  # 启用日志
)
```

## 下一步

- 查看 [README.md](../README.md) 了解完整功能
- 查看 [ARCHITECTURE.md](../ARCHITECTURE.md) 了解架构设计
- 查看 [examples/](../examples/) 目录中的更多示例
- 查看各支付方式的官方文档了解参数含义

## 技术支持

- GitHub Issues: https://github.com/your-org/pay-stack/issues
- Email: support@gopay.com

## 相关文档

- [支付宝开放平台文档](https://opendocs.alipay.com/)
- [微信支付开发文档](https://pay.weixin.qq.com/wiki/doc/api/index.html)
- [QQ钱包商户文档](https://qpay.qq.com/)
