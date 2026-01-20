"""
Apple Pay 和 PayPal 使用示例
展示如何使用Apple Pay收据验证和PayPal支付功能
"""

import gopay
from gopay import ApplePayClient, ApplePayConfig, PayPalClient, PayPalConfig


# ==================== Apple Pay 示例 ====================

def apple_pay_example():
    """Apple Pay收据验证示例"""

    print("=" * 60)
    print("Apple Pay 示例")
    print("=" * 60)

    # 1. 创建配置(沙箱环境)
    config = ApplePayConfig(
        app_shared_secret="your_app_shared_secret",  # 可选,用于验证自动续期订阅
        sandbox=True,  # 使用沙箱环境
        timeout=30
    )

    # 2. 创建客户端
    client = ApplePayClient(config)

    # 3. 验证收据
    print("\n1. 验证收据:")
    receipt_data = "base64_encoded_receipt_data"
    result = client.verify_receipt(
        receipt_data=receipt_data,
        password=None,  # 如果已在配置中设置,可省略
        exclude_old_transactions=False
    )
    print(f"验证结果: {result}")

    # 4. 查询订单
    print("\n2. 查询订单:")
    order_id = "2000000123456789"
    result = client.look_up_order_id(order_id)
    print(f"订单信息: {result}")

    # 5. 获取订阅状态
    print("\n3. 获取订阅状态:")
    result = client.get_all_subscription_statuses(order_id)
    print(f"订阅状态: {result}")

    # 6. 获取交易历史
    print("\n4. 获取交易历史:")
    query_params = {
        "productId": "com.yourapp.product",
        "startDate": "2025-01-01",
        "endDate": "2025-01-31"
    }
    result = client.get_transaction_history_v2(query_params)
    print(f"交易历史: {result}")

    # 7. 获取退款历史
    print("\n5. 获取退款历史:")
    result = client.get_refund_history(query_params)
    print(f"退款历史: {result}")

    # 8. 解码通知负载
    print("\n6. 解码App Store通知:")
    signed_payload = "base64_signed_payload"
    result = client.decode_signed_payload(signed_payload)
    print(f"解码结果: {result}")

    # 9. 获取通知历史
    print("\n7. 获取通知历史:")
    notification_params = {
        "startDate": "2025-01-01",
        "endDate": "2025-01-31"
    }
    result = client.get_notification_history(notification_params)
    print(f"通知历史: {result}")

    print("\nApple Pay示例完成!")


# ==================== PayPal 示例 ====================

def paypal_example():
    """PayPal支付示例"""

    print("\n" + "=" * 60)
    print("PayPal 示例")
    print("=" * 60)

    # 1. 创建配置(沙箱环境)
    config = PayPalConfig(
        client_id="your_paypal_client_id",
        client_secret="your_paypal_client_secret",
        sandbox=True,  # 使用沙箱环境
        timeout=30
    )

    # 2. 创建客户端
    client = PayPalClient(config)

    # 3. 创建订单
    print("\n1. 创建订单:")
    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "reference_id": "PUHF",
            "amount": {
                "currency_code": "USD",
                "value": "100.00"
            }
        }],
        "application_context": {
            "brand_name": "EXAMPLE INC",
            "landing_page": "BILLING",
            "shipping_preference": "NO_SHIPPING",
            "user_action": "PAY_NOW"
        }
    }
    result = client.create_order(order_data)
    print(f"订单创建结果: {result}")

    # 4. 获取订单详情
    if result.code == "0" or result.code == "201":
        order_id = result.data.get("id", "ORDER_ID")
        print(f"\n2. 获取订单详情: {order_id}")
        result = client.get_order(order_id)
        print(f"订单详情: {result}")

        # 5. 捕获订单支付
        print(f"\n3. 捕获订单支付:")
        result = client.capture_order(order_id)
        print(f"捕获结果: {result}")

    # 6. 创建计费计划(订阅)
    print("\n4. 创建计费计划:")
    plan_data = {
        "product_id": "PROD-XXCD522942N",
        "name": "Basic Plan",
        "description": "Basic monthly plan",
        "status": "ACTIVE",
        "billing_cycles": [{
            "frequency": {
                "unit": "MONTH",
                "value": 1
            },
            "tenure_type": "REGULAR",
            "sequence": 1,
            "total_cycles": 12,
            "pricing_scheme": {
                "fixed_price": {
                    "value": "10.00",
                    "currency_code": "USD"
                }
            }
        }],
        "payment_preferences": {
            "auto_bill_outstanding": True,
            "payment_failure_threshold": 3
        }
    }
    result = client.create_plan(plan_data)
    print(f"计划创建结果: {result}")

    # 7. 创建订阅
    print("\n5. 创建订阅:")
    subscription_data = {
        "plan_id": "P-5ML48779G1586674SL3CWWDA",
        "application_context": {
            "brand_name": "EXAMPLE INC",
            "locale": "en-US",
            "shipping_preference": "NO_SHIPPING",
            "user_action": "SUBSCRIBE_NOW",
            "payment_method": {
                "payer_selected": "PAYPAL",
                "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
            },
            "return_url": "https://example.com/return",
            "cancel_url": "https://example.com/cancel"
        }
    }
    result = client.create_subscription(subscription_data)
    print(f"订阅创建结果: {result}")

    # 8. 退款
    print("\n6. 退款:")
    refund_data = {
        "amount": {
            "value": "10.00",
            "currency_code": "USD"
        },
        "note_to_payer": "Refund for order"
    }
    result = client.refund_payment(refund_data)
    print(f"退款结果: {result}")

    print("\nPayPal示例完成!")


# ==================== 对比示例 ====================

def comparison_example():
    """Apple Pay与PayPal对比示例"""

    print("\n" + "=" * 60)
    print("Apple Pay vs PayPal 对比")
    print("=" * 60)

    comparison = """
    Apple Pay (App Store):
    - 主要用于iOS应用内购买
    - 收据验证确保交易真实
    - 支持订阅管理
    - 适用于虚拟商品(应用、游戏、数字内容)

    PayPal:
    - 国际支付标准
    - 支持多种货币
    - 可用于实物和虚拟商品
    - 强大的订单和订阅管理
    - 全球用户覆盖广泛

    使用建议:
    - iOS应用内购买 → Apple Pay
    - 国际电商网站 → PayPal
    - 跨境支付 → PayPal
    - 订阅服务 → 两者都支持,根据目标用户选择
    """

    print(comparison)


# ==================== 主程序 ====================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("国际支付示例程序")
    print("=" * 60)

    # Apple Pay示例
    # apple_pay_example()

    # PayPal示例
    # paypal_example()

    # 对比说明
    comparison_example()

    print("\n" + "=" * 60)
    print("示例程序运行完成!")
    print("=" * 60)
