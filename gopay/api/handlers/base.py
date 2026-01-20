"""
API处理器基类
定义所有支付API处理器的统一接口

遵循SOLID原则:
- 单一职责(SRP): 每个处理器专注于一种支付渠道
- 开闭原则(OCP): 通过继承扩展功能
- 里氏替换(LSP): 所有处理器可互换使用
- 接口隔离(ISP): 定义最小接口
- 依赖倒置(DIP): 依赖抽象基类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable
import logging
import uuid
from datetime import datetime

from gopay.client import PaymentClient
from gopay.api.response import ApiResponse, ApiError


logger = logging.getLogger(__name__)


class BaseApiHandler(ABC):
    """
    API处理器基类

    定义所有支付API处理器的统一接口
    """

    def __init__(self, client: PaymentClient):
        """
        初始化处理器

        Args:
            client: 支付客户端实例
        """
        self.client = client
        self._hooks: Dict[str, list] = {}

    def _generate_trace_id(self) -> str:
        """
        生成追踪ID

        Returns:
            str: 追踪ID
        """
        return str(uuid.uuid4())

    def _get_timestamp(self) -> int:
        """
        获取当前时间戳

        Returns:
            int: 时间戳
        """
        return int(datetime.now().timestamp())

    def _execute_with_hooks(
        self,
        operation: str,
        func: Callable,
        *args,
        **kwargs
    ) -> ApiResponse:
        """
        执行操作并触发钩子

        Args:
            operation: 操作名称
            func: 要执行的函数
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            ApiResponse: 响应对象
        """
        trace_id = self._generate_trace_id()
        timestamp = self._get_timestamp()

        # 执行前置钩子
        self._execute_hooks(f"before_{operation}", trace_id, *args, **kwargs)

        try:
            # 执行主操作
            result = func(*args, **kwargs)

            # 执行成功钩子
            self._execute_hooks(f"after_{operation}", trace_id, result, True)

            # 添加追踪信息
            if isinstance(result, ApiResponse):
                result.trace_id = trace_id
                result.timestamp = timestamp

            return result

        except Exception as e:
            logger.error(f"操作失败: {operation}, 错误: {str(e)}", exc_info=True)

            # 执行失败钩子
            self._execute_hooks(f"after_{operation}", trace_id, str(e), False)

            # 返回错误响应
            return ApiResponse.server_error(str(e))

    def _execute_hooks(self, hook_name: str, *args, **kwargs):
        """
        执行钩子函数

        Args:
            hook_name: 钩子名称
            *args: 位置参数
            **kwargs: 关键字参数
        """
        if hook_name in self._hooks:
            for hook in self._hooks[hook_name]:
                try:
                    hook(*args, **kwargs)
                except Exception as e:
                    logger.error(f"钩子执行失败: {hook_name}, 错误: {str(e)}")

    def register_hook(self, event: str, hook: Callable):
        """
        注册钩子函数

        Args:
            event: 事件名称 (如: before_create_order, after_create_order)
            hook: 钩子函数
        """
        if event not in self._hooks:
            self._hooks[event] = []
        self._hooks[event].append(hook)

    @abstractmethod
    def create_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        创建订单

        Args:
            params: 订单参数

        Returns:
            ApiResponse: API响应
        """
        pass

    @abstractmethod
    def query_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        查询订单

        Args:
            params: 查询参数

        Returns:
            ApiResponse: API响应
        """
        pass

    @abstractmethod
    def close_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        关闭订单

        Args:
            params: 订单参数

        Returns:
            ApiResponse: API响应
        """
        pass

    @abstractmethod
    def refund(self, params: Dict[str, Any]) -> ApiResponse:
        """
        申请退款

        Args:
            params: 退款参数

        Returns:
            ApiResponse: API响应
        """
        pass

    @abstractmethod
    def query_refund(self, params: Dict[str, Any]) -> ApiResponse:
        """
        查询退款

        Args:
            params: 查询参数

        Returns:
            ApiResponse: API响应
        """
        pass

    def verify_notify(self, params: Dict[str, Any]) -> ApiResponse:
        """
        验证通知

        Args:
            params: 通知参数

        Returns:
            ApiResponse: API响应
        """
        return ApiResponse.not_found("Method not implemented")

    def cancel_order(self, params: Dict[str, Any]) -> ApiResponse:
        """
        撤销订单

        Args:
            params: 订单参数

        Returns:
            ApiResponse: API响应
        """
        return ApiResponse.not_found("Method not implemented")
