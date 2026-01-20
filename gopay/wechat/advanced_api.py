"""
微信支付高级API
补充缺失的支付功能
"""

import logging
from typing import Optional, Dict, Any

from gopay.utils.datastructure import BodyMap, XmlMap, ResponseData


logger = logging.getLogger(__name__)


class WechatAdvancedMixin:
    """
    微信支付高级API Mixin类
    包含刷卡支付、转账、分账等高级功能
    """

    def micropay(self, params: BodyMap) -> ResponseData:
        """
        刷卡支付/付款码支付
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param params: 参数对象
        :return: 支付结果
        """
        params_dict = params.to_dict()

        # 必填参数检查
        required_fields = ["body", "out_trade_no", "total_fee", "auth_code", "spbill_create_ip"]
        for field in required_fields:
            if field not in params_dict:
                return ResponseData.error_response(
                    error=f"缺少必填参数: {field}",
                    code="MISSING_PARAMETER",
                )

        # 构建请求参数
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = f"{self.config.gateway_url}/pay/micropay"
        return self._do_request(url, request_params)

    def download_bill(self, bill_date: str, bill_type: str = "ALL", **kwargs) -> ResponseData:
        """
        下载交易账单
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param bill_date: 账单日期，格式：yyyyMMdd
        :param bill_type: 账单类型，ALL/SUCCESS/REFUND/RECHARGE_REFUND
        :param kwargs: 其他参数
        :return: 账单数据
        """
        params = self._build_common_params()
        params.update({
            "bill_date": bill_date,
            "bill_type": bill_type,
        })
        params.update(kwargs)

        url = f"{self.config.gateway_url}/pay/downloadbill"
        return self._do_request(url, params)

    def download_fund_flow(self, bill_date: str, account_type: str = "Basic", **kwargs) -> ResponseData:
        """
        下载资金账单
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param bill_date: 账单日期，格式：yyyyMMdd
        :param account_type: 账单类型，Basic/Operation/Fee
        :param kwargs: 其他参数
        :return: 资金流水
        """
        params = self._build_common_params()
        params.update({
            "bill_date": bill_date,
            "account_type": account_type,
        })
        params.update(kwargs)

        url = f"{self.config.gateway_url}/pay/downloadfundflow"
        return self._do_request(url, params)

    def transfer(self, params: BodyMap) -> ResponseData:
        """
        商家转账
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param params: 参数对象
        :return: 转账结果
        """
        params_dict = params.to_dict()

        # 必填参数检查
        required_fields = ["partner_trade_no", "openid", "amount", "desc"]
        for field in required_fields:
            if field not in params_dict:
                return ResponseData.error_response(
                    error=f"缺少必填参数: {field}",
                    code="MISSING_PARAMETER",
                )

        params_dict["mchid"] = self.config.mch_id
        params_dict["mch_appid"] = self.config.app_id

        # 构建请求参数
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = f"{self.config.gateway_url}/mmpaymkttransfers/promotion/transfers"
        return self._do_request(url, request_params)

    def get_transfer_info(self, partner_trade_no: str) -> ResponseData:
        """
        查询商家转账
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param partner_trade_no: 商户转账单号
        :return: 转账信息
        """
        params = self._build_common_params()
        params.update({
            "partner_trade_no": partner_trade_no,
        })

        url = f"{self.config.gateway_url}/mmpaymkttransfers/gettransferinfo"
        return self._do_request(url, params)

    def pay_bank(self, params: BodyMap) -> ResponseData:
        """
        企业付款到银行卡
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param params: 参数对象
        :return: 付款结果
        """
        params_dict = params.to_dict()

        # 必填参数检查
        required_fields = ["partner_trade_no", "enc_bank_no", "enc_true_name", "bank_code", "amount"]
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

        url = f"{self.config.gateway_url}/mmpaysptrans/pay_bank"
        return self._do_request(url, request_params)

    def query_bank(self, partner_trade_no: str) -> ResponseData:
        """
        查询付款到银行卡
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param partner_trade_no: 商户转账单号
        :return: 付款信息
        """
        params = self._build_common_params()
        params.update({
            "partner_trade_no": partner_trade_no,
        })

        url = f"{self.config.gateway_url}/mmpaysptrans/query_bank"
        return self._do_request(url, params)

    def profit_sharing(self, params: BodyMap) -> ResponseData:
        """
        请求分账
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param params: 参数对象
        :return: 分账结果
        """
        params_dict = params.to_dict()

        # 必填参数检查
        required_fields = ["transaction_id", "out_order_no", "receivers"]
        for field in required_fields:
            if field not in params_dict:
                return ResponseData.error_response(
                    error=f"缺少必填参数: {field}",
                    code="MISSING_PARAMETER",
                )

        params_dict["mch_id"] = self.config.mch_id
        params_dict["appid"] = self.config.app_id

        # 构建请求参数
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = f"{self.config.gateway_url}/secapi/pay/profitsharing"
        return self._do_request(url, request_params)

    def profit_sharing_query(self, transaction_id: str, out_order_no: str) -> ResponseData:
        """
        查询分账
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param transaction_id: 微信订单号
        :param out_order_no: 商户分账单号
        :return: 分账信息
        """
        params = self._build_common_params()
        params.update({
            "transaction_id": transaction_id,
            "out_order_no": out_order_no,
        })

        url = f"{self.config.gateway_url}/pay/profitsharingquery"
        return self._do_request(url, params)

    def profit_sharing_add_receiver(self, params: BodyMap) -> ResponseData:
        """
        添加分账接收方
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param params: 参数对象
        :return: 添加结果
        """
        params_dict = params.to_dict()

        # 必填参数检查
        if "receiver" not in params_dict:
            return ResponseData.error_response(
                error="缺少必填参数: receiver",
                code="MISSING_PARAMETER",
            )

        params_dict["mch_id"] = self.config.mch_id
        params_dict["appid"] = self.config.app_id

        # 构建请求参数
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = f"{self.config.gateway_url}/pay/profitsharingaddreceiver"
        return self._do_request(url, request_params)

    def profit_sharing_remove_receiver(self, params: BodyMap) -> ResponseData:
        """
        删除分账接收方
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param params: 参数对象
        :return: 删除结果
        """
        params_dict = params.to_dict()

        # 必填参数检查
        if "receiver" not in params_dict:
            return ResponseData.error_response(
                error="缺少必填参数: receiver",
                code="MISSING_PARAMETER",
            )

        params_dict["mch_id"] = self.config.mch_id
        params_dict["appid"] = self.config.app_id

        # 构建请求参数
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = f"{self.config.gateway_url}/pay/profitsharingremovereceiver"
        return self._do_request(url, request_params)

    def profit_sharing_finish(self, params: BodyMap) -> ResponseData:
        """
        完结分账
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param params: 参数对象
        :return: 完结结果
        """
        params_dict = params.to_dict()

        # 必填参数检查
        required_fields = ["transaction_id", "out_order_no", "description"]
        for field in required_fields:
            if field not in params_dict:
                return ResponseData.error_response(
                    error=f"缺少必填参数: {field}",
                    code="MISSING_PARAMETER",
                )

        params_dict["mch_id"] = self.config.mch_id
        params_dict["appid"] = self.config.app_id

        # 构建请求参数
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = f"{self.config.gateway_url}/secapi/pay/profitsharingfinish"
        return self._do_request(url, request_params)

    def batch_query_comment(self, params: BodyMap) -> ResponseData:
        """
        批量查询评价
        文档: https://pay.weixin.qq.com/wiki/doc/api/index.html

        :param params: 参数对象
        :return: 评价列表
        """
        params_dict = params.to_dict()

        # 必填参数检查
        if "begin_time" not in params_dict or "end_time" not in params_dict:
            return ResponseData.error_response(
                error="缺少必填参数: begin_time 或 end_time",
                code="MISSING_PARAMETER",
            )

        params_dict["mch_id"] = self.config.mch_id

        # 构建请求参数
        request_params = self._build_common_params()
        request_params.update(params_dict)

        url = f"{self.config.gateway_url}/billcommentsp/batchquerycomment"
        return self._do_request(url, request_params)


# 将 Mixin 的方法添加到 WechatClient 类
def inject_advanced_methods():
    """动态注入高级API方法到 WechatClient"""
    from gopay.wechat.client import WechatClient

    # 遍历 Mixin 的所有方法
    for method_name in dir(WechatAdvancedMixin):
        if not method_name.startswith("_"):
            method = getattr(WechatAdvancedMixin, method_name)
            if callable(method):
                # 动态添加到 WechatClient
                setattr(WechatClient, method_name, method)


# 自动注入
inject_advanced_methods()
