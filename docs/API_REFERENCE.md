# Pay-Stack Python SDK - API 参考文档

## 核心模块

### gopay.config

配置管理模块,提供各种支付方式的配置类。

#### PaymentConfig

基础配置类。

**参数:**
- `app_id` (str): 应用ID
- `mch_id` (str, optional): 商户号
- `api_key` (str, optional): API密钥
- `notify_url` (str, optional): 异步通知URL
- `return_url` (str, optional): 同步返回URL
- `gateway_url` (str, optional): 网关地址
- `is_sandbox` (bool): 是否沙箱环境,默认False
- `timeout` (int): 超时时间(秒),默认30
- `cert_path` (str, optional): 证书路径
- `key_path` (str, optional): 私钥路径
- `cert_pem` (str, optional): 证书内容
- `key_pem` (str, optional): 私钥内容

**方法:**
- `validate()`: 验证配置
- `to_dict()`: 转换为字典
- `from_dict(config_dict)`: 从字典创建
- `from_file(config_file)`: 从文件创建
- `get_cert_content()`: 获取证书内容
- `get_key_content()`: 获取私钥内容

#### AlipayConfig

支付宝配置类,继承自PaymentConfig。

**额外参数:**
- `gateway_url` (str): 支付宝网关,默认"https://openapi.alipay.com/gateway.do"
- `sign_type` (str): 签名类型,默认"RSA2"
- `charset` (str): 字符集,默认"utf-8"
- `format` (str): 格式,默认"JSON"
- `app_private_key` (str, optional): 应用私钥
- `app_private_key_path` (str, optional): 应用私钥路径
- `alipay_public_key` (str, optional): 支付宝公钥
- `alipay_public_key_path` (str, optional): 支付宝公钥路径

**方法:**
- `get_app_private_key()`: 获取应用私钥
- `get_alipay_public_key()`: 获取支付宝公钥

#### WechatConfig

微信支付配置类,继承自PaymentConfig。

**额外参数:**
- `api_v3_key` (str, optional): API v3密钥
- `serial_no` (str, optional): 商户序列号
- `gateway_url` (str): 微信支付网关,默认"https://api.mch.weixin.qq.com"
- `sign_type` (str): 签名类型,默认"HMAC-SHA256"
- `mp_app_id` (str, optional): 小程序AppID
- `app_app_id` (str, optional): APP应用ID

#### QQConfig

QQ钱包配置类,继承自PaymentConfig。

**额外参数:**
- `gateway_url` (str): QQ支付网关,默认"https://qpay.qq.com/cgi-bin/pay"
- `sign_type` (str): 签名类型,默认"HMAC-SHA256"

---

### gopay.utils

工具模块,提供数据结构和签名功能。

#### BodyMap

灵活的参数构建器。

**方法:**
- `set(key, value)`: 设置参数值,支持链式调用
- `get(key, default=None)`: 获取参数值
- `remove(key)`: 移除参数
- `contains(key)`: 检查是否包含参数
- `clear()`: 清空所有参数
- `to_dict()`: 转换为字典
- `to_json()`: 转换为JSON字符串
- `to_url_params()`: 转换为URL参数字符串
- `encode_wechat_sign_params()`: 编码微信签名参数
- `encode_alipay_sign_params()`: 编码支付宝签名参数
- `filter_none()`: 过滤None值
- `update(other)`: 更新参数

**示例:**
```python
params = BodyMap()
params.set("out_trade_no", "ORDER_001") \
      .set("total_amount", "0.01") \
      .set("subject", "测试商品")
```

#### XmlMap

XML处理工具。

**方法:**
- `set(key, value)`: 设置XML节点值
- `to_xml()`: 转换为XML字符串
- `from_xml(xml_str, root_name="xml")`: 从XML字符串解析
- `to_dict()`: 转换为字典

**示例:**
```python
xml_map = XmlMap()
xml_map.set("return_code", "SUCCESS")
xml_map.set("return_msg", "OK")
xml_str = xml_map.to_xml()
```

#### ResponseData

统一响应数据封装。

**属性:**
- `success` (bool): 是否成功
- `data` (dict): 响应数据
- `error` (str): 错误信息
- `code` (str): 错误代码
- `raw_response` (str): 原始响应

**方法:**
- `to_dict()`: 转换为字典
- `success_response(data, raw_response=None)`: 创建成功响应
- `error_response(error, code=None, raw_response=None)`: 创建错误响应

#### 签名函数

- `sign_params(params, key, sign_type="HMAC-SHA256")`: 对参数签名
- `verify_params(params, key, sign_type="HMAC-SHA256")`: 验证参数签名
- `generate_sign(content, key, sign_type="HMAC-SHA256")`: 生成签名
- `verify_sign(content, signature, key, sign_type="HMAC-SHA256")`: 验证签名

#### SignerFactory

签名器工厂。

**方法:**
- `get_signer(sign_type)`: 获取签名器
- `register_signer(sign_type, signer)`: 注册自定义签名器

---

### gopay.alipay

支付宝支付模块。

#### AlipayClient

支付宝支付客户端。

**初始化:**
```python
client = AlipayClient(config)
```

**支付方法:**
- `trade_page_pay(params)`: PC网站支付
- `trade_wap_pay(params)`: 手机网站支付
- `trade_app_pay(params)`: APP支付
- `trade_create(params)`: 交易创建

**订单管理:**
- `trade_query(out_trade_no=None, trade_no=None)`: 查询订单
- `trade_close(out_trade_no=None, trade_no=None)`: 关闭订单
- `trade_cancel(out_trade_no=None, trade_no=None)`: 撤销交易

**退款方法:**
- `trade_refund(refund_amount, out_trade_no=None, trade_no=None, **kwargs)`: 申请退款
- `trade_fastpay_refund_query(out_trade_no=None, trade_no=None, out_request_no=None)`: 查询退款

**通用接口:**
- `create_order(params)`: 创建订单
- `query_order(order_no, trade_no=None)`: 查询订单
- `close_order(order_no, trade_no=None)`: 关闭订单
- `refund(order_no, refund_amount, refund_no=None, **kwargs)`: 申请退款
- `query_refund(refund_no, order_no=None)`: 查询退款
- `verify_notify(data, signature)`: 验证通知

---

### gopay.wechat

微信支付模块。

#### WechatClient

微信支付客户端。

**初始化:**
```python
client = WechatClient(config)
```

**支付方法:**
- `unified_order(body, out_trade_no, total_fee, spbill_create_ip, trade_type, **kwargs)`: 统一下单

**订单管理:**
- `order_query(out_trade_no=None, transaction_id=None)`: 查询订单
- `close_order(out_trade_no)`: 关闭订单

**退款方法:**
- `refund(out_trade_no, out_refund_no, total_fee, refund_fee, **kwargs)`: 申请退款
- `refund_query(out_refund_no=None, transaction_id=None)`: 查询退款

**通用接口:**
- `create_order(params)`: 创建订单
- `query_order(order_no, transaction_id=None)`: 查询订单
- `close_order(order_no)`: 关闭订单
- `refund(order_no, refund_amount, refund_no=None, **kwargs)`: 申请退款
- `query_refund(refund_no, transaction_id=None)`: 查询退款
- `verify_notify(data, signature)`: 验证通知

---

### gopay.qq

QQ钱包支付模块。

#### QQClient

QQ钱包支付客户端。

API接口与WechatClient类似,支持:
- 统一下单
- 订单查询
- 关闭订单
- 申请退款
- 查询退款

---

### gopay.notify

通知处理模块。

#### NotifyHandler

通知处理器抽象基类。

**方法:**
- `parse(raw_data)`: 解析原始通知数据
- `verify(data, signature)`: 验证通知签名
- `success_response()`: 返回成功响应
- `fail_response(message="")`: 返回失败响应

#### AlipayNotifyHandler

支付宝通知处理器。

**初始化:**
```python
handler = AlipayNotifyHandler(public_key="xxx", sign_type="RSA2")
```

#### WechatNotifyHandler

微信通知处理器。

**初始化:**
```python
handler = WechatNotifyHandler(api_key="xxx", sign_type="HMAC-SHA256")
```

#### QQNotifyHandler

QQ钱包通知处理器。

**初始化:**
```python
handler = QQNotifyHandler(api_key="xxx", sign_type="HMAC-SHA256")
```

#### NotifyProcessor

通知处理器。

**初始化:**
```python
processor = NotifyProcessor(handler)
```

**方法:**
- `process(raw_data, callback=None)`: 处理通知

#### notify_handler_decorator

通知处理装饰器。

**使用:**
```python
@notify_handler_decorator(handler)
def handle_notify(notify_data):
    # 处理通知
    return True
```

---

### gopay.exceptions

异常模块。

**异常类:**
- `GoPayError`: 基础异常
- `ConfigError`: 配置错误
- `SignError`: 签名错误
- `PaymentError`: 支付业务错误
- `NetworkError`: 网络错误
- `CertificateError`: 证书错误
- `ValidationError`: 验证错误
- `NotifyError`: 通知处理错误

**使用示例:**
```python
from gopay.exceptions import ConfigError, PaymentError

try:
    result = client.create_order(params)
    if not result.success:
        raise PaymentError(result.error, result.code)
except ConfigError as e:
    print(f"配置错误: {e}")
except PaymentError as e:
    print(f"支付错误: {e}")
```

---

## 使用示例

详细示例请参考 `examples/` 目录:
- `alipay_example.py`: 支付宝支付完整示例
- `wechat_example.py`: 微信支付完整示例

---

## 更多文档

- [快速开始](QUICKSTART.md)
- [架构文档](../ARCHITECTURE.md)
- [项目总结](../PROJECT_SUMMARY.md)
- [README](../README.md)
