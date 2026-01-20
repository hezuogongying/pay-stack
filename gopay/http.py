"""
HTTP客户端模块
遵循单一职责原则 - 专门负责HTTP请求
"""

from typing import Optional, Dict, Any, Union
import time
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from gopay.exceptions import NetworkError


logger = logging.getLogger(__name__)


class HttpClient:
    """
    HTTP客户端
    封装requests库,提供重试、超时等功能
    """

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        retry_interval: float = 1.0,
        enable_log: bool = True,
    ):
        """
        初始化HTTP客户端
        :param timeout: 超时时间(秒)
        :param max_retries: 最大重试次数
        :param retry_interval: 重试间隔(秒)
        :param enable_log: 是否启用日志
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.enable_log = enable_log

        # 创建session
        self.session = requests.Session()

        # 配置重试策略
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=retry_interval,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs,
    ) -> requests.Response:
        """
        发送HTTP请求
        :param method: 请求方法
        :param url: 请求URL
        :param params: URL参数
        :param data: 请求体数据
        :param json: JSON请求体
        :param headers: 请求头
        :param timeout: 超时时间
        :return: 响应对象
        """
        timeout = timeout or self.timeout

        if self.enable_log:
            logger.info(f"发送HTTP请求: {method} {url}")
            if headers:
                logger.debug(f"请求头: {headers}")
            if data:
                logger.debug(f"请求数据: {data}")

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    json=json,
                    headers=headers,
                    timeout=timeout,
                    **kwargs,
                )

                if self.enable_log:
                    logger.info(f"HTTP响应: status={response.status_code}")

                return response

            except requests.exceptions.Timeout as e:
                last_error = e
                if self.enable_log:
                    logger.warning(f"请求超时(尝试 {attempt + 1}/{self.max_retries + 1}): {e}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_interval)

            except requests.exceptions.ConnectionError as e:
                last_error = e
                if self.enable_log:
                    logger.warning(f"连接错误(尝试 {attempt + 1}/{self.max_retries + 1}): {e}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_interval)

            except requests.exceptions.RequestException as e:
                raise NetworkError(
                    f"HTTP请求失败: {e}",
                    status_code=getattr(e.response, "status_code", None) if hasattr(e, "response") else None,
                )

        # 所有重试都失败
        raise NetworkError(f"HTTP请求失败,已重试{self.max_retries}次: {last_error}")

    def get(self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """GET请求"""
        return self.request("GET", url, params=params, **kwargs)

    def post(
        self,
        url: str,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """POST请求"""
        return self.request("POST", url, data=data, json=json, **kwargs)

    def put(self, url: str, data: Optional[Union[Dict[str, Any], str, bytes]] = None, **kwargs) -> requests.Response:
        """PUT请求"""
        return self.request("PUT", url, data=data, **kwargs)

    def delete(self, url: str, **kwargs) -> requests.Response:
        """DELETE请求"""
        return self.request("DELETE", url, **kwargs)

    def close(self):
        """关闭session"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
