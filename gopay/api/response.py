"""
API响应模块
定义统一的API响应格式
"""

from typing import Any, Optional, Dict
from dataclasses import dataclass
from enum import Enum


class ResponseCode(str, Enum):
    """响应状态码"""
    SUCCESS = "0"
    ERROR = "-1"
    INVALID_PARAMS = "400"
    UNAUTHORIZED = "401"
    NOT_FOUND = "404"
    SERVER_ERROR = "500"


@dataclass
class ApiResponse:
    """
    统一API响应格式

    遵循单一职责原则(SRP): 只负责响应数据的封装
    """

    code: str
    msg: str
    data: Any = None
    trace_id: Optional[str] = None
    timestamp: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典格式

        Returns:
            Dict: 字典格式的响应数据
        """
        result = {
            "code": self.code,
            "msg": self.msg,
        }

        if self.data is not None:
            result["data"] = self.data

        if self.trace_id:
            result["trace_id"] = self.trace_id

        if self.timestamp:
            result["timestamp"] = self.timestamp

        return result

    @classmethod
    def success(cls, data: Any = None, msg: str = "Success") -> "ApiResponse":
        """
        创建成功响应

        Args:
            data: 响应数据
            msg: 响应消息

        Returns:
            ApiResponse: 成功响应对象
        """
        return cls(
            code=ResponseCode.SUCCESS.value,
            msg=msg,
            data=data
        )

    @classmethod
    def error(cls, msg: str, code: str = ResponseCode.ERROR.value) -> "ApiResponse":
        """
        创建错误响应

        Args:
            msg: 错误消息
            code: 错误码

        Returns:
            ApiResponse: 错误响应对象
        """
        return cls(
            code=code,
            msg=msg,
        )

    @classmethod
    def invalid_params(cls, msg: str = "Invalid parameters") -> "ApiResponse":
        """创建参数错误响应"""
        return cls.error(msg, ResponseCode.INVALID_PARAMS.value)

    @classmethod
    def unauthorized(cls, msg: str = "Unauthorized") -> "ApiResponse":
        """创建未授权响应"""
        return cls.error(msg, ResponseCode.UNAUTHORIZED.value)

    @classmethod
    def not_found(cls, msg: str = "Resource not found") -> "ApiResponse":
        """创建未找到响应"""
        return cls.error(msg, ResponseCode.NOT_FOUND.value)

    @classmethod
    def server_error(cls, msg: str = "Internal server error") -> "ApiResponse":
        """创建服务器错误响应"""
        return cls.error(msg, ResponseCode.SERVER_ERROR.value)


class ApiError(Exception):
    """
    API错误异常

    遵循开闭原则(OCP): 可扩展的错误类型
    """

    def __init__(self, msg: str, code: str = ResponseCode.ERROR.value):
        """
        初始化API错误

        Args:
            msg: 错误消息
            code: 错误码
        """
        self.msg = msg
        self.code = code
        super().__init__(msg)

    def to_response(self) -> ApiResponse:
        """
        转换为API响应

        Returns:
            ApiResponse: 错误响应对象
        """
        return ApiResponse.error(self.msg, self.code)


class ValidationError(ApiError):
    """参数验证错误"""

    def __init__(self, msg: str = "Validation failed"):
        super().__init__(msg, ResponseCode.INVALID_PARAMS.value)


class AuthenticationError(ApiError):
    """认证错误"""

    def __init__(self, msg: str = "Authentication failed"):
        super().__init__(msg, ResponseCode.UNAUTHORIZED.value)


class NotFoundError(ApiError):
    """资源未找到错误"""

    def __init__(self, msg: str = "Resource not found"):
        super().__init__(msg, ResponseCode.NOT_FOUND.value)
