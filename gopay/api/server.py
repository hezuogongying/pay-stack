"""
支付API服务器
提供HTTP REST API接口,将支付功能对外提供服务

遵循SOLID原则:
- 单一职责(SRP): 专注于API服务器的启动和路由管理
- 开闭原则(OCP): 通过注册处理器扩展功能
- 里氏替换(LSP): 可替换为其他Web框架实现
- 接口隔离(ISP): 提供最小必要接口
- 依赖倒置(DIP): 依赖抽象的处理器
"""

import logging
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

from gopay.api.handlers.aggregated import AggregatedPayHandler
from gopay.api.handlers.base import BaseApiHandler
from gopay.api.middleware import MiddlewareChain
from gopay.api.response import ApiResponse


logger = logging.getLogger(__name__)


class ApiServerBase(ABC):
    """
    API服务器基类

    定义API服务器的抽象接口
    """

    def __init__(self):
        """初始化API服务器"""
        self.aggregated_handler = AggregatedPayHandler()
        self.middleware_chain = MiddlewareChain()

    @abstractmethod
    def register_payment_channel(self, channel: str, handler: BaseApiHandler):
        """
        注册支付渠道

        Args:
            channel: 支付渠道标识
            handler: API处理器实例
        """
        pass

    @abstractmethod
    def start(self, host: str = "0.0.0.0", port: int = 8000):
        """
        启动服务器

        Args:
            host: 监听地址
            port: 监听端口
        """
        pass

    @abstractmethod
    def stop(self):
        """停止服务器"""
        pass


class PayApiServer(ApiServerBase):
    """
    支付API服务器

    提供HTTP REST API接口,支持多种Web框架
    """

    def __init__(self, framework: str = "flask"):
        """
        初始化支付API服务器

        Args:
            framework: Web框架类型 (flask, fastapi等)
        """
        super().__init__()
        self.framework = framework.lower()
        self.app = None
        self._server = None

        if self.framework == "flask":
            self._init_flask()
        elif self.framework == "fastapi":
            self._init_fastapi()
        else:
            raise ValueError(f"不支持的Web框架: {framework}")

    def _init_flask(self):
        """初始化Flask应用"""
        try:
            from flask import Flask, request, jsonify

            self.app = Flask(__name__)

            @self.app.route("/api/v1/pay/create_order", methods=["POST"])
            @self.middleware_chain.apply
            def create_order():
                data = request.get_json()
                channel = data.get("channel")
                params = data.get("params", {})
                result = self.aggregated_handler.create_order(channel, params)
                return jsonify(result.to_dict())

            @self.app.route("/api/v1/pay/query_order", methods=["POST"])
            @self.middleware_chain.apply
            def query_order():
                data = request.get_json()
                channel = data.get("channel")
                params = data.get("params", {})
                result = self.aggregated_handler.query_order(channel, params)
                return jsonify(result.to_dict())

            @self.app.route("/api/v1/pay/close_order", methods=["POST"])
            @self.middleware_chain.apply
            def close_order():
                data = request.get_json()
                channel = data.get("channel")
                params = data.get("params", {})
                result = self.aggregated_handler.close_order(channel, params)
                return jsonify(result.to_dict())

            @self.app.route("/api/v1/pay/refund", methods=["POST"])
            @self.middleware_chain.apply
            def refund():
                data = request.get_json()
                channel = data.get("channel")
                params = data.get("params", {})
                result = self.aggregated_handler.refund(channel, params)
                return jsonify(result.to_dict())

            @self.app.route("/api/v1/pay/query_refund", methods=["POST"])
            @self.middleware_chain.apply
            def query_refund():
                data = request.get_json()
                channel = data.get("channel")
                params = data.get("params", {})
                result = self.aggregated_handler.query_refund(channel, params)
                return jsonify(result.to_dict())

            @self.app.route("/api/v1/pay/cancel_order", methods=["POST"])
            @self.middleware_chain.apply
            def cancel_order():
                data = request.get_json()
                channel = data.get("channel")
                params = data.get("params", {})
                result = self.aggregated_handler.cancel_order(channel, params)
                return jsonify(result.to_dict())

            @self.app.route("/api/v1/health", methods=["GET"])
            def health():
                return jsonify(ApiResponse.success({"status": "ok"}).to_dict())

            @self.app.route("/api/v1/channels", methods=["GET"])
            def channels():
                channels = self.aggregated_handler.supported_channels()
                return jsonify(ApiResponse.success(channels).to_dict())

            logger.info("Flask应用初始化成功")

        except ImportError:
            raise ImportError("Flask未安装,请运行: pip install flask")

    def _init_fastapi(self):
        """初始化FastAPI应用"""
        try:
            from fastapi import FastAPI
            from fastapi.responses import JSONResponse
            from pydantic import BaseModel

            self.app = FastAPI(title="GoPay Payment API", version="1.0.0")

            class PaymentRequest(BaseModel):
                channel: str
                params: Dict[str, Any]

            @self.app.post("/api/v1/pay/create_order")
            @self.middleware_chain.apply
            async def create_order(request: PaymentRequest):
                result = self.aggregated_handler.create_order(request.channel, request.params)
                return JSONResponse(content=result.to_dict())

            @self.app.post("/api/v1/pay/query_order")
            @self.middleware_chain.apply
            async def query_order(request: PaymentRequest):
                result = self.aggregated_handler.query_order(request.channel, request.params)
                return JSONResponse(content=result.to_dict())

            @self.app.post("/api/v1/pay/close_order")
            @self.middleware_chain.apply
            async def close_order(request: PaymentRequest):
                result = self.aggregated_handler.close_order(request.channel, request.params)
                return JSONResponse(content=result.to_dict())

            @self.app.post("/api/v1/pay/refund")
            @self.middleware_chain.apply
            async def refund(request: PaymentRequest):
                result = self.aggregated_handler.refund(request.channel, request.params)
                return JSONResponse(content=result.to_dict())

            @self.app.post("/api/v1/pay/query_refund")
            @self.middleware_chain.apply
            async def query_refund(request: PaymentRequest):
                result = self.aggregated_handler.query_refund(request.channel, request.params)
                return JSONResponse(content=result.to_dict())

            @self.app.post("/api/v1/pay/cancel_order")
            @self.middleware_chain.apply
            async def cancel_order(request: PaymentRequest):
                result = self.aggregated_handler.cancel_order(request.channel, request.params)
                return JSONResponse(content=result.to_dict())

            @self.app.get("/api/v1/health")
            async def health():
                result = ApiResponse.success({"status": "ok"})
                return JSONResponse(content=result.to_dict())

            @self.app.get("/api/v1/channels")
            async def channels():
                channels = self.aggregated_handler.supported_channels()
                result = ApiResponse.success(channels)
                return JSONResponse(content=result.to_dict())

            logger.info("FastAPI应用初始化成功")

        except ImportError:
            raise ImportError("FastAPI未安装,请运行: pip install fastapi uvicorn")

    def register_payment_channel(self, channel: str, handler: BaseApiHandler):
        """
        注册支付渠道

        Args:
            channel: 支付渠道标识
            handler: API处理器实例
        """
        self.aggregated_handler.register_handler(channel, handler)
        logger.info(f"注册支付渠道: {channel}")

    def add_middleware(self, middleware) -> "PayApiServer":
        """
        添加中间件

        Args:
            middleware: 中间件实例

        Returns:
            PayApiServer: 返回自身以支持链式调用
        """
        self.middleware_chain.add(middleware)
        return self

    def start(self, host: str = "0.0.0.0", port: int = 8000, **kwargs):
        """
        启动服务器

        Args:
            host: 监听地址
            port: 监听端口
            **kwargs: 其他参数
        """
        if self.framework == "flask":
            self._start_flask(host, port, **kwargs)
        elif self.framework == "fastapi":
            self._start_fastapi(host, port, **kwargs)

    def _start_flask(self, host: str, port: int, **kwargs):
        """启动Flask服务器"""
        debug = kwargs.get("debug", False)
        self.app.run(host=host, port=port, debug=debug)

    def _start_fastapi(self, host: str, port: int, **kwargs):
        """启动FastAPI服务器"""
        import uvicorn
        uvicorn.run(self.app, host=host, port=port, **kwargs)

    def stop(self):
        """停止服务器"""
        if self._server:
            self._server.shutdown()
            logger.info("服务器已停止")

    def get_app(self):
        """
        获取应用实例

        Returns:
            Flask或FastAPI应用实例
        """
        return self.app
