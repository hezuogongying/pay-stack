"""
配置管理模块
遵循开闭原则和单一职责原则 - 通过配置类扩展功能
"""

from typing import Optional, Dict, Any, Union
from pathlib import Path
from dataclasses import dataclass, field
import json
import logging

from gopay.exceptions import ConfigError


@dataclass
class PaymentConfig:
    """
    支付配置基类
    遵循依赖倒置原则 - 依赖抽象配置而非具体实现
    """

    # 应用ID
    app_id: str

    # 商户号
    mch_id: Optional[str] = None

    # API密钥
    api_key: Optional[str] = None

    # 通知URL
    notify_url: Optional[str] = None

    # 返回URL
    return_url: Optional[str] = None

    # 网关地址
    gateway_url: Optional[str] = None

    # 是否启用沙箱环境
    is_sandbox: bool = False

    # 连接超时时间(秒)
    timeout: int = 30

    # 证书路径
    cert_path: Optional[str] = None
    key_path: Optional[str] = None
    cert_pem: Optional[str] = None
    key_pem: Optional[str] = None

    # 额外配置
    extra_config: Dict[str, Any] = field(default_factory=dict)

    # 日志配置
    enable_log: bool = True
    log_level: int = logging.INFO

    # HTTP配置
    http_max_retries: int = 3
    http_retry_interval: float = 1.0

    def __post_init__(self):
        """配置验证"""
        if not self.app_id:
            raise ConfigError("app_id 不能为空", "app_id")

    def validate(self) -> None:
        """验证配置是否完整"""
        if not self.app_id:
            raise ConfigError("app_id 未配置", "app_id")

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "app_id": self.app_id,
            "mch_id": self.mch_id,
            "notify_url": self.notify_url,
            "return_url": self.return_url,
            "gateway_url": self.gateway_url,
            "is_sandbox": self.is_sandbox,
            "timeout": self.timeout,
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "PaymentConfig":
        """从字典创建配置"""
        return cls(**config_dict)

    @classmethod
    def from_file(cls, config_file: Union[str, Path]) -> "PaymentConfig":
        """
        从配置文件加载
        支持JSON格式配置文件
        """
        config_path = Path(config_file)
        if not config_path.exists():
            raise ConfigError(f"配置文件不存在: {config_file}")

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                if config_path.suffix == ".json":
                    data = json.load(f)
                else:
                    raise ConfigError(f"不支持的配置文件格式: {config_path.suffix}")
        except json.JSONDecodeError as e:
            raise ConfigError(f"配置文件解析失败: {e}")

        return cls.from_dict(data)

    def get_cert_content(self) -> Optional[str]:
        """获取证书内容"""
        if self.cert_pem:
            return self.cert_pem
        if self.cert_path:
            cert_path = Path(self.cert_path)
            if cert_path.exists():
                return cert_path.read_text(encoding="utf-8")
        return None

    def get_key_content(self) -> Optional[str]:
        """获取私钥内容"""
        if self.key_pem:
            return self.key_pem
        if self.key_path:
            key_path = Path(self.key_path)
            if key_path.exists():
                return key_path.read_text(encoding="utf-8")
        return None


@dataclass
class AlipayConfig(PaymentConfig):
    """
    支付宝配置
    遵循开闭原则 - 继承基类扩展支付宝特有配置
    """

    # 支付宝网关
    gateway_url: str = "https://openapi.alipay.com/gateway.do"
    sandbox_url: str = "https://openapi.alipaydev.com/gateway.do"

    # 签名方式
    sign_type: str = "RSA2"

    # 字符集
    charset: str = "utf-8"

    # 格式
    format: str = "JSON"

    # 应用私钥
    app_private_key: Optional[str] = None

    # 应用私钥文件路径
    app_private_key_path: Optional[str] = None

    # 支付宝公钥
    alipay_public_key: Optional[str] = None

    # 支付宝公钥文件路径
    alipay_public_key_path: Optional[str] = None

    # 应用公钥证书
    app_public_key_cert: Optional[str] = None

    # 支付宝公钥证书
    alipay_public_key_cert: Optional[str] = None

    # 支付宝根证书
    alipay_root_cert: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        # 根据环境设置网关
        if self.is_sandbox:
            self.gateway_url = self.sandbox_url

    def get_app_private_key(self) -> Optional[str]:
        """获取应用私钥"""
        if self.app_private_key:
            return self.app_private_key
        if self.app_private_key_path:
            key_path = Path(self.app_private_key_path)
            if key_path.exists():
                return key_path.read_text(encoding="utf-8")
        return None

    def get_alipay_public_key(self) -> Optional[str]:
        """获取支付宝公钥"""
        if self.alipay_public_key:
            return self.alipay_public_key
        if self.alipay_public_key_path:
            key_path = Path(self.alipay_public_key_path)
            if key_path.exists():
                return key_path.read_text(encoding="utf-8")
        return None


@dataclass
class WechatConfig(PaymentConfig):
    """
    微信支付配置
    遵循开闭原则 - 继承基类扩展微信特有配置
    """

    # 微信支付V3 API密钥
    api_v3_key: Optional[str] = None

    # 微信支付商户序列号
    serial_no: Optional[str] = None

    # 微信支付网关
    gateway_url: str = "https://api.mch.weixin.qq.com"
    sandbox_url: str = "https://api.mch.weixin.qq.com/sandboxnew"

    # 签名类型
    sign_type: str = "HMAC-SHA256"

    # 小程序AppID
    mp_app_id: Optional[str] = None

    # APP应用ID
    app_app_id: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        # 根据环境设置网关
        if self.is_sandbox:
            self.gateway_url = self.sandbox_url


@dataclass
class QQConfig(PaymentConfig):
    """
    QQ支付配置
    """

    # QQ支付网关
    gateway_url: str = "https://qpay.qq.com/cgi-bin/pay"

    # 签名类型
    sign_type: str = "HMAC-SHA256"


class ConfigManager:
    """
    配置管理器
    遵循单一职责原则 - 专门负责配置的管理和切换
    """

    def __init__(self):
        self._configs: Dict[str, PaymentConfig] = {}

    def register(self, name: str, config: PaymentConfig) -> None:
        """注册配置"""
        config.validate()
        self._configs[name] = config

    def get(self, name: str) -> PaymentConfig:
        """获取配置"""
        if name not in self._configs:
            raise ConfigError(f"配置不存在: {name}")
        return self._configs[name]

    def remove(self, name: str) -> None:
        """移除配置"""
        if name in self._configs:
            del self._configs[name]

    def list_configs(self) -> list[str]:
        """列出所有配置名称"""
        return list(self._configs.keys())
