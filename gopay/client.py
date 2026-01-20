"""
支付客户端抽象模块
遵循依赖倒置原则 - 定义支付客户端接口
遵循里氏替换原则 - 所有支付客户端可互换使用
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from gopay.config import PaymentConfig
from gopay.utils.datastructure import BodyMap, ResponseData


class PaymentClient(ABC):
    """
    支付客户端抽象基类
    定义所有支付客户端必须实现的接口
    """

    def __init__(self, config: PaymentConfig):
        """
        初始化支付客户端
        :param config: 支付配置
        """
        self.config = config
        config.validate()

    @abstractmethod
    def create_order(self, params: BodyMap) -> ResponseData:
        """
        创建订单
        :param params: 订单参数
        :return: 响应数据
        """
        pass

    @abstractmethod
    def query_order(self, order_no: str) -> ResponseData:
        """
        查询订单
        :param order_no: 订单号
        :return: 响应数据
        """
        pass

    @abstractmethod
    def close_order(self, order_no: str) -> ResponseData:
        """
        关闭订单
        :param order_no: 订单号
        :return: 响应数据
        """
        pass

    @abstractmethod
    def refund(self, order_no: str, refund_amount: float, **kwargs) -> ResponseData:
        """
        申请退款
        :param order_no: 订单号
        :param refund_amount: 退款金额
        :param kwargs: 其他参数
        :return: 响应数据
        """
        pass

    @abstractmethod
    def query_refund(self, refund_no: str) -> ResponseData:
        """
        查询退款
        :param refund_no: 退款单号
        :return: 响应数据
        """
        pass

    @abstractmethod
    def verify_notify(self, data: Dict[str, Any], signature: str) -> bool:
        """
        验证异步通知
        :param data: 通知数据
        :param signature: 签名
        :return: 是否验证通过
        """
        pass
