"""
支付宝商户管理API
"""

import logging
from gopay.utils.datastructure import BodyMap, ResponseData


logger = logging.getLogger(__name__)


class AlipayMerchantMixin:
    """支付宝商户管理API Mixin类"""

    def ant_merchant_expand_indirect_zmgo_create(self, params: BodyMap) -> ResponseData:
        """芝麻GO创建商户"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.expand.indirect.zmgo.create", biz_content)

    def ant_merchant_expand_indirect_zmgo_query(self, params: BodyMap) -> ResponseData:
        """芝麻GO查询商户"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.expand.indirect.zmgo.query", biz_content)

    def ant_merchant_expand_indirect_zmgo_modify(self, params: BodyMap) -> ResponseData:
        """芝麻GO修改商户"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.expand.indirect.zmgo.modify", biz_content)

    def ant_merchant_expand_image_upload(self, params: BodyMap) -> ResponseData:
        """图片上传接口"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.expand.image.upload", biz_content)

    def ant_merchant_expand_shop_create(self, params: BodyMap) -> ResponseData:
        """创建门店接口"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.expand.shop.create", biz_content)

    def ant_merchant_expand_shop_query(self, params: BodyMap) -> ResponseData:
        """查询门店接口"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.expand.shop.query", biz_content)

    def ant_merchant_expand_shop_modify(self, params: BodyMap) -> ResponseData:
        """修改门店接口"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.expand.shop.modify", biz_content)

    def ant_merchant_expand_itemorder_create(self, params: BodyMap) -> ResponseData:
        """创建物品接口"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.expand.itemorder.create", biz_content)

    def ant_merchant_expand_itemorder_query(self, params: BodyMap) -> ResponseData:
        """查询物品接口"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.expand.itemorder.query", biz_content)

    def ant_merchant_expand_itemorder_modify(self, params: BodyMap) -> ResponseData:
        """修改物品接口"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.expand.itemorder.modify", biz_content)

    def ant_merchant_expand_order_settle(self, params: BodyMap) -> ResponseData:
        """物品结算接口"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.expand.order.settle", biz_content)

    def ant_merchant_expand_order_query(self, params: BodyMap) -> ResponseData:
        """物品订单查询接口"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.expand.order.query", biz_content)

    def ant_merchant_expand_transaction_query(self, params: BodyMap) -> ResponseData:
        """物品交易查询接口"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.expand.transaction.query", biz_content)

    def ant_merchant_expand_order_refund(self, params: BodyMap) -> ResponseData:
        """物品退款接口"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.expand.order.refund", biz_content)

    def ant_merchant_indirect_zmgo_queryorder(self, params: BodyMap) -> ResponseData:
        """芝麻GO查询订单"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.indirect.zmgo.queryorder", biz_content)

    def ant_merchant_indirect_zmgo_refund(self, params: BodyMap) -> ResponseData:
        """芝麻GO退款"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.indirect.zmgo.refund", biz_content)

    def ant_merchant_indirect_zmgo_querysettle(self, params: BodyMap) -> ResponseData:
        """芝麻GO查询结算"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.indirect.zmgo.querysettle", biz_content)

    def ant_merchant_indirect_zmgo_orderquery(self, params: BodyMap) -> ResponseData:
        """芝麻GO订单查询"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.indirect.zmgo.orderquery", biz_content)

    def ant_merchant_indirect_zmgo_quitsqrcode(self, params: BodyMap) -> ResponseData:
        """芝麻GO退出二维码"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.indirect.zmgo.quitsqrcode", biz_content)

    def ant_merchant_order_onsell_settle(self, params: BodyMap) -> ResponseData:
        """代售充值接口"""
        biz_content = params.to_dict()
        return self._do_request("ant.merchant.order.onsell.settle", biz_content)


def inject_merchant_methods():
    from gopay.alipay.client import AlipayClient
    for method_name in dir(AlipayMerchantMixin):
        if not method_name.startswith("_"):
            method = getattr(AlipayMerchantMixin, method_name)
            if callable(method):
                setattr(AlipayClient, method_name, method)


inject_merchant_methods()
