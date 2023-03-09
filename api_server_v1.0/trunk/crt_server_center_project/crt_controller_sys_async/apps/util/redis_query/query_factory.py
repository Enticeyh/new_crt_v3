import logging
import sys

from os.path import dirname, realpath
from redis import Redis
from rq import Queue, Worker
from logging.handlers import RotatingFileHandler

root_project_dir = dirname(dirname(dirname(dirname(realpath(__file__)))))
if root_project_dir not in sys.path:
    sys.path.append(root_project_dir)

# root_project_dir = dirname(dirname(realpath(__file__)))
# if root_project_dir not in sys.path:
#     sys.path.append(root_project_dir)


def logger_init(logger_name):
    logger = logging.getLogger(logger_name)
    # log_path = 'D:\\MyProject\\new_crt_v1.0\\api_server_v1.0\\trunk\\crt_server_center\\logs\\query.log'
    log_path = f'{dirname(root_project_dir)}/logs/celery.log)'
    # 日志文件处理器 单个日志文件最大可以50MB 最多保存10个日志文件 （保存最近500MB日志）
    file_handler = RotatingFileHandler(filename=log_path, maxBytes=1024 * 1024 * 50, backupCount=10, encoding="utf-8")
    # 日志文件记录的日志登录
    file_handler.setLevel(logging.INFO)
    # 日志文件中日志格式
    file_log_format = "%(asctime)s [%(process)d] [%(levelname)s] %(message)s"
    file_handler.setFormatter(logging.Formatter(file_log_format))
    logger.setLevel(logging.DEBUG)  # 控制台打印
    logger.addHandler(file_handler)
    return logger


class MyConfig:
    # 基本配置项
    LOGGER_LEVEL = logging.DEBUG

    # 加密秘钥
    SECRET = 'njzxaq123@'

    # common/redis_module 模块配置项
    # REDIS_URL = 'redis://:njzx20220512@127.0.0.1:6379/0'
    # REDIS_URL = 'redis://:@112.124.25.173:16379/0'
    REDIS_URL = 'redis://:@127.0.0.1:16379/0'
    REDIS_SHORT_EXPIRE = 10 * 60  # REDIS 短期超时时间
    REDIS_MEDIUM_EXPIRE = 30 * 60  # REDIS 中期超时时间
    REDIS_LONG_EXPIRE = 14 * 24 * 60 * 60  # REDIS 长期超时时间, web token
    REDIS_LONG_LONG_EXPIRE = 30 * 24 * 60 * 60  # REDIS 超长超时时间, apps token

    # MYSQL_URL = 'mysql+aiomysql://root:cnfire20220512@127.0.0.1/new_crt_v1'
    MYSQL_URL = 'mysql+aiomysql://root:123456@localhost:13306/crt_test'
    # MYSQL_URL = 'mysql+aiomysql://root:123456@112.124.25.173:13306/crt_test'


class QueryFactory:
    # redis_conn = Redis.from_url('redis://:@112.124.25.173:16379/3')
    redis_conn = Redis.from_url('redis://:@127.0.0.1:16379/3')
    query = Queue(connection=redis_conn)
    worker = Worker(queues=query, connection=redis_conn)

    from apps.util.db_module.sqlalchemy_factory import db_factory
    from apps.util.redis_module.redis_factory import redis_factory

    # redis初始化
    redis_factory.from_config(MyConfig)
    redis = redis_factory.connecting()
    # mysql初始化
    db_factory.from_config(MyConfig)

    # 日志器初始化
    logger = logger_init(logger_name='query')


query = QueryFactory.query
redis = QueryFactory.redis
