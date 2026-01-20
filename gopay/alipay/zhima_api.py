"""
支付宝芝麻信用API
"""

import logging
from gopay.utils.datastructure import BodyMap, ResponseData


logger = logging.getLogger(__name__)


class AlipayZhimaMixin:
    """支付宝芝麻信用API Mixin类"""

    def zhima_credit_pe_zmgo_paysign_apply(self, params: BodyMap) -> ResponseData:
        """芝麻GO支付下单链路签约申请"""
        biz_content = params.to_dict()
        return self._do_request("zhima.credit.pe.zmgo.paysign.apply", biz_content)

    def zhima_credit_pe_zmgo_paysign_query(self, params: BodyMap) -> ResponseData:
        """芝麻GO支付下单链路签约查询"""
        biz_content = params.to_dict()
        return self._do_request("zhima.credit.pe.zmgo.paysign.query", biz_content)

    def zhima_credit_ep_scene_rating_initialize(self, params: BodyMap) -> ResponseData:
        """芝麻企业信用信用评估初始化"""
        biz_content = params.to_dict()
        return self._do_request("zhima.credit.ep.scene.rating.initialize", biz_content)

    def zhima_credit_ep_scene_fulfillment_sync(self, params: BodyMap) -> ResponseData:
        """信用服务履约同步"""
        biz_content = params.to_dict()
        return self._do_request("zhima.credit.ep.scene.fulfillment.sync", biz_content)

    def zhima_credit_ep_scene_agreement_use(self, params: BodyMap) -> ResponseData:
        """加入信用服务"""
        biz_content = params.to_dict()
        return self._do_request("zhima.credit.ep.scene.agreement.use", biz_content)

    def zhima_credit_ep_scene_agreement_unsign(self, params: BodyMap) -> ResponseData:
        """解除信用服务"""
        biz_content = params.to_dict()
        return self._do_request("zhima.credit.ep.scene.agreement.unsign", biz_content)

    def zhima_credit_ep_scene_query(self, params: BodyMap) -> ResponseData:
        """芝麻信用评分查询"""
        biz_content = params.to_dict()
        return self._do_request("zhima.credit.ep.scene.query", biz_content)

    def zhima_credit_ep_scene_risk_evaluation(self, params: BodyMap) -> ResponseData:
        """信用评估-风险评分"""
        biz_content = params.to_dict()
        return self._do_request("zhima.credit.ep.scene.risk.evaluation", biz_content)

    def zhima_credit_ep_scene_feedback(self, params: BodyMap) -> ResponseData:
        """信用服务反馈"""
        biz_content = params.to_dict()
        return self._do_request("zhima.credit.ep.scene.feedback", biz_content)

    def zhima_credit_credit_facade_create(self, params: BodyMap) -> ResponseData:
        """信用服务开通"""
        biz_content = params.to_dict()
        return self._do_request("zhima.credit.credit.facade.create", biz_content)

    def zhima_credit_credit_facade_query(self, params: BodyMap) -> ResponseData:
        """信用服务查询"""
        biz_content = params.to_dict()
        return self._do_request("zhima.credit.credit.facade.query", biz_content)

    def zhima_credit_credit_facade_brief_create(self, params: BodyMap) -> ResponseData:
        """信用服务快速开通"""
        biz_content = params.to_dict()
        return self._do_request("zhima.credit.credit.facade.brief.create", biz_content)


def inject_zhima_methods():
    from gopay.alipay.client import AlipayClient
    for method_name in dir(AlipayZhimaMixin):
        if not method_name.startswith("_"):
            method = getattr(AlipayZhimaMixin, method_name)
            if callable(method):
                setattr(AlipayClient, method_name, method)


inject_zhima_methods()
