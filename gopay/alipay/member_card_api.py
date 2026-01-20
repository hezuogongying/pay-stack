"""
支付宝营销和会员卡API
包含营销活动、会员卡管理等功能
"""

import logging
from typing import Dict, Any
from gopay.utils.datastructure import BodyMap, ResponseData


logger = logging.getLogger(__name__)


class AlipayMarketingAndCardMixin:
    """
    支付宝营销和会员卡API Mixin类
    """

    # ==================== 营销活动API ====================

    def open_app_qrcode_create(self, params: BodyMap) -> ResponseData:
        """
        小程序生成推广二维码接口
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.open.app.qrcode.create", biz_content)

    def open_app_mini_app_templatemessage_send(self, params: BodyMap) -> ResponseData:
        """
        小程序模板消息发送
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.open.app.mini.app.templatemessage.send", biz_content)

    def marketing_campaign_cash_create(self, params: BodyMap) -> ResponseData:
        """
        创建现金活动接口
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.marketing.campaign.cash.create", biz_content)

    def marketing_campaign_cash_trigger(self, params: BodyMap) -> ResponseData:
        """
        触发现金红包活动
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.marketing.campaign.cash.trigger", biz_content)

    def marketing_campaign_cash_status_modify(self, params: BodyMap) -> ResponseData:
        """
        更改现金活动状态接口
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.marketing.campaign.cash.status.modify", biz_content)

    def marketing_campaign_cash_event_trigger(self, params: BodyMap) -> ResponseData:
        """
        现金红包活动触发接口
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.marketing.campaign.cash.event.trigger", biz_content)

    def marketing_campaign_cash_list_query(self, params: BodyMap) -> ResponseData:
        """
        查询现金活动列表
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.marketing.campaign.cash.list.query", biz_content)

    def marketing_campaign_cash_detail_query(self, params: BodyMap) -> ResponseData:
        """
        查询现金活动详情
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.marketing.campaign.cash.detail.query", biz_content)

    def marketing_activity_discount_create(self, params: BodyMap) -> ResponseData:
        """
        创建优惠券活动
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.marketing.activity.discount.create", biz_content)

    def marketing_activity_discount_query(self, params: BodyMap) -> ResponseData:
        """
        查询优惠券活动
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.marketing.activity.discount.query", biz_content)

    def marketing_activity_discount_modify(self, params: BodyMap) -> ResponseData:
        """
        修改优惠券活动
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.marketing.activity.discount.modify", biz_content)

    def marketing_voucher_create(self, params: BodyMap) -> ResponseData:
        """
        创建商户券
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.marketing.voucher.create", biz_content)

    def marketing_voucher_query(self, params: BodyMap) -> ResponseData:
        """
        查询商户券
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.marketing.voucher.query", biz_content)

    def marketing_voucher_modify(self, params: BodyMap) -> ResponseData:
        """
        修改商户券
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.marketing.voucher.modify", biz_content)

    def marketing_voucher_send(self, params: BodyMap) -> ResponseData:
        """
        发放商户券
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.marketing.voucher.send", biz_content)

    def marketing_voucher_use(self, params: BodyMap) -> ResponseData:
        """
        核销商户券
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.marketing.voucher.use", biz_content)

    def marketing_voucher_refund(self, params: BodyMap) -> ResponseData:
        """
        退回商户券
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.marketing.voucher.refund", biz_content)

    # ==================== 会员卡API ====================

    def hzm_aft_user_sequence_add(self, params: BodyMap) -> ResponseData:
        """
        会员卡改签接口
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.hzm.aft.user.sequence.add", biz_content)

    def hzm_aft_user_sequence_query(self, params: BodyMap) -> ResponseData:
        """
        会员卡查询接口
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.hzm.aft.user.sequence.query", biz_content)

    def hzm_aft_user_sequence_del(self, params: BodyMap) -> ResponseData:
        """
        会员卡删除接口
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.hzm.aft.user.sequence.del", biz_content)

    def hzm_aft_user_card_update(self, params: BodyMap) -> ResponseData:
        """
        会员卡信息修改
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.hzm.aft.user.card.update", biz_content)

    def hzm_aft_user_card_query(self, params: BodyMap) -> ResponseData:
        """
        会员卡查询
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.hzm.aft.user.card.query", biz_content)

    def hzm_aft_lifecycle_draw(self, params: BodyMap) -> ResponseData:
        """
        根据用户领取模板生成会员卡卡号
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.hzm.aft.lifecycle.draw", biz_content)

    def hzm_aft_lifecycle_detail_query(self, params: BodyMap) -> ResponseData:
        """
        会员卡领卡详情查询
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.hzm.aft.lifecycle.detail.query", biz_content)

    def hzm_aft_lifecycle_template_modify(self, params: BodyMap) -> ResponseData:
        """
        会员卡充值模板修改
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.hzm.aft.lifecycle.template.modify", biz_content)

    def hzm_aft_lifecycle_template_query(self, params: BodyMap) -> ResponseData:
        """
        会员卡充值模板查询
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.hzm.aft.lifecycle.template.query", biz_content)

    def hzm_aft_lifecycle_template_add(self, params: BodyMap) -> ResponseData:
        """
        会员卡充值模板新增
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.hzm.aft.lifecycle.template.add", biz_content)


def inject_marketing_card_methods():
    from gopay.alipay.client import AlipayClient
    for method_name in dir(AlipayMarketingAndCardMixin):
        if not method_name.startswith("_"):
            method = getattr(AlipayMarketingAndCardMixin, method_name)
            if callable(method):
                setattr(AlipayClient, method_name, method)


inject_marketing_card_methods()
