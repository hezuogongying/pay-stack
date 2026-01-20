"""
其他支付方式示例
演示通联支付和拉卡拉支付的使用
"""

from gopay.allinpay import AllinPayClient, AllinPayConfig
from gopay.lakala import LakalaClient, LakalaConfig
from gopay.utils import BodyMap


def allinpay_example():
    """通联支付示例"""
    print("=" * 60)
    print("通联支付示例")
    print("=" * 60)
    print()

    # 1. 创建配置
    config = AllinPayConfig(
        app_id="your_app_id",
        merchant_id="your_merchant_id",
        api_key="your_api_key",
        notify_url="https://your-site.com/notify/allinpay",
    )

    # 2. 创建客户端
    client = AllinPayClient(config)
    print("✓ 客户端初始化成功\n")

    # 3. 创建订单
    print("3. 创建订单...")
    params = BodyMap()
    params.set("orderid", "ORDER_20240120001")
    params.set("amount", "0.01")
    params.set("productname", "测试商品")

    result = client.create_order(params)
    if result.success:
        print(f"✓ 订单创建成功: {result.data}\n")
    else:
        print(f"✗ 订单创建失败: {result.error}\n")

    # 4. 查询订单
    print("4. 查询订单...")
    result = client.query_order("ORDER_20240120001")
    if result.success:
        print(f"✓ 订单查询成功: {result.data}\n")
    else:
        print(f"✗ 订单查询失败: {result.error}\n")

    # 5. 申请退款
    print("5. 申请退款...")
    result = client.refund(
        order_no="ORDER_20240120001",
        refund_amount=0.01,
        refund_no="REFUND_20240120001",
    )
    if result.success:
        print(f"✓ 退款申请成功\n")
    else:
        print(f"✗ 退款申请失败: {result.error}\n")


def lakala_example():
    """拉卡拉支付示例"""
    print("=" * 60)
    print("拉卡拉支付示例")
    print("=" * 60)
    print()

    # 1. 创建配置
    config = LakalaConfig(
        app_id="your_app_id",
        mch_id="your_mch_id",
        terminal_id="your_terminal_id",
        api_key="your_api_key",
        notify_url="https://your-site.com/notify/lakala",
    )

    # 2. 创建客户端
    client = LakalaClient(config)
    print("✓ 客户端初始化成功\n")

    # 3. 创建订单
    print("3. 创建订单...")
    params = BodyMap()
    params.set("order_no", "ORDER_20240120002")
    params.set("total_amount", "0.01")
    params.set("subject", "测试商品")
    params.set("body", "拉卡拉测试商品")

    result = client.create_order(params)
    if result.success:
        print(f"✓ 订单创建成功: {result.data}\n")
    else:
        print(f"✗ 订单创建失败: {result.error}\n")

    # 4. 查询订单
    print("4. 查询订单...")
    result = client.query_order("ORDER_20240120002")
    if result.success:
        print(f"✓ 订单查询成功: {result.data}\n")
    else:
        print(f"✗ 订单查询失败: {result.error}\n")

    # 5. 申请退款
    print("5. 申请退款...")
    result = client.refund(
        order_no="ORDER_20240120002",
        refund_amount=0.01,
        refund_no="REFUND_20240120002",
    )
    if result.success:
        print(f"✓ 退款申请成功\n")
    else:
        print(f"✗ 退款申请失败: {result.error}\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("GoPay Python SDK - 其他支付方式示例")
    print("=" * 60)
    print()

    print("注意: 以下为示例代码，实际使用时需要替换真实的配置信息")
    print()

    # 运行通联支付示例
    try:
        allinpay_example()
    except Exception as e:
        print(f"通联支付示例执行出错: {e}")
        import traceback
        traceback.print_exc()

    print("\n")

    # 运行拉卡拉支付示例
    try:
        lakala_example()
    except Exception as e:
        print(f"拉卡拉支付示例执行出错: {e}")
        import traceback
        traceback.print_exc()

    print("=" * 60)
    print("示例执行完毕")
    print("=" * 60)
