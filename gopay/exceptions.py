"""
异常定义模块
遵循单一职责原则 - 每个异常类负责一种错误类型
"""

from typing import Optional, Dict, Any


class GoPayError(Exception):
    """GoPay基础异常类"""

    def __init__(self, message: str, code: Optional[str] = None, extra: Optional[Dict[str, Any]] = None):
        self.message = message
        self.code = code
        self.extra = extra or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "code": self.code,
            "extra": self.extra,
        }


class ConfigError(GoPayError):
    """配置错误"""

    def __init__(self, message: str, config_key: Optional[str] = None):
        super().__init__(message, code="CONFIG_ERROR")
        self.config_key = config_key


class SignError(GoPayError):
    """签名验签错误"""

    def __init__(self, message: str, sign_type: Optional[str] = None):
        super().__init__(message, code="SIGN_ERROR")
        self.sign_type = sign_type


class PaymentError(GoPayError):
    """支付业务错误"""

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        error_sub_code: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, code=error_code or "PAYMENT_ERROR", extra=extra)
        self.error_sub_code = error_sub_code


class NetworkError(GoPayError):
    """网络请求错误"""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_text: Optional[str] = None,
    ):
        super().__init__(message, code="NETWORK_ERROR")
        self.status_code = status_code
        self.response_text = response_text


class CertificateError(GoPayError):
    """证书处理错误"""

    def __init__(self, message: str, cert_type: Optional[str] = None):
        super().__init__(message, code="CERTIFICATE_ERROR")
        self.cert_type = cert_type


class ValidationError(GoPayError):
    """参数验证错误"""

    def __init__(self, message: str, field_name: Optional[str] = None, field_value: Optional[Any] = None):
        super().__init__(message, code="VALIDATION_ERROR")
        self.field_name = field_name
        self.field_value = field_value


class NotifyError(GoPayError):
    """通知处理错误"""

    def __init__(self, message: str, notify_type: Optional[str] = None):
        super().__init__(message, code="NOTIFY_ERROR")
        self.notify_type = notify_type
