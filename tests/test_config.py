"""
配置测试
"""

import pytest
from pathlib import Path
import tempfile
import json

from gopay.config import PaymentConfig, AlipayConfig, WechatConfig, QQConfig, ConfigManager
from gopay.exceptions import ConfigError


class TestPaymentConfig:
    """支付配置基类测试"""

    def test_create_config(self):
        """测试创建配置"""
        config = PaymentConfig(
            app_id="test_app_id",
            mch_id="test_mch_id",
            api_key="test_api_key",
            notify_url="https://test.com/notify",
        )
        assert config.app_id == "test_app_id"
        assert config.mch_id == "test_mch_id"
        assert config.api_key == "test_api_key"

    def test_config_validation(self):
        """测试配置验证"""
        with pytest.raises(ConfigError):
            PaymentConfig(app_id="")

    def test_config_to_dict(self):
        """测试配置转换为字典"""
        config = PaymentConfig(
            app_id="test_app_id",
            mch_id="test_mch_id",
        )
        config_dict = config.to_dict()
        assert config_dict["app_id"] == "test_app_id"
        assert config_dict["mch_id"] == "test_mch_id"

    def test_config_from_dict(self):
        """测试从字典创建配置"""
        config_dict = {
            "app_id": "test_app_id",
            "mch_id": "test_mch_id",
            "api_key": "test_api_key",
        }
        config = PaymentConfig.from_dict(config_dict)
        assert config.app_id == "test_app_id"
        assert config.mch_id == "test_mch_id"

    def test_config_from_file(self):
        """测试从文件加载配置"""
        config_data = {
            "app_id": "test_app_id",
            "mch_id": "test_mch_id",
            "api_key": "test_api_key",
        }

        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config_data, f)
            temp_file = f.name

        try:
            config = PaymentConfig.from_file(temp_file)
            assert config.app_id == "test_app_id"
            assert config.mch_id == "test_mch_id"
        finally:
            Path(temp_file).unlink()


class TestAlipayConfig:
    """支付宝配置测试"""

    def test_create_alipay_config(self):
        """测试创建支付宝配置"""
        config = AlipayConfig(
            app_id="test_app_id",
            app_private_key="test_private_key",
            alipay_public_key="test_public_key",
        )
        assert config.app_id == "test_app_id"
        assert config.gateway_url == "https://openapi.alipay.com/gateway.do"

    def test_sandbox_mode(self):
        """测试沙箱模式"""
        config = AlipayConfig(
            app_id="test_app_id",
            is_sandbox=True,
        )
        assert config.gateway_url == "https://openapi.alipaydev.com/gateway.do"


class TestWechatConfig:
    """微信支付配置测试"""

    def test_create_wechat_config(self):
        """测试创建微信支付配置"""
        config = WechatConfig(
            app_id="test_app_id",
            mch_id="test_mch_id",
            api_key="test_api_key",
        )
        assert config.app_id == "test_app_id"
        assert config.mch_id == "test_mch_id"

    def test_sandbox_mode(self):
        """测试沙箱模式"""
        config = WechatConfig(
            app_id="test_app_id",
            mch_id="test_mch_id",
            api_key="test_api_key",
            is_sandbox=True,
        )
        assert config.gateway_url == "https://api.mch.weixin.qq.com/sandboxnew"


class TestQQConfig:
    """QQ钱包配置测试"""

    def test_create_qq_config(self):
        """测试创建QQ钱包配置"""
        config = QQConfig(
            app_id="test_app_id",
            mch_id="test_mch_id",
            api_key="test_api_key",
        )
        assert config.app_id == "test_app_id"


class TestConfigManager:
    """配置管理器测试"""

    def test_register_and_get_config(self):
        """测试注册和获取配置"""
        manager = ConfigManager()
        config = PaymentConfig(app_id="test_app_id")

        manager.register("test", config)
        retrieved_config = manager.get("test")

        assert retrieved_config.app_id == "test_app_id"

    def test_get_nonexistent_config(self):
        """测试获取不存在的配置"""
        manager = ConfigManager()
        with pytest.raises(ConfigError):
            manager.get("nonexistent")

    def test_remove_config(self):
        """测试移除配置"""
        manager = ConfigManager()
        config = PaymentConfig(app_id="test_app_id")

        manager.register("test", config)
        manager.remove("test")

        with pytest.raises(ConfigError):
            manager.get("test")

    def test_list_configs(self):
        """测试列出所有配置"""
        manager = ConfigManager()
        config1 = PaymentConfig(app_id="app1")
        config2 = PaymentConfig(app_id="app2")

        manager.register("config1", config1)
        manager.register("config2", config2)

        configs = manager.list_configs()
        assert "config1" in configs
        assert "config2" in configs
        assert len(configs) == 2
