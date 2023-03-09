from sanic import Sanic
from sanic.log import logger
from sanic.http import Http
from sanic.compat import Header
from sanic.exceptions import HeaderExpectationFailed, InvalidUsage, PayloadTooLarge


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

APP_NAME = "crt_controller_sys"


def check_config(cfg_class):
    if not hasattr(cfg_class, 'REDIS_URL'):
        raise ValueError('crt_controller_sys, 请正确配置 REDIS_URL 配置项')

    if not hasattr(cfg_class, 'MYSQL_URL'):
        raise ValueError('crt_controller_sys, 请正确配置 MYSQL_URL 配置项')

    if not hasattr(cfg_class, 'WORKER_ID'):
        raise ValueError('crt_controller_sys, 请正确配置 WORKER_ID 配置项')

    logger.info(f'crt_controller_sys config >>>')
    logger.info(f'REDIS_URL: {cfg_class.REDIS_URL}')
    logger.info(f'MYSQL_URL: {cfg_class.MYSQL_URL}')
    logger.info(f'WORKER_ID: {cfg_class.WORKER_ID}')
    logger.info(f' <<<')


def make_app(cfg_class):
    app = Sanic('crt_controller_sys')

    # 初始化
    # * 配置redis
    from crt_controller_sys.apps.util.redis_module import redis_factory
    redis_factory.from_config(cfg_class)  # redis初始化

    # 配置mysql
    from crt_controller_sys.apps.util.db_module import db_factory
    # engine配置项
    engine_options = {
        "pool_recycle": 1800,
        "pool_pre_ping": True,
    }
    # session配置项
    session_options = {}
    db_factory.from_config(cfg_class, engine_options=engine_options, session_options=session_options)

    # 配置雪花id
    from crt_controller_sys.apps.util.snowflakeid import snow_fake_factory
    snow_fake_factory.from_config(cfg_class)

    # 加载中间件
    from crt_controller_sys.apps.util import middlewares

    # * 检查配置项
    check_config(cfg_class)
    # * 加载配置项
    from crt_controller_sys.apps.config import Config
    app.update_config(Config)  # 通用配置
    app.update_config(cfg_class)  # 特别配置
    app.config.RESPONSE_TIMEOUT = 600

    # 创建蓝图和路由
    from crt_controller_sys.apps.urls import routes
    routes(app)
    logger.info(f'all routers >>>')
    for route in app.router.routes_all.values():
        logger.info(f'URL_PATH: {route.uri}, URL_METHODS: {route.methods}')
    logger.info(f' <<<')

    return app
