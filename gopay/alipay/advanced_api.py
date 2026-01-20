"""
支付宝支付高级API
补充缺失的支付功能
"""

import logging
from typing import Optional, Dict, Any
from urllib.parse import urlencode

from gopay.utils.datastructure import BodyMap, ResponseData


logger = logging.getLogger(__name__)


# 扩展 AlipayClient 类，添加缺失的API方法
class AlipayAdvancedMixin:
    """
    支付宝高级API Mixin类
    包含当面支付、扫码支付等高级功能
    """

    def trade_pay(self, params: BodyMap) -> ResponseData:
        """
        统一收单交易支付接口
        适用于当面付、声波支付等场景
        文档: https://opendocs.alipay.com/open/02cdx8

        :param params: 参数对象
        :return: 支付结果
        """
        biz_content = params.to_dict()

        # 必填参数检查
        required_fields = ["out_trade_no", "subject", "total_amount", "auth_code", "scene"]
        for field in required_fields:
            if field not in biz_content:
                return ResponseData.error_response(
                    error=f"缺少必填参数: {field}",
                    code="MISSING_PARAMETER",
                )

        return self._do_request("alipay.trade.pay", biz_content)

    def trade_precreate(self, params: BodyMap) -> ResponseData:
        """
        统一收单线下交易预创建
        适用于扫码支付场景
        文档: https://opendocs.alipay.com/open/02ekfg

        :param params: 参数对象
        :return: 预创建结果，包含二维码URL
        """
        biz_content = params.to_dict()

        # 必填参数检查
        required_fields = ["out_trade_no", "total_amount", "subject"]
        for field in required_fields:
            if field not in biz_content:
                return ResponseData.error_response(
                    error=f"缺少必填参数: {field}",
                    code="MISSING_PARAMETER",
                )

        return self._do_request("alipay.trade.precreate", biz_content)

    def fund_auth_order_app_freeze(self, params: BodyMap) -> ResponseData:
        """
        金融资金预授权冻结接口
        文档: https://opendocs.alipay.com/open/02fkar7

        :param params: 参数对象
        :return: 授权冻结结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.fund.auth.order.app.freeze", biz_content)

    def fund_auth_order_freeze(self, params: BodyMap) -> ResponseData:
        """
        金融资金授权冻结接口
        文档: https://opendocs.alipay.com/open/02fkar7

        :param params: 参数对象
        :return: 授权冻结结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.fund.auth.order.freeze", biz_content)

    def fund_auth_order_voucher_query(self, params: BodyMap) -> ResponseData:
        """
        金融资金授权查询接口
        文档: https://opendocs.alipay.com/open/02fkar7

        :param params: 参数对象
        :return: 授权查询结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.fund.auth.order.voucher.query", biz_content)

    def fund_auth_order_unfreeze(self, params: BodyMap) -> ResponseData:
        """
        金融资金授权撤销接口
        文档: https://opendocs.alipay.com/open/02fkar7

        :param params: 参数对象
        :return: 撤销结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.fund.auth.order.unfreeze", biz_content)

    def fund_trans_order_query(self, params: BodyMap) -> ResponseData:
        """
        资金转账查询接口
        文档: https://opendocs.alipay.com/open/02cbr8

        :param params: 参数对象
        :return: 转账查询结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.fund.trans.order.query", biz_content)

    def fund_trans_uni_transfer(self, params: BodyMap) -> ResponseData:
        """
        单笔转账接口
        文档: https://opendocs.alipay.com/open/02cbr8

        :param params: 参数对象
        :return: 转账结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.fund.trans.uni.transfer", biz_content)

    def data_bill_balance_query(self, params: Optional[BodyMap] = None) -> ResponseData:
        """
        查询账户余额接口
        文档: https://opendocs.alipay.com/open/02cbr8

        :param params: 参数对象
        :return: 账户余额
        """
        biz_content = params.to_dict() if params else {}
        return self._do_request("alipay.data.bill.balance.query", biz_content)

    def data_bill_subscribe_query(self, params: BodyMap) -> ResponseData:
        """
        账单订阅接口
        文档: https://opendocs.alipay.com/open/02cbr8

        :param params: 参数对象
        :return: 订阅结果
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.data.bill.subscribe.query", biz_content)


# 将 Mixin 的方法添加到 AlipayClient 类
def inject_advanced_methods():
    """动态注入高级API方法到 AlipayClient"""
    from gopay.alipay.client import AlipayClient

    # 遍历 Mixin 的所有方法
    for method_name in dir(AlipayAdvancedMixin):
        if not method_name.startswith("_"):
            method = getattr(AlipayAdvancedMixin, method_name)
            if callable(method):
                # 动态添加到 AlipayClient
                setattr(AlipayClient, method_name, method)


# 自动注入
inject_advanced_methods()
