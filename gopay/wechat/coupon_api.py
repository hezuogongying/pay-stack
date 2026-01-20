"""
微信支付代金券API
包含代金券、商家券、满减券等功能
"""

import logging
from typing import Dict, Any
from gopay.utils.datastructure import BodyMap, ResponseData


logger = logging.getLogger(__name__)


class WechatCouponMixin:
    """
    微信支付代金券API Mixin类
    包含代金券、商家券等相关功能
    """

    def send_coupon(self, params: BodyMap) -> ResponseData:
        """
        发放代金券
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param params: 参数对象
        :return: 发放结果
        """
        params_dict = params.to_dict()

        # 必填参数检查
        required_fields = ["coupon_stock_id", "openid_count", "partner_trade_no"]
        for field in required_fields:
            if field not in params_dict:
                return ResponseData.error_response(
                    error=f"缺少必填参数: {field}",
                    code="MISSING_PARAMETER",
                )

        params_dict["mch_id"] = self.config.mch_id

        # 构建请求参数
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = f"{self.config.gateway_url}/mmpaymkttransfers/send_coupon"
        return self._do_request(url, request_params)

    def query_coupon_stock(self, params: BodyMap) -> ResponseData:
        """
        查询代金券批次
        :param params: 参数对象
        :return: 查询结果
        """
        params_dict = params.to_dict()

        # 必填参数检查
        if "coupon_stock_id" not in params_dict:
            return ResponseData.error_response(
                error="缺少必填参数: coupon_stock_id",
                code="MISSING_PARAMETER",
            )

        params_dict["mch_id"] = self.config.mch_id

        # 构建请求参数
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = f"{self.config.gateway_url}/mmpaymkttransfers/query_coupon_stock"
        return self._do_request(url, request_params)

    def query_coupon(self, params: BodyMap) -> ResponseData:
        """
        查询代金券信息
        :param params: 参数对象
        :return: 查询结果
        """
        params_dict = params.to_dict()

        # 必填参数检查
        required_fields = ["coupon_id", "openid", "stock_id"]
        for field in required_fields:
            if field not in params_dict:
                return ResponseData.error_response(
                    error=f"缺少必填参数: {field}",
                    code="MISSING_PARAMETER",
                )

        params_dict["mch_id"] = self.config.mch_id

        # 构建请求参数
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = f"{self.config.gateway_url}/mmpaymkttransfers/query_coupon"
        return self._do_request(url, request_params)

    # ==================== 商家券相关API ====================

    def create_busifavor(self, params: BodyMap) -> ResponseData:
        """
        创建商家券
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param params: 参数对象
        :return: 创建结果
        """
        params_dict = params.to_dict()

        # 必填参数检查
        required_fields = ["stock_type", "coupon_name", "belong_merchant", "available_merchants", "max_coupons", "no_cash", "description"]
        for field in required_fields:
            if field not in params_dict:
                return ResponseData.error_response(
                    error=f"缺少必填参数: {field}",
                    code="MISSING_PARAMETER",
                )

        params_dict["mchid"] = self.config.mch_id

        # 构建请求参数
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = f"{self.config.gateway_url}/v3/marketing/busifavor/stocks"
        return self._do_request(url, request_params)

    def query_busifavor(self, stock_id: str) -> ResponseData:
        """
        查询商家券详情
        :param stock_id: 批次ID
        :return: 查询结果
        """
        url = f"{self.config.gateway_url}/v3/marketing/busifavor/stocks/{stock_id}"
        return self._do_request(url, {})

    def modify_busifavor_budget(self, stock_id: str, params: BodyMap) -> ResponseData:
        """
        修改商家券预算
        :param stock_id: 批次ID
        :param params: 参数对象
        :return: 修改结果
        """
        params_dict = params.to_dict()

        url = f"{self.config.gateway_url}/v3/marketing/busifavor/stocks/{stock_id}/budget"
        return self._do_request(url, params_dict)

    def use_busifavor(self, params: BodyMap) -> ResponseData:
        """
        核销商家券
        :param params: 参数对象
        :return: 核销结果
        """
        params_dict = params.to_dict()

        # 必填参数检查
        required_fields = ["coupon_code", "stock_id", "appid"]
        for field in required_fields:
            if field not in params_dict:
                return ResponseData.error_response(
                    error=f"缺少必填参数: {field}",
                    code="MISSING_PARAMETER",
                )

        url = f"{self.config.gateway_url}/v3/marketing/busifavor/coupons/use"
        return self._do_request(url, params_dict)

    def return_busifavor(self, params: BodyMap) -> ResponseData:
        """
        退还商家券
        :param params: 参数对象
        :return: 退还结果
        """
        params_dict = params.to_dict()

        # 必填参数检查
        required_fields = ["coupon_code", "stock_id", "return_request_no"]
        for field in required_fields:
            if field not in params_dict:
                return ResponseData.error_response(
                    error=f"缺少必填参数: {field}",
                    code="MISSING_PARAMETER",
                )

        url = f"{self.config.gateway_url}/v3/marketing/busifavor/coupons/return"
        return self._do_request(url, params_dict)

    def deactivate_busifavor(self, stock_id: str, params: BodyMap) -> ResponseData:
        """
        使优惠券失效
        :param stock_id: 批次ID
        :param params: 参数对象
        :return: 失效结果
        """
        params_dict = params.to_dict()

        url = f"{self.config.gateway_url}/v3/marketing/busifavor/coupons/deactivate"
        return self._do_request(url, params_dict)

    def send_busifavor(self, params: BodyMap) -> ResponseData:
        """
        发放商家券
        :param params: 参数对象
        :return: 发放结果
        """
        params_dict = params.to_dict()

        # 必填参数检查
        required_fields = ["stock_id", "coupon_count"]
        for field in required_fields:
            if field not in params_dict:
                return ResponseData.error_response(
                    error=f"缺少必填参数: {field}",
                    code="MISSING_PARAMETER",
                )

        url = f"{self.config.gateway_url}/v3/marketing/busifavor/coupons/{params_dict['stock_id']}/send"
        return self._do_request(url, params_dict)

    def query_busifavor_users(self, stock_id: str, params: BodyMap) -> ResponseData:
        """
        查询商家券用户
        :param stock_id: 批次ID
        :param params: 参数对象
        :return: 查询结果
        """
        params_dict = params.to_dict()

        url = f"{self.config.gateway_url}/v3/marketing/busifavor/stocks/{stock_id}/users"
        return self._do_request(url, params_dict)


# 将 Mixin 的方法添加到 WechatClient 类
def inject_coupon_methods():
    """动态注入代金券API方法到 WechatClient"""
    from gopay.wechat.client import WechatClient

    for method_name in dir(WechatCouponMixin):
        if not method_name.startswith("_"):
            method = getattr(WechatCouponMixin, method_name)
            if callable(method):
                setattr(WechatClient, method_name, method)


# 自动注入
inject_coupon_methods()
