"""
数据结构测试
"""

import pytest
from gopay.utils.datastructure import BodyMap, XmlMap, ResponseData


class TestBodyMap:
    """BodyMap测试"""

    def test_create_body_map(self):
        """测试创建BodyMap"""
        body = BodyMap()
        assert body is not None
        assert len(body) == 0

    def test_set_and_get(self):
        """测试设置和获取值"""
        body = BodyMap()
        body.set("key1", "value1")
        body.set("key2", "value2")

        assert body.get("key1") == "value1"
        assert body.get("key2") == "value2"
        assert len(body) == 2

    def test_filter_none(self):
        """测试过滤None值"""
        body = BodyMap()
        body.set("key1", "value1")
        body.set("key2", None)
        body.set("key3", "")
        body.set("key4", "value4")

        assert body.get("key1") == "value1"
        assert body.get("key2") is None
        assert body.get("key3") is None
        assert len(body) == 2  # 只有key1和key4

    def test_chain_call(self):
        """测试链式调用"""
        body = BodyMap()
        result = body.set("key1", "value1").set("key2", "value2").set("key3", "value3")

        assert result is body  # 返回自身
        assert len(body) == 3

    def test_to_dict(self):
        """测试转换为字典"""
        body = BodyMap()
        body.set("key1", "value1")
        body.set("key2", "value2")

        data = body.to_dict()
        assert isinstance(data, dict)
        assert data["key1"] == "value1"
        assert data["key2"] == "value2"

    def test_to_json(self):
        """测试转换为JSON"""
        body = BodyMap()
        body.set("key1", "value1")
        body.set("key2", "value2")

        json_str = body.to_json()
        assert isinstance(json_str, str)
        assert "key1" in json_str
        assert "value1" in json_str

    def test_to_url_params(self):
        """测试转换为URL参数"""
        body = BodyMap()
        body.set("key1", "value1")
        body.set("key2", "value2")

        url_params = body.to_url_params()
        assert isinstance(url_params, str)
        assert "key1=value1" in url_params
        assert "key2=value2" in url_params

    def test_encode_wechat_sign_params(self):
        """测试编码微信签名参数"""
        body = BodyMap()
        body.set("c_key", "value3")
        body.set("a_key", "value1")
        body.set("b_key", "value2")

        params_str = body.encode_wechat_sign_params()
        assert params_str == "a_key=value1&b_key=value2&c_key=value3"

    def test_encode_alipay_sign_params(self):
        """测试编码支付宝签名参数"""
        body = BodyMap()
        body.set("c_key", "value3")
        body.set("a_key", "value1")
        body.set("b_key", "value2")

        params_str = body.encode_alipay_sign_params()
        assert params_str == "a_key=value1&b_key=value2&c_key=value3"

    def test_remove(self):
        """测试移除参数"""
        body = BodyMap()
        body.set("key1", "value1")
        body.set("key2", "value2")

        body.remove("key1")
        assert body.get("key1") is None
        assert body.get("key2") == "value2"
        assert len(body) == 1

    def test_clear(self):
        """测试清空参数"""
        body = BodyMap()
        body.set("key1", "value1")
        body.set("key2", "value2")

        body.clear()
        assert len(body) == 0

    def test_update(self):
        """测试更新参数"""
        body = BodyMap()
        body.set("key1", "value1")

        body.update({"key2": "value2", "key3": "value3"})
        assert len(body) == 3
        assert body.get("key2") == "value2"

    def test_contains(self):
        """测试检查参数是否存在"""
        body = BodyMap()
        body.set("key1", "value1")

        assert body.contains("key1") is True
        assert body.contains("key2") is False


class TestXmlMap:
    """XmlMap测试"""

    def test_create_xml_map(self):
        """测试创建XmlMap"""
        xml_map = XmlMap()
        assert xml_map is not None

    def test_set_and_to_xml(self):
        """测试设置值和转换为XML"""
        xml_map = XmlMap()
        xml_map.set("key1", "value1")
        xml_map.set("key2", "value2")

        xml_str = xml_map.to_xml()
        assert "<xml>" in xml_str
        assert "<key1>value1</key1>" in xml_str
        assert "<key2>value2</key2>" in xml_str
        assert "</xml>" in xml_str

    def test_cdata_encoding(self):
        """测试CDATA编码"""
        xml_map = XmlMap()
        xml_map.set("key1", "value with <special> chars")
        xml_map.set("key2", "value with & ampersand")

        xml_str = xml_map.to_xml()
        assert "<![CDATA[" in xml_str

    def test_from_xml(self):
        """测试从XML解析"""
        xml_str = "<xml><key1>value1</key1><key2>value2</key2></xml>"
        xml_map = XmlMap.from_xml(xml_str)

        assert xml_map.get("key1") == "value1"
        assert xml_map.get("key2") == "value2"

    def test_to_dict(self):
        """测试转换为字典"""
        xml_map = XmlMap()
        xml_map.set("key1", "value1")
        xml_map.set("key2", "value2")

        data = xml_map.to_dict()
        assert isinstance(data, dict)
        assert data["key1"] == "value1"
        assert data["key2"] == "value2"


class TestResponseData:
    """ResponseData测试"""

    def test_success_response(self):
        """测试成功响应"""
        data = {"key1": "value1", "key2": "value2"}
        response = ResponseData.success_response(data)

        assert response.success is True
        assert response.data == data
        assert response.error is None

    def test_error_response(self):
        """测试错误响应"""
        response = ResponseData.error_response("error message", "ERR001")

        assert response.success is False
        assert response.error == "error message"
        assert response.code == "ERR001"

    def test_to_dict(self):
        """测试转换为字典"""
        data = {"key1": "value1"}
        response = ResponseData.success_response(data)

        response_dict = response.to_dict()
        assert response_dict["success"] is True
        assert response_dict["data"] == data

    def test_repr(self):
        """测试字符串表示"""
        success_response = ResponseData.success_response({"key": "value"})
        error_response = ResponseData.error_response("error", "ERR001")

        success_str = repr(success_response)
        error_str = repr(error_response)

        assert "success=True" in success_str
        assert "success=False" in error_str
        assert "error" in error_str
