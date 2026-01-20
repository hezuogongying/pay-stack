"""
微信其他高级API
包含合单支付、撤销、多次分账等
"""

import logging
from gopay.utils.datastructure import BodyMap, ResponseData


logger = logging.getLogger(__name__)


class WechatOtherAdvancedMixin:
    """微信高级功能 API Mixin类"""

    def reverse(self, params: BodyMap) -> ResponseData:
        """
        撤销订单
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html
        """
        params_dict = params.to_dict()
        request_params = self._build_common_params()
        request_params.update(params_dict)
        url = f"{self.config.gateway_url}/secapi/pay/reverse"
        return self._do_request(url, request_params)

    def combine(self, params: BodyMap) -> ResponseData:
        """
        合单支付
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html
        """
        params_dict = params.to_dict()
        request_params = self._build_common_params()
        request_params.update(params_dict)
        url = f"{self.config.gateway_url}/v3/combine-transactions/combine"
        return self._do_request(url, request_params)

    def combine_query(self, combine_out_trade_no: str) -> ResponseData:
        """
        查询合单订单
        """
        url = f"{self.config.gateway_url}/v3/combine-transactions/no-transactions/{combine_out_trade_no}"
        return self._do_request(url, {})

    def multi_profit_sharing(self, params: BodyMap) -> ResponseData:
        """
        请求多次分账
        """
        params_dict = params.to_dict()
        request_params = self._build_common_params()
        request_params.update(params_dict)
        url = f"{self.config.gateway_url}/v3/profitsharingorders/multi-orders"
        return self._do_request(url, request_params)

    def profit_sharing_split_by_buyer(self, params: BodyMap) -> ResponseData:
        """
        买家分账
        """
        params_dict = params.to_dict()
        request_params = self._build_common_params()
        request_params.update(params_dict)
        url = f"{self.config.gateway_url}/v3/profitsharingorders"
        return self._do_request(url, request_params)

    def profit_sharing_split_by_merchant(self, params: BodyMap) -> ResponseData:
        """
        商户分账
        """
        params_dict = params.to_dict()
        request_params = self._build_common_params()
        request_params.update(params_dict)
        url = f"{self.config.gateway_url}/v3/profitsharingorders"
        return self._do_request(url, request_params)

    def get_rsa_public_key(self, params: BodyMap) -> ResponseData:
        """
        获取RSA加密公钥
        """
        params_dict = params.to_dict()
        url = f"{self.config.gateway_url}/rssig/get"
        return self._do_request(url, params_dict)

    def report(self, params: BodyMap) -> ResponseData:
        """
        交易保障
        """
        params_dict = params.to_dict()
        request_params = self._build_common_params()
        request_params.update(params_dict)
        url = f"{self.config.gateway_url}/pay/report"
        return self._do_request(url, request_params)

    def download_fund_flow(self, params: BodyMap) -> ResponseData:
        """
        下载资金对账单
        补充之前的方法
        """
        params_dict = params.to_dict()
        request_params = self._build_common_params()
        request_params.update(params_dict)
        url = f"{self.config.gateway_url}/pay/downloadfundflow"
        return self._do_request(url, request_params)

    def batch_query_comment(self, params: BodyMap) -> ResponseData:
        """
        批量查询评价
        """
        params_dict = params.to_dict()
        request_params = self._build_common_params()
        request_params.update(params_dict)
        url = f"{self.config.gateway_url}/billcommentsp/batchquerycomment"
        return self._do_request(url, request_params)

    def query_exchange_rate(self, params: BodyMap) -> ResponseData:
        """
        查询汇率
        """
        params_dict = params.to_dict()
        url = f"{self.config.gateway_url}/pay/queryexchagerate"
        return self._do_request(url, params_dict)

    def get_sign_key(self, params: BodyMap) -> ResponseData:
        """
        获取签名密钥
        """
        params_dict = params.to_dict()
        url = f"{self.config.gateway_url}/rms/getsignkey"
        return self._do_request(url, params_dict)

    def risk_get_signkey(self, params: BodyMap) -> ResponseData:
        """
        获取商户RSA公钥
        """
        params_dict = params.to_dict()
        url = f"{self.config.gateway_url}/risk/getpublickey"
        return self._do_request(url, params_dict)

    def risk_manage(self, params: BodyMap) -> ResponseData:
        """
        风控管理
        """
        params_dict = params.to_dict()
        url = f"{self.config.gateway_url}/risk/getpost"
        return self._do_request(url, params_dict)


def inject_advanced_methods():
    from gopay.wechat.client import WechatClient
    for method_name in dir(WechatOtherAdvancedMixin):
        if not method_name.startswith("_"):
            method = getattr(WechatOtherAdvancedMixin, method_name)
            if callable(method):
                setattr(WechatClient, method_name, method)


inject_advanced_methods()
