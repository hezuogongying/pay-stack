"""
微信支付发票API
包含电子发票开具、查询等功能
"""

import logging
from typing import Dict, Any
from gopay.utils.datastructure import BodyMap, ResponseData


logger = logging.getLogger(__name__)


class WechatInvoiceMixin:
    """
    微信支付发票API Mixin类
    包含电子发票相关功能
    """

    def create_invoice(self, params: BodyMap) -> ResponseData:
        """
        开具电子发票
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param params: 参数对象
        :return: 开票结果
        """
        params_dict = params.to_dict()

        # 必填参数检查
        required_fields = ["s_pappid", "order_id", "openid", "type", "payee", "detail", "amount"]
        for field in required_fields:
            if field not in params_dict:
                return ResponseData.error_response(
                    error=f"缺少必填参数: {field}",
                    code="MISSING_PARAMETER",
                )

        # 构建请求参数
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = f"{self.config.gateway_url}/v3/new-tax-control-invoice/fapiao/create"
        return self._do_request(url, request_params)

    def query_invoice(self, fapiao_id: str, params: BodyMap) -> ResponseData:
        """
        查询电子发票
        :param fapiao_id: 发票ID
        :param params: 参数对象
        :return: 查询结果
        """
        params_dict = params.to_dict()

        url = f"{self.config.gateway_url}/v3/new-tax-control-invoice/fapiao/query"
        return self._do_request(url, params_dict)

    def update_invoice(self, fapiao_id: str, params: BodyMap) -> ResponseData:
        """
        更新电子发票信息
        :param fapiao_id: 发票ID
        :param params: 参数对象
        :return: 更新结果
        """
        params_dict = params.to_dict()

        url = f"{self.config.gateway_url}/v3/new-tax-control-invoice/fapiao/update"
        return self._do_request(url, params_dict)

    def clear_invoice(self, fapiao_id: str) -> ResponseData:
        """
        冲红电子发票
        :param fapiao_id: 发票ID
        :return: 冲红结果
        """
        params = {"fapiao_id": fapiao_id}

        url = f"{self.config.gateway_url}/v3/new-tax-control-invoice/fapiao/clear"
        return self._do_request(url, params)

    def get_invoice_config(self, params: BodyMap) -> ResponseData:
        """
        查询发票配置
        :param params: 参数对象
        :return: 查询结果
        """
        params_dict = params.to_dict()

        url = f"{self.config.gateway_url}/v3/new-tax-control-invoice/user/title"
        return self._do_request(url, params_dict)

    def set_invoice_config(self, params: BodyMap) -> ResponseData:
        """
        设置发票配置
        :param params: 参数对象
        :return: 设置结果
        """
        params_dict = params.to_dict()

        # 必填参数检查
        required_fields = ["s_pappid", "openid", "title", "phone"]
        for field in required_fields:
            if field not in params_dict:
                return ResponseData.error_response(
                    error=f"缺少必填参数: {field}",
                    code="MISSING_PARAMETER",
                )

        url = f"{self.config.gateway_url}/v3/new-tax-control-invoice/user/title"
        return self._do_request(url, params_dict)

    def get_invoice_info(self, params: BodyMap) -> ResponseData:
        """
        查询个人发票信息
        :param params: 参数对象
        :return: 查询结果
        """
        params_dict = params.to_dict()

        url = f"{self.config.gateway_url}/v3/new-tax-control-invoice/fapiao/buyer/query"
        return self._do_request(url, params_dict)

    def reject_invoice(self, fapiao_id: str, params: BodyMap) -> ResponseData:
        """
        拒绝开具发票
        :param fapiao_id: 发票ID
        :param params: 参数对象
        :return: 拒绝结果
        """
        params_dict = params.to_dict()

        url = f"{self.config.gateway_url}/v3/new-tax-control-invoice/fapiao/reject"
        return self._do_request(url, params_dict)

    def make_out_invoice(self, params: BodyMap) -> ResponseData:
        """
        制作电子发票(预览)
        :param params: 参数对象
        :return: 制作结果
        """
        params_dict = params.to_dict()

        url = f"{self.config.gateway_url}/v3/new-tax-control-invoice/fapiao/preview"
        return self._do_request(url, params_dict)

    def query_mch_tax(self, params: BodyMap) -> ResponseData:
        """
        查询商户税号
        :param params: 参数对象
        :return: 查询结果
        """
        params_dict = params.to_dict()

        url = f"{self.config.gateway_url}/v3/new-tax-control-invoice/mch/query"
        return self._do_request(url, params_dict)

    def get_mch_tax(self, params: BodyMap) -> ResponseData:
        """
        获取商户税号信息
        :param params: 参数对象
        :return: 获取结果
        """
        params_dict = params.to_dict()

        url = f"{self.config.gateway_url}/v3/new-tax-control-invoice/mch/get"
        return self._do_request(url, params_dict)


# 将 Mixin 的方法添加到 WechatClient 类
def inject_invoice_methods():
    """动态注入发票API方法到 WechatClient"""
    from gopay.wechat.client import WechatClient

    for method_name in dir(WechatInvoiceMixin):
        if not method_name.startswith("_"):
            method = getattr(WechatInvoiceMixin, method_name)
            if callable(method):
                setattr(WechatClient, method_name, method)


# 自动注入
inject_invoice_methods()
