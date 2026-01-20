"""
签名和验签模块
遵循策略模式 - 支持多种签名算法
遵循单一职责原则 - 每个签名器负责一种签名方式
"""

from typing import Dict, Any, Optional, Union
from abc import ABC, abstractmethod
import hashlib
import hmac
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend

from gopay.exceptions import SignError


class Signer(ABC):
    """
    签名器抽象基类
    遵循依赖倒置原则 - 定义签名接口
    """

    @abstractmethod
    def sign(self, data: str, key: str) -> str:
        """签名"""
        pass

    @abstractmethod
    def verify(self, data: str, signature: str, key: str) -> bool:
        """验签"""
        pass


class MD5Signer(Signer):
    """MD5签名器"""

    def sign(self, data: str, key: str) -> str:
        """MD5签名"""
        try:
            sign_str = f"{data}&key={key}"
            return hashlib.md5(sign_str.encode("utf-8")).hexdigest().upper()
        except Exception as e:
            raise SignError(f"MD5签名失败: {e}", "MD5")

    def verify(self, data: str, signature: str, key: str) -> bool:
        """MD5验签"""
        calculated_sign = self.sign(data, key)
        return calculated_sign == signature


class HMACSHA256Signer(Signer):
    """HMAC-SHA256签名器"""

    def sign(self, data: str, key: str) -> str:
        """HMAC-SHA256签名"""
        try:
            sign_str = f"{data}&key={key}"
            return hmac.new(key.encode("utf-8"), sign_str.encode("utf-8"), hashlib.sha256).hexdigest().upper()
        except Exception as e:
            raise SignError(f"HMAC-SHA256签名失败: {e}", "HMAC-SHA256")

    def verify(self, data: str, signature: str, key: str) -> bool:
        """HMAC-SHA256验签"""
        calculated_sign = self.sign(data, key)
        return calculated_sign == signature


class RSASigner(Signer):
    """RSA签名器(支持RSA和RSA2)"""

    def __init__(self, algorithm: str = "RSA2"):
        """
        初始化RSA签名器
        :param algorithm: RSA(sha1) 或 RSA2(sha256)
        """
        if algorithm not in ["RSA", "RSA2"]:
            raise SignError(f"不支持的RSA算法: {algorithm}", algorithm)
        self.algorithm = algorithm
        self.hash_alg = hashes.SHA1() if algorithm == "RSA" else hashes.SHA256()

    def _load_private_key(self, key: str) -> rsa.RSAPrivateKey:
        """加载私钥"""
        try:
            # 支持PEM格式和PKCS#1格式
            if "-----BEGIN" not in key:
                # 如果没有头尾,添加PKCS#1头尾
                key = f"-----BEGIN RSA PRIVATE KEY-----\n{key}\n-----END RSA PRIVATE KEY-----"

            private_key = serialization.load_pem_private_key(
                key.encode("utf-8"),
                password=None,
                backend=default_backend(),
            )
            if not isinstance(private_key, rsa.RSAPrivateKey):
                raise SignError("私钥格式错误,需要RSA私钥", self.algorithm)
            return private_key
        except Exception as e:
            raise SignError(f"加载私钥失败: {e}", self.algorithm)

    def _load_public_key(self, key: str) -> rsa.RSAPublicKey:
        """加载公钥"""
        try:
            if "-----BEGIN" not in key:
                key = f"-----BEGIN PUBLIC KEY-----\n{key}\n-----END PUBLIC KEY-----"

            public_key = serialization.load_pem_public_key(
                key.encode("utf-8"),
                backend=default_backend(),
            )
            if not isinstance(public_key, rsa.RSAPublicKey):
                raise SignError("公钥格式错误,需要RSA公钥", self.algorithm)
            return public_key
        except Exception as e:
            raise SignError(f"加载公钥失败: {e}", self.algorithm)

    def sign(self, data: str, key: str) -> str:
        """RSA签名"""
        try:
            private_key = self._load_private_key(key)
            signature = private_key.sign(
                data.encode("utf-8"),
                padding.PKCS1v15(),
                self.hash_alg,
            )
            return base64.b64encode(signature).decode("utf-8")
        except Exception as e:
            raise SignError(f"RSA签名失败: {e}", self.algorithm)

    def verify(self, data: str, signature: str, key: str) -> bool:
        """RSA验签"""
        try:
            public_key = self._load_public_key(key)
            signature_bytes = base64.b64decode(signature)
            public_key.verify(
                signature_bytes,
                data.encode("utf-8"),
                padding.PKCS1v15(),
                self.hash_alg,
            )
            return True
        except Exception:
            return False


class SignerFactory:
    """
    签名器工厂
    遵循开闭原则 - 通过工厂创建签名器,易于扩展
    """

    _signers: Dict[str, Signer] = {
        "MD5": MD5Signer(),
        "HMAC-SHA256": HMACSHA256Signer(),
        "RSA": RSASigner("RSA"),
        "RSA2": RSASigner("RSA2"),
    }

    @classmethod
    def get_signer(cls, sign_type: str) -> Signer:
        """获取签名器"""
        sign_type_upper = sign_type.upper()
        if sign_type_upper not in cls._signers:
            raise SignError(f"不支持的签名类型: {sign_type}", sign_type)
        return cls._signers[sign_type_upper]

    @classmethod
    def register_signer(cls, sign_type: str, signer: Signer) -> None:
        """注册自定义签名器"""
        cls._signers[sign_type.upper()] = signer


def sign_params(params: Dict[str, Any], key: str, sign_type: str = "HMAC-SHA256") -> str:
    """
    对参数进行签名
    :param params: 参数字典
    :param key: 密钥
    :param sign_type: 签名类型
    :return: 签名字符串
    """
    # 过滤空值和sign字段
    filtered_params = {k: v for k, v in params.items() if v not in [None, ""] and k != "sign"}
    # 按key排序
    sorted_params = sorted(filtered_params.items())
    # 拼接参数
    param_str = "&".join([f"{k}={v}" for k, v in sorted_params])
    # 签名
    signer = SignerFactory.get_signer(sign_type)
    return signer.sign(param_str, key)


def verify_params(params: Dict[str, Any], key: str, sign_type: str = "HMAC-SHA256") -> bool:
    """
    验证参数签名
    :param params: 参数字典
    :param key: 密钥
    :param sign_type: 签名类型
    :return: 是否验证通过
    """
    if "sign" not in params:
        return False
    signature = params["sign"]
    calculated_sign = sign_params(params, key, sign_type)
    return signature == calculated_sign


def generate_sign(content: str, key: str, sign_type: str = "HMAC-SHA256") -> str:
    """
    生成签名
    :param content: 待签名内容
    :param key: 密钥
    :param sign_type: 签名类型
    :return: 签名
    """
    signer = SignerFactory.get_signer(sign_type)
    return signer.sign(content, key)


def verify_sign(content: str, signature: str, key: str, sign_type: str = "HMAC-SHA256") -> bool:
    """
    验证签名
    :param content: 待验签内容
    :param signature: 签名
    :param key: 密钥
    :param sign_type: 签名类型
    :return: 是否验证通过
    """
    signer = SignerFactory.get_signer(sign_type)
    return signer.verify(content, signature, key)
