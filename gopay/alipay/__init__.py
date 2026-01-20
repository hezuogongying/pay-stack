"""
支付宝支付模块
"""

from gopay.alipay.client import AlipayClient

# 自动注入所有扩展API
import gopay.alipay.advanced_api       # 高级支付API
import gopay.alipay.marketing_api       # 营销API
import gopay.alipay.user_api           # 用户授权API
import gopay.alipay.member_card_api    # 会员卡API
import gopay.alipay.zhima_api          # 芝麻信用API
import gopay.alipay.merchant_api       # 商户管理API

__all__ = ["AlipayClient"]
