"""
支付宝用户授权API
包含用户登录授权、信息查询等功能
"""

import logging
from typing import Dict, Any
from gopay.utils.datastructure import BodyMap, ResponseData


logger = logging.getLogger(__name__)


class AlipayUserMixin:
    """
    支付宝用户授权API Mixin类
    """

    def user_info_auth(self, params: BodyMap) -> ResponseData:
        """
        支付宝登录授权
        文档: https://opendocs.alipay.com/open/284/106117358
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.user.info.auth", biz_content)

    def user_info_share(self, params: BodyMap) -> ResponseData:
        """
        支付宝会员授权信息查询
        文档: https://opendocs.alipay.com/open/284/106118351
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.user.info.share", biz_content)

    def user_authzh_details(self, params: BodyMap) -> ResponseData:
        """
        会员卡信息查询(详情版)
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.user.authzh.details", biz_content)

    def user_certify_open_init(self, params: BodyMap) -> ResponseData:
        """
        身份认证初始化服务
        文档: https://opendocs.alipay.com/open/284/106282956
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.user.certify.open.initialize", biz_content)

    def user_certify_open_certify(self, params: BodyMap) -> ResponseData:
        """
        身份认证开始认证
        文档: https://opendocs.alipay.com/open/284/106282956
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.user.certify.open.certify", biz_content)

    def user_certify_open_query(self, params: BodyMap) -> ResponseData:
        """
        身份认证记录查询
        文档: https://opendocs.alipay.com/open/284/106282956
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.user.certify.open.query", biz_content)

    def user_face_verify_verify(self, params: BodyMap) -> ResponseData:
        """
        人脸初始化
        文档: https://opendocs.alipay.com/open/271/105898990
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.user.face.verify.verify", biz_content)

    def user_face_verify_query(self, params: BodyMap) -> ResponseData:
        """
        人脸查询结果查询
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.user.face.verify.query", biz_content)

    def user_agreement_page_sign(self, params: BodyMap) -> ResponseData:
        """
        支付宝个人协议页面签约接口
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.user.agreement.page.sign", biz_content)

    def user_agreement_page_sign_in_qrcode(self, params: BodyMap) -> ResponseData:
        """
        PC转二维码唤起签约页
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.user.agreement.page.signin.qrcode", biz_content)

    def user_agreement_page_unsign(self, params: BodyMap) -> ResponseData:
        """
        支付宝个人代扣协议解约接口
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.user.agreement.page.unsign", biz_content)

    def user_agreement_query(self, params: BodyMap) -> ResponseData:
        """
        支付宝个人代扣协议查询接口
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.user.agreement.query", biz_content)

    def user_transaction_query(self, params: BodyMap) -> ResponseData:
        """
        支付宝个人交易记录查询
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.user.transaction.query", biz_content)

    def user_invoice_billsend(self, params: BodyMap) -> ResponseData:
        """
        蚂蚁发票发送指令
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.user.invoice.billsend", biz_content)

    def user_invoice_bill查询(self, params: BodyMap) -> ResponseData:
        """
        蚂蚁发票查询指令
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.user.invoice.billquery", biz_content)

    def user_invoice_batchquery(self, params: BodyMap) -> ResponseData:
        """
        蚂蚁发票批量查询指令
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.user.invoice.batchquery", biz_content)

    def system_oauth_token(self, params: BodyMap) -> ResponseData:
        """
        换取授权访问令牌
        文档: https://opendocs.alipay.com/open/284/106118352
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.system.oauth.token", biz_content)

    def system_oauth_token_refresh(self, params: BodyMap) -> ResponseData:
        """
        换取用户授权令牌(refresh_token)
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.system.oauth.token.refresh", biz_content)

    def system_oauth_token_query(self, params: BodyMap) -> ResponseData:
        """
        查询授权信息
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.system.oauth.token.query", biz_content)

    def system_oauth_token_app_query(self, params: BodyMap) -> ResponseData:
        """
        查询应用授权
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.system.oauth.token.app.query", biz_content)

    def system_oauth_token_app_cancel(self, params: BodyMap) -> ResponseData:
        """
        撤销应用授权
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.system.oauth.token.app.cancel", biz_content)

    def system_oauth_token_app_refresh(self, params: BodyMap) -> ResponseData:
        """
        换取应用授权令牌(应用授权)
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.system.oauth.token.app.refresh", biz_content)

    def system_oauth_token_app_exchange(self, params: BodyMap) -> ResponseData:
        """
        换取应用授权令牌(授权码换取)
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.system.oauth.token.app.exchange", biz_content)

    def monitor_heartbeat_syn(self, params: BodyMap) -> ResponseData:
        """
        验签接口
        文档: https://opendocs.alipay.com/open/284/106118361
        """
        biz_content = params.to_dict()
        return self._do_request("alipay.monitor.heartbeat.syn", biz_content)


def inject_user_methods():
    from gopay.alipay.client import AlipayClient
    for method_name in dir(AlipayUserMixin):
        if not method_name.startswith("_"):
            method = getattr(AlipayUserMixin, method_name)
            if callable(method):
                setattr(AlipayClient, method_name, method)


inject_user_methods()
