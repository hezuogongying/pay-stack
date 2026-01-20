"""
微信支付模块
"""

from gopay.wechat.client import WechatClient

# 自动注入所有扩展API
import gopay.wechat.advanced_api       # 高级支付API
import gopay.wechat.coupon_api          # 代金券API
import gopay.wechat.invoice_api         # 发票API

__all__ = ["WechatClient"]
