import logging

from sanic import Sanic
from sanic.log import logger
from sanic.http import Http
from sanic.exceptions import HeaderExpectationFailed, InvalidUsage, PayloadTooLarge
from sanic.compat import Header


class CustomHttp(Http):
    """自定义Http解析函数，替换http1_request_header"""

    async def custom_http1_request_header(self):  # no cov
        """
        Receive and parse request header into self.request.
        """
        # Receive until full header is in buffer
        buf = self.recv_buffer
        pos = 0

        while True:
            pos = buf.find(b"\r\n\r\n", pos)
            if pos != -1:
                break

            pos = max(0, len(buf) - 3)
            if pos >= self.HEADER_MAX_SIZE:
                break

            await self._receive_more()

        if pos >= self.HEADER_MAX_SIZE:
            raise PayloadTooLarge("Request header exceeds the size limit")

        # Parse header content
        try:
            head = buf[:pos]
            raw_headers = head.decode(errors="surrogateescape")

            reqline, *split_headers = raw_headers.split("\r\n")
            # http协议空格不规范分割时会出现错误
            # method, self.url, protocol = reqline.split(" ")
            method, self.url, protocol = reqline.split()
            print(method, self.url, protocol)
            await self.dispatch(
                "http.lifecycle.read_head",
                inline=True,
                context={"head": bytes(head)},
            )

            if protocol == "HTTP/1.1":
                self.keep_alive = True
            elif protocol == "HTTP/1.0":
                self.keep_alive = False
            else:
                raise Exception  # Raise a Bad Request on try-except

            self.head_only = method.upper() == "HEAD"
            request_body = False
            headers = []

            for name, value in (h.split(":", 1) for h in split_headers):
                name, value = h = name.lower(), value.lstrip()

                if name in ("content-length", "transfer-encoding"):
                    request_body = True
                elif name == "connection":
                    self.keep_alive = value.lower() == "keep-alive"

                headers.append(h)
        except Exception:
            raise InvalidUsage("Bad Request")

        headers_instance = Header(headers)
        self.upgrade_websocket = (
                headers_instance.getone("upgrade", "").lower() == "websocket"
        )

        # Prepare a Request object
        request = self.protocol.request_class(
            url_bytes=self.url.encode(),
            headers=headers_instance,
            head=bytes(head),
            version=protocol[5:],
            method=method,
            transport=self.protocol.transport,
            app=self.protocol.app,
        )
        await self.dispatch(
            "http.lifecycle.request",
            inline=True,
            context={"request": request},
        )

        # Prepare for request body
        self.request_bytes_left = self.request_bytes = 0
        if request_body:
            headers = request.headers
            expect = headers.getone("expect", None)

            if expect is not None:
                if expect.lower() == "100-continue":
                    self.expecting_continue = True
                else:
                    raise HeaderExpectationFailed(f"Unknown Expect: {expect}")

            if headers.getone("transfer-encoding", None) == "chunked":
                self.request_body = "chunked"
                pos -= 2  # One CRLF stays in buffer
            else:
                self.request_body = True
                self.request_bytes_left = self.request_bytes = int(
                    headers["content-length"]
                )

        # Remove header and its trailing CRLF
        del buf[: pos + 4]
        self.request, request.stream = request, self
        self.protocol.state["requests_count"] += 1


Http.http1_request_header = CustomHttp.custom_http1_request_header


APP_NAME = "crt_controller_sys_async"


def init_logger():
    log_path = '../logs/crt_controller_sys_async.log'
    # file_handler = logging.FileHandler(filename=log_path, encoding="utf-8")
    from logging.handlers import RotatingFileHandler
    # 日志文件处理器 单个日志文件最大可以50MB 最多保存10个日志文件 （保存最近500MB日志）
    file_handler = RotatingFileHandler(filename=log_path, maxBytes=1024 * 1024 * 50, backupCount=10, encoding="utf-8")
    # 日志文件记录的日志登录
    file_handler.setLevel(logging.INFO)
    # 日志文件中日志格式
    file_log_format = "%(asctime)s [%(process)d] [%(levelname)s] %(message)s"
    file_handler.setFormatter(logging.Formatter(file_log_format))

    # sanic 默认日志器
    root_logger = logging.getLogger('sanic.root')
    # root_logger.setLevel(logging.DEBUG)  # 控制台打印
    root_logger.setLevel(logging.INFO)  # 控制台打印
    root_logger.addHandler(file_handler)


def check_config(cfg_class):
    if not hasattr(cfg_class, 'REDIS_URL'):
        raise ValueError('crt_controller_sys_async, 请正确配置 REDIS_URL 配置项')

    if not hasattr(cfg_class, 'MYSQL_URL'):
        raise ValueError('crt_controller_sys_async, 请正确配置 MYSQL_URL 配置项')

    logger.info(f'crt_controller_sys_async config >>>')
    logger.info(f'REDIS_URL: {cfg_class.REDIS_URL}')
    logger.info(f'MYSQL_URL: {cfg_class.MYSQL_URL}')
    logger.info(f' <<<')


def make_app():
    app = Sanic('crt_controller_sys_async')

    # 初始化
    from apps.config import MyConfig
    from apps.urls import routes
    init_logger()

    # 加载中间件
    from apps.util import middlewares

    # * 检查配置项
    check_config(MyConfig)
    # * 加载配置项
    app.update_config(MyConfig)

    # * 配置redis
    from apps.util.redis_module import redis_factory
    redis_factory.from_config(MyConfig)  # redis初始化
    app.config.REDIS = redis_factory.connecting()  # 获取redis对象 redis连接由aioredis管理

    # 配置mysql
    from apps.util.db_module import db_factory
    engine_options = {}  # engine配置项
    session_options = {}  # session配置项
    db_factory.from_config(MyConfig, engine_options=engine_options, session_options=session_options)
    app.config.DB_ENGINE = db_factory.db_engine

    # 创建蓝图和路由
    routes(app)
    logger.debug(f'all routers >>>')
    for route in app.router.routes_all.values():
        logger.debug(f'URL_PATH: {route.uri}, URL_METHODS: {route.methods}')
    logger.debug(f' <<<')

    return app
