"""
支付宝支付示例
演示如何使用支付宝SDK进行各种操作
"""

from gopay.alipay import AlipayClient
from gopay.config import AlipayConfig
from gopay.utils import BodyMap


def main():
    # ==================== 配置初始化 ====================
    print("1. 初始化支付宝配置...")

    # 从字典创建配置
    config_dict = {
        "app_id": "2021000000000000",  # 替换为你的应用ID
        "app_private_key": """-----BEGIN RSA PRIVATE KEY-----
        你的应用私钥
        -----END RSA PRIVATE KEY-----""",
        "alipay_public_key": """-----BEGIN PUBLIC KEY-----
        支付宝公钥
        -----END PUBLIC KEY-----""",
        "notify_url": "https://your-site.com/notify/alipay",
        "return_url": "https://your-site.com/return/alipay",
        "is_sandbox": True,  # 使用沙箱环境测试
    }

    config = AlipayConfig(**config_dict)

    # 创建客户端
    client = AlipayClient(config)
    print("✓ 客户端初始化成功\n")

    # ==================== PC网站支付 ====================
    print("2. 创建PC网站支付订单...")

    params = BodyMap()
    params.set("out_trade_no", "ORDER_20240120001")  # 商户订单号
    params.set("total_amount", "0.01")  # 订单金额
    params.set("subject", "测试商品 - 高端显卡")  # 订单标题
    params.set("body", "RTX 4090 Ti x 2")  # 订单描述

    result = client.trade_page_pay(params)

    if result.success:
        pay_url = result.data["pay_url"]
        print(f"✓ 支付链接生成成功:")
        print(f"  {pay_url}\n")
    else:
        print(f"✗ 支付链接生成失败: {result.error}\n")

    # ==================== 手机网站支付 ====================
    print("3. 创建手机网站支付订单...")

    params = BodyMap()
    params.set("out_trade_no", "ORDER_20240120002")
    params.set("total_amount", "0.01")
    params.set("subject", "测试商品 - 手机端")
    params.set("quit_url", "https://your-site.com/quit")

    result = client.trade_wap_pay(params)

    if result.success:
        pay_url = result.data["pay_url"]
        print(f"✓ H5支付链接生成成功:")
        print(f"  {pay_url}\n")
    else:
        print(f"✗ H5支付链接生成失败: {result.error}\n")

    # ==================== APP支付 ====================
    print("4. 创建APP支付订单...")

    params = BodyMap()
    params.set("out_trade_no", "ORDER_20240120003")
    params.set("total_amount", "0.01")
    params.set("subject", "测试商品 - APP端")

    result = client.trade_app_pay(params)

    if result.success:
        order_string = result.data["order_string"]
        print(f"✓ APP支付订单字符串生成成功:")
        print(f"  {order_string[:50]}...\n")
    else:
        print(f"✗ APP支付订单生成失败: {result.error}\n")

    # ==================== 交易创建 ====================
    print("5. 创建交易...")

    params = BodyMap()
    params.set("out_trade_no", "ORDER_20240120004")
    params.set("total_amount", "0.01")
    params.set("subject", "测试商品")
    params.set("buyer_id", "2088100000000000")  # 买家支付宝用户ID

    result = client.trade_create(params)

    if result.success:
        print(f"✓ 交易创建成功:")
        print(f"  交易号: {result.data.get('trade_no')}\n")
    else:
        print(f"✗ 交易创建失败: {result.error}\n")

    # ==================== 查询订单 ====================
    print("6. 查询订单...")

    result = client.trade_query(out_trade_no="ORDER_20240120001")

    if result.success:
        print(f"✓ 订单查询成功:")
        print(f"  交易状态: {result.data.get('trade_status')}")
        print(f"  买家账号: {result.data.get('buyer_logon_id')}\n")
    else:
        print(f"✗ 订单查询失败: {result.error}\n")

    # ==================== 关闭订单 ====================
    print("7. 关闭订单...")

    result = client.trade_close(out_trade_no="ORDER_20240120004")

    if result.success:
        print(f"✓ 订单关闭成功\n")
    else:
        print(f"✗ 订单关闭失败: {result.error}\n")

    # ==================== 申请退款 ====================
    print("8. 申请退款...")

    result = client.trade_refund(
        refund_amount=0.01,
        out_trade_no="ORDER_20240120001",
        out_request_no="REFUND_20240120001",
        refund_reason="测试退款",
    )

    if result.success:
        print(f"✓ 退款申请成功\n")
    else:
        print(f"✗ 退款申请失败: {result.error}\n")

    # ==================== 查询退款 ====================
    print("9. 查询退款...")

    result = client.trade_fastpay_refund_query(
        out_trade_no="ORDER_20240120001",
        out_request_no="REFUND_20240120001",
    )

    if result.success:
        print(f"✓ 退款查询成功:")
        print(f"  退款状态: {result.data.get('refund_status')}\n")
    else:
        print(f"✗ 退款查询失败: {result.error}\n")

    # ==================== 撤销交易 ====================
    print("10. 撤销交易...")

    result = client.trade_cancel(out_trade_no="ORDER_20240120004")

    if result.success:
        print(f"✓ 交易撤销成功:")
        print(f"  撤销状态: {result.data.get('retry_flag')}\n")
    else:
        print(f"✗ 交易撤销失败: {result.error}\n")


if __name__ == "__main__":
    print("=" * 60)
    print("支付宝支付示例")
    print("=" * 60)
    print()

    try:
        main()
    except Exception as e:
        print(f"✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()

    print("=" * 60)
    print("示例执行完毕")
    print("=" * 60)
