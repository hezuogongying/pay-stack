"""
数据结构模块
提供灵活的数据结构用于构建请求参数
"""

from typing import Any, Dict, Optional, Union, List
from urllib.parse import urlencode
from collections import OrderedDict
import json


class BodyMap(dict):
    """
    请求体映射类
    遵循开闭原则 - 提供链式调用和灵活的参数构建
    类似Go版本中的BodyMap
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 使用OrderedDict保持参数顺序
        self._ordered_data = OrderedDict()

    def set(self, key: str, value: Any) -> "BodyMap":
        """
        设置参数值
        支持链式调用
        """
        if value is not None and value != "":
            self._ordered_data[key] = value
            self[key] = value
        return self

    def get(self, key: str, default: Any = None) -> Any:
        """获取参数值"""
        return self._ordered_data.get(key, default)

    def remove(self, key: str) -> "BodyMap":
        """移除参数"""
        if key in self._ordered_data:
            del self._ordered_data[key]
            if key in self:
                del self[key]
        return self

    def contains(self, key: str) -> bool:
        """检查是否包含某个参数"""
        return key in self._ordered_data

    def clear(self) -> "BodyMap":
        """清空所有参数"""
        self._ordered_data.clear()
        super().clear()
        return self

    def to_dict(self) -> Dict[str, Any]:
        """转换为普通字典"""
        return dict(self._ordered_data)

    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self._ordered_data, ensure_ascii=False)

    def to_url_params(self) -> str:
        """转换为URL参数字符串"""
        return urlencode(self._ordered_data, doseq=True)

    def encode_wechat_sign_params(self) -> str:
        """
        编码微信签名参数
        按照key的字母顺序排序,并拼接成字符串
        格式: key1=value1&key2=value2
        """
        sorted_params = sorted(self._ordered_data.items())
        return "&".join([f"{k}={v}" for k, v in sorted_params if v not in [None, ""]])

    def encode_alipay_sign_params(self) -> str:
        """
        编码支付宝签名参数
        按照key的字母顺序排序,并拼接成字符串
        """
        sorted_params = sorted(self._ordered_data.items())
        return "&".join([f"{k}={v}" for k, v in sorted_params if v not in [None, ""]])

    def filter_none(self) -> "BodyMap":
        """过滤值为None的参数"""
        filtered = {k: v for k, v in self._ordered_data.items() if v is not None and v != ""}
        self._ordered_data = OrderedDict(filtered)
        super().clear()
        super().update(filtered)
        return self

    def update(self, other: Union[Dict[str, Any], "BodyMap"]) -> "BodyMap":
        """更新参数"""
        if isinstance(other, BodyMap):
            self._ordered_data.update(other._ordered_data)
        else:
            self._ordered_data.update(other)
        super().update(self._ordered_data)
        return self

    def keys(self):
        """返回所有键"""
        return self._ordered_data.keys()

    def values(self):
        """返回所有值"""
        return self._ordered_data.values()

    def items(self):
        """返回所有键值对"""
        return self._ordered_data.items()

    def __len__(self) -> int:
        return len(self._ordered_data)

    def __repr__(self) -> str:
        return f"BodyMap({dict(self._ordered_data)})"

    def __str__(self) -> str:
        return json.dumps(self._ordered_data, ensure_ascii=False, indent=2)


class XmlMap(dict):
    """
    XML映射类
    用于微信支付等需要XML格式的场景
    """

    def __init__(self, root_name: str = "xml", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root_name = root_name
        self._data = OrderedDict()

    def set(self, key: str, value: Any) -> "XmlMap":
        """设置XML节点值"""
        if value is not None and value != "":
            self._data[key] = value
            self[key] = value
        return self

    def to_xml(self) -> str:
        """转换为XML字符串"""
        xml_parts = [f"<{self.root_name}>"]
        for key, value in self._data.items():
            # CDATA包裹特殊字符
            if isinstance(value, str) and any(c in value for c in ["<", ">", "&", "'"]):
                xml_parts.append(f"<{key}><![CDATA[{value}]]></{key}>")
            else:
                xml_parts.append(f"<{key}>{value}</{key}>")
        xml_parts.append(f"</{self.root_name}>")
        return "".join(xml_parts)

    @classmethod
    def from_xml(cls, xml_str: str, root_name: str = "xml") -> "XmlMap":
        """从XML字符串解析"""
        try:
            import xml.etree.ElementTree as ET

            root = ET.fromstring(xml_str)
            xml_map = cls(root_name=root_name)
            for child in root:
                xml_map.set(child.tag, child.text)
            return xml_map
        except Exception as e:
            raise ValueError(f"XML解析失败: {e}")

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return dict(self._data)


class ResponseData:
    """
    响应数据类
    统一封装各种支付渠道的响应
    """

    def __init__(
        self,
        success: bool,
        data: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        code: Optional[str] = None,
        raw_response: Optional[str] = None,
    ):
        self.success = success
        self.data = data or {}
        self.error = error
        self.code = code
        self.raw_response = raw_response

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "code": self.code,
            "raw_response": self.raw_response,
        }

    @classmethod
    def success_response(cls, data: Dict[str, Any], raw_response: Optional[str] = None) -> "ResponseData":
        """创建成功响应"""
        return cls(success=True, data=data, raw_response=raw_response)

    @classmethod
    def error_response(cls, error: str, code: Optional[str] = None, raw_response: Optional[str] = None) -> "ResponseData":
        """创建错误响应"""
        return cls(success=False, error=error, code=code, raw_response=raw_response)

    def __repr__(self) -> str:
        if self.success:
            return f"ResponseData(success=True, data={self.data})"
        return f"ResponseData(success=False, error={self.error}, code={self.code})"
