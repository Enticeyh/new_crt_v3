from sanic import Sanic
from sanic.log import logger

APP_NAME = "crt_api_sys"


def check_config(cfg_class):
    if not hasattr(cfg_class, 'REDIS_URL'):
        raise ValueError('crt_api_sys, 请正确配置 REDIS_URL 配置项')

    if not hasattr(cfg_class, 'MYSQL_URL'):
        raise ValueError('crt_api_sys, 请正确配置 MYSQL_URL 配置项')

    logger.info(f'crt_api_sys config >>>')
    logger.info(f'REDIS_URL: {cfg_class.REDIS_URL}')
    logger.info(f'MYSQL_URL: {cfg_class.MYSQL_URL}')
    logger.info(f' <<<')


def make_app(cfg_class):
    app = Sanic('crt_api_sys')

    # 初始化
    # * 配置redis
    from crt_api_sys.apps.util.redis_module import redis_factory
    redis_factory.from_config(cfg_class)  # redis初始化

    # 配置mysql
    from crt_api_sys.apps.util.db_module import db_factory
    # engine配置项
    engine_options = {
        "pool_recycle": 1800,
        "pool_pre_ping": True,
    }
    # session配置项
    session_options = {}
    db_factory.from_config(cfg_class, engine_options=engine_options, session_options=session_options)

    # 配置串口工具 用于传输灯
    from crt_api_sys.apps.util.serial_model import serial_factory
    serial_factory.from_config(cfg_class)

    # 加载中间件
    from crt_api_sys.apps.util import middlewares

    # * 检查配置项
    check_config(cfg_class)
    # * 加载配置项
    app.update_config(cfg_class)
    app.config.RESPONSE_TIMEOUT = 600

    # 创建蓝图和路由
    from crt_api_sys.apps.urls import routes
    routes(app)
    logger.info(f'all routers >>>')
    for route in app.router.routes_all.values():
        logger.info(f'URL_PATH: {route.uri}, URL_METHODS: {route.methods}')
    logger.info(f' <<<')

    return app
