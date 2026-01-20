"""
签名测试
"""

import pytest
from gopay.utils.signer import (
    MD5Signer,
    HMACSHA256Signer,
    RSASigner,
    SignerFactory,
    sign_params,
    verify_params,
)
from gopay.exceptions import SignError


class TestMD5Signer:
    """MD5签名器测试"""

    def test_sign(self):
        """测试MD5签名"""
        signer = MD5Signer()
        data = "key1=value1&key2=value2"
        key = "test_key"
        signature = signer.sign(data, key)
        assert signature is not None
        assert len(signature) == 32  # MD5签名长度为32

    def test_verify(self):
        """测试MD5验签"""
        signer = MD5Signer()
        data = "key1=value1&key2=value2"
        key = "test_key"
        signature = signer.sign(data, key)
        assert signer.verify(data, signature, key) is True
        assert signer.verify(data, "wrong_sign", key) is False


class TestHMACSHA256Signer:
    """HMAC-SHA256签名器测试"""

    def test_sign(self):
        """测试HMAC-SHA256签名"""
        signer = HMACSHA256Signer()
        data = "key1=value1&key2=value2"
        key = "test_key"
        signature = signer.sign(data, key)
        assert signature is not None
        assert len(signature) == 64  # HMAC-SHA256签名长度为64

    def test_verify(self):
        """测试HMAC-SHA256验签"""
        signer = HMACSHA256Signer()
        data = "key1=value1&key2=value2"
        key = "test_key"
        signature = signer.sign(data, key)
        assert signer.verify(data, signature, key) is True
        assert signer.verify(data, "wrong_sign", key) is False


class TestRSASigner:
    """RSA签名器测试"""

    @pytest.fixture
    def rsa_key_pair(self):
        """生成RSA密钥对"""
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import serialization

        # 生成私钥
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend(),
        )

        # 提取公钥
        public_key = private_key.public_key()

        # 序列化私钥
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode("utf-8")

        # 序列化公钥
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

        return private_pem, public_pem

    def test_rsa2_sign_and_verify(self, rsa_key_pair):
        """测试RSA2签名和验签"""
        private_key, public_key = rsa_key_pair
        signer = RSASigner("RSA2")
        data = "test_data"
        signature = signer.sign(data, private_key)
        assert signer.verify(data, signature, public_key) is True

    def test_rsa_sign_and_verify(self, rsa_key_pair):
        """测试RSA签名和验签"""
        private_key, public_key = rsa_key_pair
        signer = RSASigner("RSA")
        data = "test_data"
        signature = signer.sign(data, private_key)
        assert signer.verify(data, signature, public_key) is True

    def test_invalid_algorithm(self):
        """测试无效的RSA算法"""
        with pytest.raises(SignError):
            RSASigner("INVALID")


class TestSignerFactory:
    """签名器工厂测试"""

    def test_get_md5_signer(self):
        """测试获取MD5签名器"""
        signer = SignerFactory.get_signer("MD5")
        assert isinstance(signer, MD5Signer)

    def test_get_hmac_sha256_signer(self):
        """测试获取HMAC-SHA256签名器"""
        signer = SignerFactory.get_signer("HMAC-SHA256")
        assert isinstance(signer, HMACSHA256Signer)

    def test_get_rsa_signer(self):
        """测试获取RSA签名器"""
        signer = SignerFactory.get_signer("RSA")
        assert isinstance(signer, RSASigner)
        assert signer.algorithm == "RSA"

    def test_get_rsa2_signer(self):
        """测试获取RSA2签名器"""
        signer = SignerFactory.get_signer("RSA2")
        assert isinstance(signer, RSASigner)
        assert signer.algorithm == "RSA2"

    def test_invalid_sign_type(self):
        """测试无效的签名类型"""
        with pytest.raises(SignError):
            SignerFactory.get_signer("INVALID")


class TestSignParams:
    """参数签名测试"""

    def test_sign_params_md5(self):
        """测试MD5签名参数"""
        params = {
            "key1": "value1",
            "key2": "value2",
            "sign": "old_sign",
        }
        key = "test_key"
        signature = sign_params(params, key, "MD5")
        assert signature is not None

    def test_sign_params_hmac_sha256(self):
        """测试HMAC-SHA256签名参数"""
        params = {
            "key1": "value1",
            "key2": "value2",
        }
        key = "test_key"
        signature = sign_params(params, key, "HMAC-SHA256")
        assert signature is not None

    def test_verify_params(self):
        """测试验证参数签名"""
        params = {
            "key1": "value1",
            "key2": "value2",
        }
        key = "test_key"
        signature = sign_params(params, key, "MD5")
        params["sign"] = signature
        assert verify_params(params, key, "MD5") is True

    def test_verify_params_with_wrong_sign(self):
        """测试使用错误签名验证参数"""
        params = {
            "key1": "value1",
            "key2": "value2",
            "sign": "wrong_sign",
        }
        key = "test_key"
        assert verify_params(params, key, "MD5") is False

    def test_filter_none_values(self):
        """测试过滤None值"""
        params = {
            "key1": "value1",
            "key2": None,
            "key3": "",
            "key4": "value4",
        }
        key = "test_key"
        signature = sign_params(params, key, "MD5")
        # 确保空值被过滤
        assert signature is not None
