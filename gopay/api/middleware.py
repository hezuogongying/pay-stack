"""
API中间件模块
提供认证、日志、错误处理等中间件功能

遵循SOLID原则:
- 单一职责(SRP): 每个中间件专注于单一功能
- 开闭原则(OCP): 可扩展新的中间件
- 里氏替换(LSP): 中间件可互换
- 接口隔离(ISP): 最小接口
- 依赖倒置(DIP): 依赖抽象接口
"""

import logging
import time
from typing import Callable, Optional, Dict, Any
from functools import wraps


logger = logging.getLogger(__name__)


class ErrorHandler:
    """
    错误处理中间件

    遵循单一职责原则(SRP): 只负责错误捕获和转换
    """

    @staticmethod
    def handle(func: Callable) -> Callable:
        """
        错误处理装饰器

        Args:
            func: 要装饰的函数

        Returns:
            Callable: 装饰后的函数
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"错误: {str(e)}", exc_info=True)
                from gopay.api.response import ApiResponse
                return ApiResponse.server_error(str(e))

        return wrapper


class AuthMiddleware:
    """
    认证中间件

    遵循单一职责原则(SRP): 只负责认证验证
    """

    def __init__(self, api_keys: Optional[list] = None):
        """
        初始化认证中间件

        Args:
            api_keys: 允许的API密钥列表
        """
        self.api_keys = set(api_keys or [])

    def add_api_key(self, key: str):
        """
        添加API密钥

        Args:
            key: API密钥
        """
        self.api_keys.add(key)

    def remove_api_key(self, key: str):
        """
        移除API密钥

        Args:
            key: API密钥
        """
        if key in self.api_keys:
            self.api_keys.remove(key)

    def verify(self, api_key: str) -> bool:
        """
        验证API密钥

        Args:
            api_key: API密钥

        Returns:
            bool: 是否有效
        """
        return api_key in self.api_keys

    def authenticate(self, func: Callable) -> Callable:
        """
        认证装饰器

        Args:
            func: 要装饰的函数

        Returns:
            Callable: 装饰后的函数
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 从kwargs中获取api_key
            api_key = kwargs.pop("api_key", None)

            if not api_key:
                from gopay.api.response import ApiResponse
                return ApiResponse.unauthorized("缺少API密钥")

            if not self.verify(api_key):
                from gopay.api.response import ApiResponse
                return ApiResponse.unauthorized("无效的API密钥")

            return func(*args, **kwargs)

        return wrapper


class LoggingMiddleware:
    """
    日志中间件

    遵循单一职责原则(SRP): 只负责日志记录
    """

    def __init__(self, log_level: int = logging.INFO):
        """
        初始化日志中间件

        Args:
            log_level: 日志级别
        """
        self.log_level = log_level

    def log_request(self, operation: str, params: Dict[str, Any]):
        """
        记录请求日志

        Args:
            operation: 操作名称
            params: 请求参数
        """
        logger.log(self.log_level, f"请求: {operation}, 参数: {params}")

    def log_response(self, operation: str, response, duration: float):
        """
        记录响应日志

        Args:
            operation: 操作名称
            response: 响应对象
            duration: 耗时(秒)
        """
        from gopay.api.response import ApiResponse

        if isinstance(response, ApiResponse):
            logger.log(
                self.log_level,
                f"响应: {operation}, 状态码: {response.code}, 耗时: {duration:.3f}s"
            )

    def log(self, func: Callable) -> Callable:
        """
        日志装饰器

        Args:
            func: 要装饰的函数

        Returns:
            Callable: 装饰后的函数
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            operation = func.__name__
            params = kwargs

            self.log_request(operation, params)

            start_time = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start_time

            self.log_response(operation, result, duration)

            return result

        return wrapper


class RateLimiter:
    """
    限流中间件

    遵循单一职责原则(SRP): 只负责请求限流
    """

    def __init__(self, max_requests: int = 100, window: int = 60):
        """
        初始化限流器

        Args:
            max_requests: 时间窗口内最大请求数
            window: 时间窗口(秒)
        """
        self.max_requests = max_requests
        self.window = window
        self._requests: Dict[str, list] = {}

    def _clean_old_requests(self, key: str):
        """
        清理过期请求记录

        Args:
            key: 请求标识
        """
        current_time = time.time()
        if key in self._requests:
            # 移除超过时间窗口的请求
            self._requests[key] = [
                req_time for req_time in self._requests[key]
                if current_time - req_time < self.window
            ]

    def is_allowed(self, key: str = "default") -> bool:
        """
        检查是否允许请求

        Args:
            key: 请求标识(如:API密钥、IP地址)

        Returns:
            bool: 是否允许
        """
        self._clean_old_requests(key)

        if key not in self._requests:
            self._requests[key] = []

        if len(self._requests[key]) >= self.max_requests:
            return False

        self._requests[key].append(time.time())
        return True

    def check_rate_limit(self, func: Callable) -> Callable:
        """
        限流装饰器

        Args:
            func: 要装饰的函数

        Returns:
            Callable: 装饰后的函数
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            api_key = kwargs.get("api_key", "default")

            if not self.is_allowed(api_key):
                from gopay.api.response import ApiResponse
                return ApiResponse.error("请求过于频繁,请稍后再试", "429")

            return func(*args, **kwargs)

        return wrapper


class MiddlewareChain:
    """
    中间件链

    遵循单一职责原则(SRP): 负责中间件的链式管理
    """

    def __init__(self):
        """初始化中间件链"""
        self._middlewares = []

    def add(self, middleware) -> "MiddlewareChain":
        """
        添加中间件

        Args:
            middleware: 中间件实例

        Returns:
            MiddlewareChain: 返回自身以支持链式调用
        """
        self._middlewares.append(middleware)
        return self

    def apply(self, func: Callable) -> Callable:
        """
        应用所有中间件到函数

        Args:
            func: 要装饰的函数

        Returns:
            Callable: 装饰后的函数
        """
        # 按照相反的顺序应用中间件
        # 这样第一个添加的中间件会最外层执行
        for middleware in reversed(self._middlewares):
            if hasattr(middleware, "handle"):
                func = middleware.handle(func)
            elif hasattr(middleware, "authenticate"):
                func = middleware.authenticate(func)
            elif hasattr(middleware, "log"):
                func = middleware.log(func)
            elif hasattr(middleware, "check_rate_limit"):
                func = middleware.check_rate_limit(func)

        return func
