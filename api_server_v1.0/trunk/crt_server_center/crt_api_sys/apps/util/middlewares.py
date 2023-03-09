import re
import time

from urllib import parse
from sanic import Sanic
from sanic.log import logger
from contextvars import ContextVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sanic.response import json

from .redis_module import redis_factory
from .db_module import db_factory
from .authentication import check_token
from .err_code import ErrorCode

app = Sanic.get_app('crt_api_sys')

# _base_model_async_session_ctx = ContextVar("session")  # 存放全局db session


# _base_redis_conn_ctx = ContextVar("conn")  # 存放全局redis conn


@app.middleware("request")
async def start(request):
    logger.info('********************** Start **************************')
    logger.info(f'{request.ip} {request.method} {parse.unquote(request.url)}')
    if request.args:
        logger.info(f'args: {request.args}')
    if request.form:
        logger.info(f'form: {request.form}')
    elif request.json:
        logger.info(f'json: {request.json}')

    request.ctx.start_time = time.time()

    # request.ctx.async_session = sessionmaker(bind=db_factory.db_engine, class_=AsyncSession, expire_on_commit=False)()
    # request.ctx.async_session_ctx_token = _base_model_async_session_ctx.set(request.ctx.async_session)


#
#     # 创建redis conn
#     request.ctx.conn = await redis_factory.get_redis(apps.config.REDIS_POOL)
#     request.ctx.conn_ctx_token = _base_redis_conn_ctx.set(request.ctx.conn)


@app.middleware("request")
async def check_token_user(request):
    """
    检查token 并且 获取用户
    :param request:
    :return:
    """
    # token校验白名单
    white_list = [
        "/api/v1/login",
        "/api/v1/user",
        "/api/v1/basic_data/roles",
        "/api/v1/basic_data/device_type",
        "/api/v1/basic_data/picture_type",
        "/api/v1/basic_data/alarm_type",
        "/api/v1/basic_data/gb_evt_type",
        "/api/v1/basic_data/device_icons",
        "/api/v1/records/build_drawings",
        "/api/v1/records/files",
        "/api/v1/other/alarm_info",
        "/api/v1/other/drawing_assign",
        "/api/v1/other/alarm_logs",
        "/api/v1/other/help",
        "/api/v1/other/update_reset",
        "/api/v1/other/update_assign",
        "/api/v1/other/projects",
        "/api/v1/other/reset",
    ]
    regular_white_list = [
        "/api/v1/records/alarm_log/\\d+"
    ]

    is_regular = False
    for regular in regular_white_list:
        if re.match(regular, request.path):
            is_regular = True
            break

    if request.path not in white_list and not is_regular and 'static' not in request.path and request.method != 'OPTIONS':
        is_auth, authenticated = check_token(request)
        logger.info(f'check token: {is_auth}!!!')
        if not is_auth:
            code, msg = authenticated
            response_data = {
                'ok': False,
                'code': code,
                'msg': msg,
                'data': {}
            }
            return json(response_data, status=401)

        # toke格式 authenticated: {'user_id': 1, 'exp': 1807933539, 'sub': 'access'}
        user_id = authenticated.get("user_id")

        token = await redis_factory.get_string_cache(k=f'login:{user_id}', to_json=False)
        if request.token != token:
            code, msg = ErrorCode.AUTH_ERR_TOKEN_INVALID
            response_data = {
                'ok': False,
                'code': code,
                'msg': msg,
                'data': {}
            }
            return json(response_data, status=401)

        request.ctx.user_id = user_id


@app.middleware("response")
async def end(request, response):
    try:
        if response.content_type == 'application/json':
            body = response.body.decode('unicode-escape')
            logger.info(f"response: status {response.status} body {body}")
        else:
            logger.info(f"response: status {response.status} body {response.content_type}")
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


# @app.middleware("response")
# async def close_session(request, response):
#     """
#     关闭db session
#     :param request:
#     :param response:
#     :return:
#     """
#     if hasattr(request.ctx, "session_ctx_token"):
#         _base_model_async_session_ctx.reset(request.ctx.async_session_ctx_token)
#         await request.ctx.async_session.close()
#
#     # 关闭redis conn
#     if hasattr(request.ctx, "conn_ctx_token"):
#         _base_redis_conn_ctx.reset(request.ctx.conn_ctx_token)
#         await request.ctx.conn.close()
