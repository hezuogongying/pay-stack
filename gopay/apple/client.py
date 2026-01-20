"""
Apple Pay客户端
支持App Store收据验证和订阅管理
"""

import logging
import json
from typing import Optional, Dict, Any
from urllib.parse import urljoin

from gopay.config import PaymentConfig
from gopay.utils.datastructure import ResponseData
from gopay.http import HttpClient


logger = logging.getLogger(__name__)


class ApplePayConfig(PaymentConfig):
    """Apple Pay配置"""

    def __init__(
        self,
        app_shared_secret: Optional[str] = None,
        sandbox: bool = True,
        timeout: int = 30,
        **kwargs
    ):
        """
        初始化Apple Pay配置

        Args:
            app_shared_secret: App共享密钥(用于验证自动续期订阅)
            sandbox: 是否使用沙箱环境(True=沙箱, False=生产环境)
            timeout: 请求超时时间(秒)
        """
        self.app_shared_secret = app_shared_secret
        self.sandbox = sandbox
        self.timeout = timeout

        # 设置网关URL
        if sandbox:
            self.gateway_url = "https://sandbox.itunes.apple.com"
        else:
            self.gateway_url = "https://buy.itunes.apple.com"

        super().__init__(gateway_url=self.gateway_url, **kwargs)

    def validate(self):
        """验证配置"""
        if not self.app_shared_secret:
            logger.warning("未设置app_shared_secret,某些订阅功能可能无法使用")


class ApplePayClient:
    """Apple Pay客户端 - 支持收据验证和订阅管理"""

    def __init__(self, config: ApplePayConfig):
        """
        初始化Apple Pay客户端

        Args:
            config: Apple Pay配置对象
        """
        self.config = config
        self.config.validate()
        self.http_client = HttpClient(
            timeout=config.timeout,
            max_retries=3,
            retry_interval=1
        )

    def _do_request(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ) -> ResponseData:
        """
        执行HTTP请求

        Args:
            endpoint: API端点
            data: 请求数据

        Returns:
            ResponseData: 响应数据
        """
        url = urljoin(self.config.gateway_url, endpoint)

        try:
            response = self.http_client.post(
                url=url,
                json=data or {},
                headers={"Content-Type": "application/json"}
            )

            return ResponseData(
                code=str(response.get("status", 0)),
                msg=response.get("error", "Success"),
                data=response
            )

        except Exception as e:
            logger.error(f"Apple Pay请求失败: {str(e)}")
            return ResponseData(
                code="-1",
                msg=str(e),
                data={}
            )

    def look_up_order_id(self, order_id: str) -> ResponseData:
        """
        查询订单信息

        Args:
            order_id: 订单ID

        Returns:
            ResponseData: 订单信息
        """
        endpoint = f"/inApps/v1/lookup/{order_id}"
        return self._do_request(endpoint)

    def get_all_subscription_statuses(
        self,
        order_id: str,
        status: Optional[str] = None
    ) -> ResponseData:
        """
        获取所有订阅状态

        Args:
            order_id: 订单ID
            status: 可选的状态筛选

        Returns:
            ResponseData: 订阅状态列表
        """
        endpoint = f"/inApps/v1/subscriptions/{order_id}"
        params = {}
        if status:
            params["status"] = status
        return self._do_request(endpoint, params if params else None)

    def get_transaction_history(
        self,
        query_params: Optional[Dict[str, Any]] = None
    ) -> ResponseData:
        """
        获取交易历史(已废弃,使用get_transaction_history_v2)

        Args:
            query_params: 查询参数

        Returns:
            ResponseData: 交易历史记录
        """
        endpoint = "/inApps/v1/history"
        return self._do_request(endpoint, query_params)

    def get_transaction_history_v2(
        self,
        query_params: Optional[Dict[str, Any]] = None
    ) -> ResponseData:
        """
        获取交易历史(V2版本)

        Args:
            query_params: 查询参数,包括:
                - productId: 产品ID
                - transactionId: 交易ID
                - startDate: 开始日期
                - endDate: 结束日期
                - revoked: 是否显示已撤销的交易

        Returns:
            ResponseData: 交易历史记录
        """
        endpoint = "/inApps/v2/history"
        return self._do_request(endpoint, query_params)

    def get_notification_history(
        self,
        query_params: Optional[Dict[str, Any]] = None
    ) -> ResponseData:
        """
        获取通知历史

        Args:
            query_params: 查询参数,包括:
                - startDate: 开始日期
                - endDate: 结束日期
                - notificationType: 通知类型
                - onlyFailures: 是否只显示失败的通知

        Returns:
            ResponseData: 通知历史记录
        """
        endpoint = "/inApps/v1/notifications/history"
        return self._do_request(endpoint, query_params)

    def verify_receipt(
        self,
        receipt_data: str,
        password: Optional[str] = None,
        exclude_old_transactions: bool = False
    ) -> ResponseData:
        """
        验证收据

        Args:
            receipt_data: 收据数据(Base64编码)
            password: App共享密钥(可选,如果未配置)
            exclude_old_transactions: 是否排除旧交易

        Returns:
            ResponseData: 验证结果
        """
        endpoint = "/verifyReceipt"

        receipt_password = password or self.config.app_shared_secret

        request_data = {
            "receipt-data": receipt_data,
            "exclude-old-transactions": exclude_old_transactions
        }

        if receipt_password:
            request_data["password"] = receipt_password

        return self._do_request(endpoint, request_data)

    def decode_signed_payload(self, signed_payload: str) -> ResponseData:
        """
        解码签名负载(用于App Store Server Notification)

        Args:
            signed_payload: 签名的负载(Base64编码)

        Returns:
            ResponseData: 解码后的数据
        """
        endpoint = "/inApps/v1/decodeSignedPayload"
        return self._do_request(endpoint, {"signedPayload": signed_payload})

    def extract_claims(
        self,
        signed_payload: str,
        claims_version: str = "1"
    ) -> ResponseData:
        """
        从签名负载中提取声明

        Args:
            signed_payload: 签名的负载
            claims_version: 声明版本

        Returns:
            ResponseData: 提取的声明
        """
        endpoint = "/inApps/v1/extractClaims"
        return self._do_request(endpoint, {
            "signedPayload": signed_payload,
            "claimsVersion": claims_version
        })

    def extract_claims_token(
        self,
        signed_payload: str
    ) -> ResponseData:
        """
        从签名负载中提取声明令牌

        Args:
            signed_payload: 签名的负载

        Returns:
            ResponseData: 提取的声明令牌
        """
        endpoint = "/inApps/v1/extractClaimsToken"
        return self._do_request(endpoint, {"signedPayload": signed_payload})

    def get_refund_history(
        self,
        query_params: Optional[Dict[str, Any]] = None
    ) -> ResponseData:
        """
        获取退款历史

        Args:
            query_params: 查询参数,包括:
                - productId: 产品ID
                - transactionId: 交易ID
                - startDate: 开始日期
                - endDate: 结束日期

        Returns:
            ResponseData: 退款历史记录
        """
        endpoint = "/inApps/v2/refund/lookup"
        return self._do_request(endpoint, query_params)

    def get_consumption_info(
        self,
        query_params: Optional[Dict[str, Any]] = None
    ) -> ResponseData:
        """
        获取消耗信息

        Args:
            query_params: 查询参数,包括:
                - transactionId: 交易ID
                - startDate: 开始日期
                - endDate: 结束日期

        Returns:
            ResponseData: 消耗信息
        """
        endpoint = "/inApps/v1/consumption"
        return self._do_request(endpoint, query_params)

    def get_subscription_status(
        self,
        transaction_id: str
    ) -> ResponseData:
        """
        获取订阅状态

        Args:
            transaction_id: 交易ID

        Returns:
            ResponseData: 订阅状态
        """
        endpoint = f"/inApps/v1/subscriptions/{transaction_id}"
        return self._do_request(endpoint)
