"""
高级API使用示例
展示补充的高级功能
"""

from gopay.alipay import AlipayClient
from gopay.wechat import WechatClient
from gopay.config import AlipayConfig, WechatConfig
from gopay.utils import BodyMap


def alipay_advanced_examples():
    """支付宝高级API示例"""
    print("=" * 60)
    print("支付宝高级API示例")
    print("=" * 60)
    print()

    # 初始化客户端
    config = AlipayConfig(
        app_id="your_app_id",
        app_private_key="your_private_key",
        alipay_public_key="alipay_public_key",
        is_sandbox=True,
    )
    client = AlipayClient(config)

    # 1. 当面支付
    print("1. 当面支付 (TradePay)")
    params = BodyMap()
    params.set("out_trade_no", "FACE_20240120001")
    params.set("total_amount", "0.01")
    params.set("subject", "当面付测试")
    params.set("auth_code", "289123456789012345")  # 用户的付款码
    params.set("scene", "bar_code")  # 条码支付

    result = client.trade_pay(params)
    print(f"当面付结果: {'成功' if result.success else '失败'}")
    if result.success:
        print(f"  交易号: {result.data.get('trade_no')}")
    print()

    # 2. 扫码支付
    print("2. 扫码支付 (TradePrecreate)")
    params = BodyMap()
    params.set("out_trade_no", "SCAN_20240120001")
    params.set("total_amount", "0.01")
    params.set("subject", "扫码支付测试")

    result = client.trade_precreate(params)
    print(f"扫码支付结果: {'成功' if result.success else '失败'}")
    if result.success:
        print(f"  二维码URL: {result.data.get('qr_code')}")
    print()

    # 3. 资金授权冻结
    print("3. 资金授权冻结")
    params = BodyMap()
    params.set("out_order_no", "AUTH_20240120001")
    params.set("auth_code", "289123456789012345")
    params.set("auth_amount", "0.01")
    params.set("payee_user_id", "2088100000000000")
    params.set("product_code", "PRE_AUTH_ONLINE_TRADE")

    result = client.fund_auth_order_freeze(params)
    print(f"授权冻结结果: {'成功' if result.success else '失败'}")
    if result.success:
        print(f"  授权单号: {result.data.get('auth_no')}")
    print()

    # 4. 单笔转账
    print("4. 单笔转账")
    params = BodyMap()
    params.set("out_biz_no", "TRANS_20240120001")
    params.set("payee_type", "ALIPAY_LOGON_ID")
    params.set("payee_account", "user@example.com")
    params.set("amount", "0.01")
    params.set("remark", "测试转账")

    result = client.fund_trans_uni_transfer(params)
    print(f"转账结果: {'成功' if result.success else '失败'}")
    if result.success:
        print(f"  转账单号: {result.data.get('order_id')}")
    print()

    # 5. 查询账户余额
    print("5. 查询账户余额")
    params = BodyMap()
    params.set("bill_type", "sign")  # sign:可用余额，basic:基本账户

    result = client.data_bill_balance_query(params)
    print(f"余额查询结果: {'成功' if result.success else '失败'}")
    if result.success:
        print(f"  可用余额: {result.data.get('available_amount')}")
    print()


def wechat_advanced_examples():
    """微信支付高级API示例"""
    print("=" * 60)
    print("微信支付高级API示例")
    print("=" * 60)
    print()

    # 初始化客户端
    config = WechatConfig(
        app_id="your_app_id",
        mch_id="your_mch_id",
        api_key="your_api_key",
    )
    client = WechatClient(config)

    # 1. 刷卡支付
    print("1. 刷卡支付 (Micropay)")
    params = BodyMap()
    params.set("body", "刷卡支付测试")
    params.set("out_trade_no", "MICRO_20240120001")
    params.set("total_fee", 1)  # 单位:分
    params.set("auth_code", "134567890123456789")  # 付款码
    params.set("spbill_create_ip", "127.0.0.1")

    result = client.micropay(params)
    print(f"刷卡支付结果: {'成功' if result.success else '失败'}")
    if result.success:
        print(f"  交易号: {result.data.get('transaction_id')}")
    print()

    # 2. 下载交易账单
    print("2. 下载交易账单")
    result = client.download_bill(
        bill_date="20240120",
        bill_type="ALL",  # ALL:所有订单, SUCCESS:成功订单, REFUND:退款订单
    )
    print(f"下载账单结果: {'成功' if result.success else '失败'}")
    if result.success:
        print(f"  账单数据长度: {len(result.data.get('data', ''))}")
    print()

    # 3. 商家转账
    print("3. 商家转账到零钱")
    params = BodyMap()
    params.set("partner_trade_no", "TRANS_20240120001")
    params.set("openid", "user_openid")
    params.set("amount", 1)  # 单位:分
    params.set("desc", "测试转账")
    params.set("spbill_create_ip", "127.0.0.1")
    params.set("check_name", "NO_CHECK")  # 不验证真实姓名

    result = client.transfer(params)
    print(f"转账结果: {'成功' if result.success else '失败'}")
    if result.success:
        print(f"  转账单号: {result.data.get('payment_no')}")
    print()

    # 4. 查询转账
    print("4. 查询转账")
    result = client.get_transfer_info("TRANS_20240120001")
    print(f"查询转账结果: {'成功' if result.success else '失败'}")
    if result.success:
        print(f"  转账状态: {result.data.get('status')}")
    print()

    # 5. 请求分账
    print("5. 请求分账")
    params = BodyMap()
    params.set("transaction_id", "wx_transaction_id")
    params.set("out_order_no", "PROFIT_20240120001")
    params.set("receivers", [
        {
            "type": "PERSONAL_OPENID",
            "receiver": "user_openid",
            "amount": 1,  # 单位:分
            "description": "分账给用户",
        }
    ])

    result = client.profit_sharing(params)
    print(f"分账结果: {'成功' if result.success else '失败'}")
    if result.success:
        print(f"  分账单号: {result.data.get('order_id')}")
    print()

    # 6. 添加分账接收方
    print("6. 添加分账接收方")
    params = BodyMap()
    params.set("receiver", {
        "type": "PERSONAL_OPENID",
        "account": "user_openid",
        "relation_name": "服务商",
        "custom_relation": "分销",
    })

    result = client.profit_sharing_add_receiver(params)
    print(f"添加接收方结果: {'成功' if result.success else '失败'}")
    print()

    # 7. 企业付款到银行卡
    print("7. 企业付款到银行卡")
    params = BodyMap()
    params.set("partner_trade_no", "BANK_20240120001")
    params.set("enc_bank_no", "encrypted_bank_no")  # 需要加密
    params.set("enc_true_name", "encrypted_real_name")  # 需要加密
    params.set("bank_code", "ICBC")  # 工商银行
    params.set("amount", 1)  # 单位:分
    params.set("desc", "测试付款到银行卡")

    result = client.pay_bank(params)
    print(f"付款到银行卡结果: {'成功' if result.success else '失败'}")
    if result.success:
        print(f"  付款单号: {result.data.get('payment_no')}")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("GoPay Python SDK - 高级API示例")
    print("=" * 60)
    print()

    print("注意: 以下为示例代码，实际使用时需要替换真实的配置信息")
    print()

    # 运行支付宝高级API示例
    try:
        alipay_advanced_examples()
    except Exception as e:
        print(f"支付宝高级API示例执行出错: {e}")

    print("\n")

    # 运行微信支付高级API示例
    try:
        wechat_advanced_examples()
    except Exception as e:
        print(f"微信支付高级API示例执行出错: {e}")

    print("=" * 60)
    print("示例执行完毕")
    print("=" * 60)
