"""
扫呗支付使用示例
展示如何使用扫呗支付的各种支付方式
"""

import gopay
from gopay import SaobeiClient, SaobeiConfig
from gopay.utils.datastructure import BodyMap


def saobei_example():
    """扫呗支付完整示例"""

    print("=" * 60)
    print("扫呗支付示例")
    print("=" * 60)

    # 1. 创建配置
    config = SaobeiConfig(
        merchant_id="your_merchant_id",  # 商户号
        terminal_id="your_terminal_id",  # 终端号
        key="your_merchant_key",  # 商户密钥
        gateway_url="https://pay.so-pay.cn",  # 支付网关
        timeout=30
    )

    # 2. 创建客户端
    client = SaobeiClient(config)

    # 3. 小程序支付
    print("\n1. 小程序支付:")
    params = BodyMap() \
        .put("out_trade_no", "ORDER" + str(int(__import__("time").time()))) \
        .put("total_fee", 100) \
        .put("body", "测试商品") \
        .put("openid", "user_openid") \
        .put("type", "wxpay")  # wxpay=微信, alipay=支付宝

    result = client.mini_pay(params)
    print(f"支付结果: {result}")

    # 4. 付款码支付(线下POS场景)
    print("\n2. 付款码支付(刷卡支付):")
    params = BodyMap() \
        .put("out_trade_no", "ORDER" + str(int(__import__("time").time()))) \
        .put("total_fee", 100) \
        .put("body", "测试商品") \
        .put("auth_code", "134567890123456789") \
        .put("type", "wxpay")

    result = client.barcode_pay(params)
    print(f"支付结果: {result}")

    # 5. 生成支付二维码
    print("\n3. 生成支付二维码:")
    params = BodyMap() \
        .put("out_trade_no", "ORDER" + str(int(__import__("time").time()))) \
        .put("total_fee", 100) \
        .put("body", "测试商品") \
        .put("type", "wxpay")

    result = client.get_pay_qrcode(params)
    print(f"二维码数据: {result}")

    # 6. 查询订单
    print("\n4. 查询订单:")
    params = BodyMap().put("out_trade_no", "ORDER123456")
    result = client.query(params)
    print(f"查询结果: {result}")

    # 7. 申请退款
    print("\n5. 申请退款:")
    params = BodyMap() \
        .put("out_trade_no", "ORDER123456") \
        .put("out_refund_no", "REFUND" + str(int(__import__("time").time()))) \
        .put("refund_fee", 50) \
        .put("total_fee", 100) \
        .put("type", "wxpay")

    result = client.refund(params)
    print(f"退款结果: {result}")

    # 8. 退款查询
    print("\n6. 退款查询:")
    params = BodyMap().put("out_refund_no", "REFUND123456")
    result = client.query_refund(params)
    print(f"退款查询结果: {result}")

    # 9. 关闭订单
    print("\n7. 关闭订单:")
    params = BodyMap() \
        .put("out_trade_no", "ORDER123456") \
        .put("type", "wxpay")

    result = client.close_order(params)
    print(f"关闭结果: {result}")

    # 10. 撤销订单
    print("\n8. 撤销订单:")
    params = BodyMap() \
        .put("out_trade_no", "ORDER123456") \
        .put("type", "wxpay")

    result = client.cancel_order(params)
    print(f"撤销结果: {result}")

    print("\n扫呗支付示例完成!")


def payment_type_comparison():
    """支付类型对比"""

    print("\n" + "=" * 60)
    print("扫呗支付类型说明")
    print("=" * 60)

    comparison = """
    扫呗支持的支付类型(type参数):

    1. 微信支付 (wxpay):
       - 小程序支付: mini_pay()
       - 付款码支付: barcode_pay()
       - 二维码支付: get_pay_qrcode()

    2. 支付宝 (alipay):
       - 小程序支付: mini_pay()
       - 付款码支付: barcode_pay()
       - 二维码支付: get_pay_qrcode()

    使用场景:
    - 小程序支付: 适用于微信小程序、支付宝小程序
    - 付款码支付: 适用于线下POS机扫码
    - 二维码支付: 适用于生成二维码供用户扫码

    注意事项:
    1. 金额单位为分,100分=1元
    2. 订单号需要保证唯一性
    3. 商户号和终端号需要向扫呗申请
    4. 生产环境和沙箱环境使用不同的网关地址
    """

    print(comparison)


def best_practices():
    """最佳实践"""

    print("\n" + "=" * 60)
    print("扫呗支付最佳实践")
    print("=" * 60)

    practices = """
    1. 订单号生成:
       - 使用时间戳 + 随机数保证唯一性
       - 建议格式: 商户前缀 + 时间戳 + 随机数
       - 示例: "M20250120143025123456"

    2. 金额处理:
       - 金额单位为分,需要转换
       - 示例: 100元 = 100分
       - 注意浮点数精度问题,建议使用整数

    3. 错误处理:
       - 检查返回的code字段
       - code="0"表示成功
       - 记录错误日志以便排查问题

    4. 异步通知:
       - 配置异步通知URL
       - 验证通知签名确保通知真实性
       - 处理重复通知(幂等性设计)

    5. 安全建议:
       - 商户密钥不要硬编码在代码中
       - 使用环境变量或配置文件
       - 定期更换密钥
       - 使用HTTPS通信

    6. 测试建议:
       - 先在沙箱环境测试
       - 测试各种场景:成功、失败、退款等
       - 使用小额金额测试
       - 验证异步通知处理逻辑
    """

    print(practices)


# ==================== 主程序 ====================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("扫呗支付示例程序")
    print("=" * 60)

    # 完整支付流程示例
    # saobei_example()

    # 支付类型说明
    payment_type_comparison()

    # 最佳实践
    best_practices()

    print("\n" + "=" * 60)
    print("示例程序运行完成!")
    print("=" * 60)
