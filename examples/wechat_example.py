"""
微信支付示例
演示如何使用微信支付SDK进行各种操作
"""

from gopay.wechat import WechatClient
from gopay.config import WechatConfig
from gopay.utils import BodyMap


def main():
    # ==================== 配置初始化 ====================
    print("1. 初始化微信支付配置...")

    config = WechatConfig(
        app_id="wx0000000000000000",  # 替换为你的应用ID
        mch_id="10000000",  # 替换为你的商户号
        api_key="your_api_key_32_characters_length",  # 替换为你的API密钥
        notify_url="https://your-site.com/notify/wechat",
        is_sandbox=False,
    )

    # 创建客户端
    client = WechatClient(config)
    print("✓ 客户端初始化成功\n")

    # ==================== 统一下单 - NATIVE支付 ====================
    print("2. 创建NATIVE支付订单...")

    result = client.unified_order(
        body="测试商品 - RTX 4090",
        out_trade_no="ORDER_20240120001",
        total_fee=1,  # 单位:分
        spbill_create_ip="127.0.0.1",
        trade_type="NATIVE",
        product_id="PROD_001",
    )

    if result.success:
        code_url = result.data.get("code_url")
        print(f"✓ NATIVE支付订单创建成功:")
        print(f"  二维码链接: {code_url}")
        print(f"  预支付交易会话: {result.data.get('prepay_id')}\n")
    else:
        print(f"✗ NATIVE支付订单创建失败: {result.error}\n")

    # ==================== 统一下单 - JSAPI支付 ====================
    print("3. 创建JSAPI支付订单...")

    result = client.unified_order(
        body="测试商品 - JSAPI",
        out_trade_no="ORDER_20240120002",
        total_fee=1,
        spbill_create_ip="127.0.0.1",
        trade_type="JSAPI",
        openid="user_openid",  # 用户在商户appid下的唯一标识
    )

    if result.success:
        prepay_id = result.data.get("prepay_id")
        print(f"✓ JSAPI支付订单创建成功:")
        print(f"  预支付交易会话: {prepay_id}\n")
    else:
        print(f"✗ JSAPI支付订单创建失败: {result.error}\n")

    # ==================== 统一下单 - APP支付 ====================
    print("4. 创建APP支付订单...")

    result = client.unified_order(
        body="测试商品 - APP",
        out_trade_no="ORDER_20240120003",
        total_fee=1,
        spbill_create_ip="127.0.0.1",
        trade_type="APP",
    )

    if result.success:
        prepay_id = result.data.get("prepay_id")
        print(f"✓ APP支付订单创建成功:")
        print(f"  预支付交易会话: {prepay_id}\n")
    else:
        print(f"✗ APP支付订单创建失败: {result.error}\n")

    # ==================== 统一下单 - H5支付 ====================
    print("5. 创建H5支付订单...")

    result = client.unified_order(
        body="测试商品 - H5",
        out_trade_no="ORDER_20240120004",
        total_fee=1,
        spbill_create_ip="127.0.0.1",
        trade_type="MWEB",
        scene_info={
            "h5_info": {
                "type": "Wap",
                "app_name": "测试商城",
                "package_name": "com.example.mall",
            }
        },
    )

    if result.success:
        mweb_url = result.data.get("mweb_url")
        print(f"✓ H5支付订单创建成功:")
        print(f"  支付链接: {mweb_url}\n")
    else:
        print(f"✗ H5支付订单创建失败: {result.error}\n")

    # ==================== 查询订单 ====================
    print("6. 查询订单...")

    result = client.order_query(out_trade_no="ORDER_20240120001")

    if result.success:
        print(f"✓ 订单查询成功:")
        print(f"  交易状态: {result.data.get('trade_state')}")
        print(f"  交易类型: {result.data.get('trade_type')}")
        print(f"  总金额: {result.data.get('total_fee')}分\n")
    else:
        print(f"✗ 订单查询失败: {result.error}\n")

    # ==================== 关闭订单 ====================
    print("7. 关闭订单...")

    result = client.close_order(out_trade_no="ORDER_20240120004")

    if result.success:
        print(f"✓ 订单关闭成功\n")
    else:
        print(f"✗ 订单关闭失败: {result.error}\n")

    # ==================== 申请退款 ====================
    print("8. 申请退款...")

    result = client.refund(
        out_trade_no="ORDER_20240120001",
        out_refund_no="REFUND_20240120001",
        total_fee=1,  # 订单总金额(分)
        refund_fee=1,  # 退款金额(分)
        refund_desc="测试退款",
    )

    if result.success:
        print(f"✓ 退款申请成功\n")
    else:
        print(f"✗ 退款申请失败: {result.error}\n")

    # ==================== 查询退款 ====================
    print("9. 查询退款...")

    result = client.refund_query(out_refund_no="REFUND_20240120001")

    if result.success:
        print(f"✓ 退款查询成功:")
        print(f"  退款状态: {result.data.get('refund_status')}")  # SUCCESS-退款成功,PROCESSING-退款处理中,FAILED-退款失败,CHANGE-退款异常
        print(f"  退款金额: {result.data.get('refund_fee')}分\n")
    else:
        print(f"✗ 退款查询失败: {result.error}\n")


if __name__ == "__main__":
    print("=" * 60)
    print("微信支付示例")
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
