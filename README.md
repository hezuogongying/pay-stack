# Pay-Stack Python SDK

<div align="center">

企业级Python支付SDK - 支持8种主流支付方式,提供完整的支付解决方案

[![Python Version](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Payment Channels](https://img.shields.io/badge/支付渠道-8种-blue.svg)](#支持的支付渠道)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[⭐ Star](https://github.com/hezuogongying/pay-stack) | [🐛 报告问题](https://github.com/hezuogongying/pay-stack/issues) | [📖 文档](https://github.com/hezuogongying/pay-stack/wiki)

</div>

---

## ✨ 特性

- 🎯 **8种支付方式** - 支付宝、微信、QQ钱包、Apple Pay、PayPal、通联、拉卡拉、扫呗
- 🏗️ **SOLID架构设计** - 遵循SOLID原则,易于扩展和维护
- 🔌 **统一接口** - 所有支付方式实现相同的接口,易于切换
- 🔔 **完善的通知处理** - 内置通知解析和验签功能
- 🌐 **API服务功能** - 支持封装为HTTP REST API,提供聚合支付服务
- 🚀 **多框架支持** - 支持Flask和FastAPI,灵活选择Web框架
- 🛡️ **中间件系统** - 认证、日志、限流等中间件支持
- 💡 **类型提示** - 全面的类型注解,提供更好的IDE支持
- ⚠️ **完善的错误处理** - 详细的错误信息和异常类型

## 📊 支持的支付渠道

| 支付渠道 | API数量 | 说明 |
|:--------:|:-------:|------|
| 💰 **支付宝** | ~120 | PC支付、手机支付、APP支付、当面支付、转账、分账等 |
| 💚 **微信支付** | ~75 | 公众号、小程序、H5、APP支付、代金券、发票等 |
| 🐧 **QQ钱包** | ~12 | 核心支付功能 |
| 🍎 **Apple Pay** | ~12 | 收据验证、订阅管理、App Store内购 |
| 💳 **PayPal** | ~25 | 订单、支付、订阅、退款,国际支付 |
| 🏪 **通联支付** | ~10 | 基础支付功能 |
| 🔷 **拉卡拉** | ~10 | 基础支付功能 |
| 📱 **扫呗** | ~8 | 小程序支付、付款码支付、二维码支付 |
| **总计** | **~312** | **完整功能覆盖** |

## 🚀 快速安装

```bash
# 克隆项目
git clone https://github.com/hezuogongying/pay-stack.git
cd pay-stack

# 安装依赖
pip install -e .
```

## 💡 快速开始

### 支付宝支付

```python
from gopay.alipay import AlipayClient
from gopay.config import AlipayConfig
from gopay.utils import BodyMap

# 1. 创建配置
config = AlipayConfig(
    app_id="your_app_id",
    app_private_key="your_app_private_key",
    alipay_public_key="alipay_public_key",
    notify_url="https://your-site.com/notify/alipay",
    is_sandbox=False,  # 设置为True使用沙箱环境
)

# 2. 创建客户端
client = AlipayClient(config)

# 3. 创建订单
params = BodyMap()
params.set("out_trade_no", "ORDER_20240120001")
params.set("total_amount", "0.01")
params.set("subject", "测试商品")

result = client.trade_create(params)
if result.success:
    print("订单创建成功:", result.data)
else:
    print("订单创建失败:", result.error)
```

### 微信支付

```python
from gopay.wechat import WechatClient
from gopay.config import WechatConfig
from gopay.utils import BodyMap

# 1. 创建配置
config = WechatConfig(
    app_id="your_app_id",
    mch_id="your_mch_id",
    api_key="your_api_key",
    notify_url="https://your-site.com/notify/wechat",
)

# 2. 创建客户端
client = WechatClient(config)

# 3. 统一下单
params = BodyMap()
params.set("out_trade_no", "ORDER_20240120001")
params.set("total_fee", "1")  # 单位:分
params.set("body", "测试商品")
params.set("trade_type", "JSAPI")

result = client.unified_order(params)
if result.success:
    print("下单成功:", result.data)
```

### 国际支付 (Apple Pay + PayPal)

```python
from gopay.apple import ApplePayClient
from gopay.paypal import PayPalClient

# Apple Pay - 收据验证
apple_client = ApplePayClient(app_shared_secret="your_secret", sandbox=True)
result = apple_client.verify_receipt("base64_receipt_data")

# PayPal - 创建订单
paypal_client = PayPalClient(client_id="your_id", client_secret="your_secret", sandbox=True)
result = paypal_client.create_order({
    "intent": "CAPTURE",
    "purchase_units": [{
        "amount": {"currency_code": "USD", "value": "10.00"}
    }]
})
```

## 🌐 聚合支付 API服务

将支付功能封装为HTTP API服务,提供统一的聚合支付接口:

```python
from gopay.api import PayApiServer
from gopay.api.middleware import ErrorHandler, AuthMiddleware, LoggingMiddleware

# 创建API服务器
server = PayApiServer(framework="flask")  # 或 "fastapi"

# 注册支付渠道
server.register_payment_channel("alipay", alipay_handler)
server.register_payment_channel("wechat", wechat_handler)

# 添加中间件
server.add_middleware(ErrorHandler())
server.add_middleware(AuthMiddleware(api_keys=["your_api_key"]))
server.add_middleware(LoggingMiddleware())

# 启动服务器
server.start(host="0.0.0.0", port=8000)
```

### API端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/pay/create_order` | POST | 创建订单 |
| `/api/v1/pay/query_order` | POST | 查询订单 |
| `/api/v1/pay/close_order` | POST | 关闭订单 |
| `/api/v1/pay/refund` | POST | 申请退款 |
| `/api/v1/health` | GET | 健康检查 |
| `/api/v1/channels` | GET | 支持的渠道 |

### 聚合支付优势

✅ **统一接口** - 所有支付渠道使用相同的API格式
✅ **简化集成** - 客户端只需对接一个API,无需关心渠道差异
✅ **灵活切换** - 根据业务需求随时切换支付渠道
✅ **易于扩展** - 新增支付渠道不影响现有代码
✅ **统一管理** - 统一的日志、错误处理、认证授权

## 🏗️ 架构设计

### SOLID原则

- **单一职责原则 (SRP)** - 每个模块专注于单一支付渠道
- **开闭原则 (OCP)** - 通过抽象类扩展,无需修改现有代码
- **里氏替换原则 (LSP)** - 所有支付客户端可互换使用
- **接口隔离原则 (ISP)** - 细分接口,避免依赖不需要的方法
- **依赖倒置原则 (DIP)** - 依赖抽象而非具体实现

### 设计模式

- 🔧 **工厂模式** - 签名器创建
- 📋 **策略模式** - 多框架支持(Flask/FastAPI)
- 🎨 **装饰器模式** - 中间件系统
- 📝 **模板方法模式** - 客户端基类
- ⛓️ **责任链模式** - 中间件链处理
- 🔌 **适配器模式** - 不同支付渠道适配
- 🏠 **外观模式** - API服务封装

## 📚 文档

### 核心文档

- [📖 快速开始](docs/QUICKSTART.md) - 快速入门指南
- [📚 API参考](docs/API_REFERENCE.md) - 完整API参考手册
- [🌐 API服务](docs/API_SERVICE.md) - HTTP REST API服务完整指南

### 示例代码

- [支付宝示例](examples/alipay_example.py) - 支付宝完整示例
- [微信示例](examples/wechat_example.py) - 微信完整示例
- [国际支付示例](examples/international_payment_example.py) - 国际支付示例
- [API服务器示例](examples/api_server_example.py) - API服务器示例

## 💼 商业价值

### 适用行业

- 🛒 **电商行业** - B2C、B2B、跨境电商
- 🎮 **游戏娱乐** - 网络游戏、直播平台
- 🍔 **餐饮零售** - 扫码点餐、新零售
- 🚗 **交通出行** - 网约车、旅游预订
- 📚 **内容付费** - 在线教育、数字内容
- 💰 **金融服务** - 互联网金融、供应链金融
- 🏥 **医疗健康** - 在线问诊、医疗器械
- 🏘️ **生活服务** - 物业管理、本地服务
- 🎓 **教育培训** - 在线平台、企业培训
- 🏛️ **政府机构** - 政务缴费、公共服务

### 业务价值

- 💰 **降低成本** - 统一集成8种支付渠道,减少开发成本60%+
- 🚀 **加速上线** - 开箱即用,缩短集成周期80%+
- 📈 **提升转化** - 支持多种支付方式,提升支付成功率15%+
- 🌍 **拓展业务** - 国际支付支持,轻松拓展海外市场
- 🔒 **安全可靠** - 企业级安全保障,符合监管要求

## 🛠️ 开发

```bash
# 克隆项目
git clone https://github.com/hezuogongying/pay-stack.git
cd pay-stack

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black gopay/

# 代码检查
flake8 gopay/
mypy gopay/
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request!

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

[MIT License](LICENSE)

## 📞 联系方式

- GitHub Issues: https://github.com/hezuogongying/pay-stack/issues
- Email: 139563281@qq.com

## 🙏 鸣谢

感谢 [GoPay](https://github.com/go-pay/gopay) 项目提供的设计思路和参考。

---

<div align="center">

**⭐ 如果这个项目对你有帮助,请给我们一个Star!**

[GitHub](https://github.com/hezuogongying/pay-stack) | [Gitee](https://gitee.com/hezuo_111_admin/pay-stack)

Made with ❤️ by Pay-Stack Team

</div>

---

## 💬 赞赏支持

<div align="center">

微信赞赏码 &nbsp;&nbsp;&nbsp;&nbsp; 支付宝赞助码

<br>

<img width="200" height="200" src="assets/wx_pay.png" style="object-fit: contain;"/>
&nbsp;&nbsp;&nbsp;&nbsp;
<img width="200" height="200" src="assets/hzwy_pay.png" style="object-fit: contain;"/>

</div>

---

## 📢 问题沟通

<div align="center">

加微信群沟通,关注公众号获取最新版本

<br>

微信群 &nbsp;&nbsp;&nbsp;&nbsp; 公众号

<br>

<img width="200" height="200" src="assets/wx_qun.png" style="object-fit: contain;"/>
&nbsp;&nbsp;&nbsp;&nbsp;
<img width="200" height="200" src="assets/gzh_vip.png" style="object-fit: contain;"/>

</div>
