"""
微信OAuth API
包含微信开放平台授权相关功能
"""

import logging
from gopay.utils.datastructure import BodyMap, ResponseData


logger = logging.getLogger(__name__)


class WechatOAuthMixin:
    """微信OAuth API Mixin类"""

    def get_oauth2_access_token(self, params: BodyMap) -> ResponseData:
        """
        获取access_token
        文档: https://developers.weixin.qq.com/doc/oplatform/Getting_S_started/Getting_Access_Token.html
        """
        params_dict = params.to_dict()
        url = f"{self.config.gateway_url}/cgi-bin/token"
        return self._do_request(url, params_dict)

    def refresh_oauth2_access_token(self, params: BodyMap) -> ResponseData:
        """
        刷新access_token
        """
        params_dict = params.to_dict()
        url = f"{self.config.gateway_url}/cgi-bin/token"
        return self._do_request(url, params_dict)

    def check_oauth2_access_token(self, params: BodyMap) -> ResponseData:
        """
        检验access_token是否有效
        """
        params_dict = params.to_dict()
        url = f"{self.config.gateway_url}/cgi-bin/auth/draft/api/check_token"
        return self._do_request(url, params_dict)

    def get_oauth2_userinfo(self, params: BodyMap) -> ResponseData:
        """
        获取用户信息
        """
        params_dict = params.to_dict()
        url = f"{self.config.gateway_url}/cgi-bin/user/info"
        return self._do_request(url, params_dict)

    def jscode2session(self, params: BodyMap) -> ResponseData:
        """
        登录凭证校验
        """
        params_dict = params.to_dict()
        url = f"{self.config.gateway_url}/wxa/checksession"
        return self._do_request(url, params_dict)

    def get_api_domain_ip(self, params: BodyMap) -> ResponseData:
        """
        获取微信服务器IP地址
        """
        params_dict = params.to_dict()
        url = f"{self.config.gateway_url}/cgi-bin/get_api_domain_ip"
        return self._do_request(url, params_dict)

    def clear_quota(self, params: BodyMap) -> ResponseData:
        """
        清除接口调用次数
        """
        params_dict = params.to_dict()
        url = f"{self.config.gateway_url}/cgi-bin/clear_quota"
        return self._do_request(url, params_dict)


def inject_oauth_methods():
    from gopay.wechat.client import WechatClient
    for method_name in dir(WechatOAuthMixin):
        if not method_name.startswith("_"):
            method = getattr(WechatOAuthMixin, method_name)
            if callable(method):
                setattr(WechatClient, method_name, method)


inject_oauth_methods()
