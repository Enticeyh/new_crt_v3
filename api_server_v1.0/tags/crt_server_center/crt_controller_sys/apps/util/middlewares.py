import time

from urllib import parse
from sanic import Sanic
from sanic.log import logger
from contextvars import ContextVar
from sqlalchemy.orm import sessionmaker

from .db_module import db_factory

app = Sanic.get_app('crt_controller_sys')

_base_model_session_ctx = ContextVar("session")  # 存放全局db session


# _base_redis_conn_ctx = ContextVar("conn")  # 存放全局redis conn


@app.middleware("request")
async def start(request):
    logger.info('********************** Start **************************')
    logger.info(f'{request.ip} {request.method} {parse.unquote(request.url)}')
    request.ctx.start_time = time.time()


@app.middleware("request")
async def create_session(request):
    """
    创建 db session
    :param request:
    :return:
    """
    request.ctx.session = sessionmaker(bind=db_factory.db_engine, expire_on_commit=False)()
    request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)

#     # 创建redis conn
#     request.ctx.conn = await redis_factory.get_redis(apps.config.REDIS_POOL)
#     request.ctx.conn_ctx_token = _base_redis_conn_ctx.set(request.ctx.conn)


@app.middleware("response")
async def end(request, response):
    try:
        body = response.body.decode('unicode-escape') if response.content_type == 'application/json' else response.body
        logger.info(f"response: status {response.status} body {body}")
    except Exception as e:
        logger.error(e)
        logger.info(f"{response.status} {response.body}")
    request_handle_time = time.time() - request.ctx.start_time
    logger.info(f'request handle consume: {request_handle_time}s !!!')
    logger.info('********************** End **************************')


@app.middleware("response")
async def add_cors_headers(request, response):
    """
    配置CORS请求头
    :param request:
    :param response:
    :return:
    """
    if request.method != "OPTIONS" and request.route:
        methods = [method for method in request.route.methods]
        allow_methods = list(set(methods))
        if "OPTIONS" not in allow_methods:
            allow_methods.append("OPTIONS")
        headers = {
            "Access-Control-Allow-Methods": ",".join(allow_methods),
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": (
                "origin, content-type, accept, "
                "authorization, x-xsrf-token, x-request-id"
            ),
        }
        response.headers.extend(headers)


@app.middleware("response")
async def close_session(request, response):
    """
    关闭db session
    :param request:
    :param response:
    :return:
    """
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        request.ctx.session.close()
#
#     # 关闭redis conn
#     if hasattr(request.ctx, "conn_ctx_token"):
#         _base_redis_conn_ctx.reset(request.ctx.conn_ctx_token)
#         await request.ctx.conn.close()
