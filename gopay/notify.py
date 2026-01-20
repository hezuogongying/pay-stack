"""
通知处理模块
遵循单一职责原则 - 专门负责支付通知的验证和解析
遵循开闭原则 - 通过工厂模式支持多种支付渠道
"""

import logging
from typing import Dict, Any, Optional, Union, Callable
from abc import ABC, abstractmethod
import json
from functools import wraps

from gopay.utils.datastructure import XmlMap
from gopay.utils.signer import SignerFactory
from gopay.exceptions import NotifyError


logger = logging.getLogger(__name__)


class NotifyHandler(ABC):
    """
    通知处理器抽象基类
    遵循依赖倒置原则 - 定义通知处理接口
    """

    @abstractmethod
    def parse(self, raw_data: Union[str, bytes, Dict[str, Any]]) -> Dict[str, Any]:
        """解析原始通知数据"""
        pass

    @abstractmethod
    def verify(self, data: Dict[str, Any], signature: str) -> bool:
        """验证通知签名"""
        pass

    @abstractmethod
    def success_response(self) -> str:
        """返回成功响应"""
        pass

    @abstractmethod
    def fail_response(self, message: str = "") -> str:
        """返回失败响应"""
        pass


class AlipayNotifyHandler(NotifyHandler):
    """
    支付宝通知处理器
    """

    def __init__(self, public_key: str, sign_type: str = "RSA2"):
        """
        初始化支付宝通知处理器
        :param public_key: 支付宝公钥
        :param sign_type: 签名类型
        """
        self.public_key = public_key
        self.signer = SignerFactory.get_signer(sign_type)

    def parse(self, raw_data: Union[str, bytes, Dict[str, Any]]) -> Dict[str, Any]:
        """解析支付宝通知数据"""
        if isinstance(raw_data, dict):
            return raw_data
        elif isinstance(raw_data, (str, bytes)):
            # 支付宝通知通常是POST表单数据
            try:
                if isinstance(raw_data, bytes):
                    raw_data = raw_data.decode("utf-8")
                # URL参数格式
                from urllib.parse import parse_qs
                parsed = parse_qs(raw_data)
                return {k: v[0] if v else "" for k, v in parsed.items()}
            except Exception as e:
                raise NotifyError(f"解析支付宝通知失败: {e}", "ALIPAY")
        else:
            raise NotifyError("不支持的数据格式", "ALIPAY")

    def verify(self, data: Dict[str, Any], signature: str) -> bool:
        """验证支付宝通知签名"""
        try:
            # 过滤空值和sign字段
            filtered_data = {k: v for k, v in data.items() if v not in [None, ""] and k != "sign"}
            # 按key排序
            sorted_params = sorted(filtered_data.items())
            # 拼接参数
            param_str = "&".join([f"{k}={v}" for k, v in sorted_params])

            return self.signer.verify(param_str, signature, self.public_key)
        except Exception as e:
            logger.error(f"支付宝通知验签失败: {e}")
            return False

    def success_response(self) -> str:
        """返回成功响应"""
        return "success"

    def fail_response(self, message: str = "") -> str:
        """返回失败响应"""
        return "failure"


class WechatNotifyHandler(NotifyHandler):
    """
    微信通知处理器
    """

    def __init__(self, api_key: str, sign_type: str = "HMAC-SHA256"):
        """
        初始化微信通知处理器
        :param api_key: API密钥
        :param sign_type: 签名类型
        """
        self.api_key = api_key
        self.signer = SignerFactory.get_signer(sign_type)

    def parse(self, raw_data: Union[str, bytes, Dict[str, Any]]) -> Dict[str, Any]:
        """解析微信通知数据"""
        if isinstance(raw_data, dict):
            return raw_data
        elif isinstance(raw_data, (str, bytes)):
            try:
                if isinstance(raw_data, bytes):
                    raw_data = raw_data.decode("utf-8")
                # 微信通知是XML格式
                xml_map = XmlMap.from_xml(raw_data)
                return xml_map.to_dict()
            except Exception as e:
                raise NotifyError(f"解析微信通知失败: {e}", "WECHAT")
        else:
            raise NotifyError("不支持的数据格式", "WECHAT")

    def verify(self, data: Dict[str, Any], signature: str) -> bool:
        """验证微信通知签名"""
        try:
            # 过滤空值和sign字段
            filtered_data = {k: v for k, v in data.items() if v not in [None, ""] and k != "sign"}
            # 按key排序
            sorted_params = sorted(filtered_data.items())
            # 拼接参数
            param_str = "&".join([f"{k}={v}" for k, v in sorted_params])

            calculated_sign = self.signer.sign(param_str, self.api_key)
            return calculated_sign == signature
        except Exception as e:
            logger.error(f"微信通知验签失败: {e}")
            return False

    def success_response(self) -> str:
        """返回成功响应"""
        xml_map = XmlMap()
        xml_map.set("return_code", "SUCCESS")
        xml_map.set("return_msg", "OK")
        return xml_map.to_xml()

    def fail_response(self, message: str = "") -> str:
        """返回失败响应"""
        xml_map = XmlMap()
        xml_map.set("return_code", "FAIL")
        xml_map.set("return_msg", message or "处理失败")
        return xml_map.to_xml()


class QQNotifyHandler(NotifyHandler):
    """
    QQ钱包通知处理器
    """

    def __init__(self, api_key: str, sign_type: str = "HMAC-SHA256"):
        """
        初始化QQ钱包通知处理器
        :param api_key: API密钥
        :param sign_type: 签名类型
        """
        self.api_key = api_key
        self.signer = SignerFactory.get_signer(sign_type)

    def parse(self, raw_data: Union[str, bytes, Dict[str, Any]]) -> Dict[str, Any]:
        """解析QQ钱包通知数据"""
        # QQ钱包通知格式与微信类似,都是XML
        if isinstance(raw_data, dict):
            return raw_data
        elif isinstance(raw_data, (str, bytes)):
            try:
                if isinstance(raw_data, bytes):
                    raw_data = raw_data.decode("utf-8")
                # QQ钱包通知是XML格式
                xml_map = XmlMap.from_xml(raw_data)
                return xml_map.to_dict()
            except Exception as e:
                raise NotifyError(f"解析QQ钱包通知失败: {e}", "QQ")
        else:
            raise NotifyError("不支持的数据格式", "QQ")

    def verify(self, data: Dict[str, Any], signature: str) -> bool:
        """验证QQ钱包通知签名"""
        try:
            # 过滤空值和sign字段
            filtered_data = {k: v for k, v in data.items() if v not in [None, ""] and k != "sign"}
            # 按key排序
            sorted_params = sorted(filtered_data.items())
            # 拼接参数
            param_str = "&".join([f"{k}={v}" for k, v in sorted_params])

            calculated_sign = self.signer.sign(param_str, self.api_key)
            return calculated_sign == signature
        except Exception as e:
            logger.error(f"QQ钱包通知验签失败: {e}")
            return False

    def success_response(self) -> str:
        """返回成功响应"""
        xml_map = XmlMap()
        xml_map.set("return_code", "SUCCESS")
        xml_map.set("return_msg", "OK")
        return xml_map.to_xml()

    def fail_response(self, message: str = "") -> str:
        """返回失败响应"""
        xml_map = XmlMap()
        xml_map.set("return_code", "FAIL")
        xml_map.set("return_msg", message or "处理失败")
        return xml_map.to_xml()


class NotifyProcessor:
    """
    通知处理器
    遵循单一职责原则 - 统一的通知处理入口
    """

    def __init__(self, handler: NotifyHandler):
        """
        初始化通知处理器
        :param handler: 具体的通知处理器
        """
        self.handler = handler

    def process(
        self,
        raw_data: Union[str, bytes, Dict[str, Any]],
        callback: Optional[Callable[[Dict[str, Any]], Any]] = None,
    ) -> str:
        """
        处理通知
        :param raw_data: 原始通知数据
        :param callback: 业务处理回调函数
        :return: 响应字符串
        """
        try:
            # 解析通知
            data = self.handler.parse(raw_data)

            # 获取签名
            signature = data.get("sign", "")
            if not signature:
                logger.warning("通知中没有签名")
                return self.handler.fail_response("缺少签名")

            # 验证签名
            if not self.handler.verify(data, signature):
                logger.warning("通知签名验证失败")
                return self.handler.fail_response("签名验证失败")

            # 执行业务回调
            if callback:
                try:
                    result = callback(data)
                    if result is False:
                        return self.handler.fail_response("业务处理失败")
                except Exception as e:
                    logger.error(f"业务处理失败: {e}")
                    return self.handler.fail_response("业务处理异常")

            # 返回成功响应
            return self.handler.success_response()

        except NotifyError as e:
            logger.error(f"通知处理失败: {e}")
            return self.handler.fail_response(str(e))
        except Exception as e:
            logger.error(f"通知处理异常: {e}")
            return self.handler.fail_response("处理异常")


def notify_handler_decorator(handler: NotifyHandler):
    """
    通知处理装饰器
    用于简化Web框架中的通知处理
    """
    def decorator(func: Callable[[Dict[str, Any]], Any]):
        @wraps(func)
        def wrapper(raw_data: Union[str, bytes, Dict[str, Any]], *args, **kwargs):
            processor = NotifyProcessor(handler)
            return processor.process(raw_data, lambda data: func(data, *args, **kwargs))
        return wrapper
    return decorator
