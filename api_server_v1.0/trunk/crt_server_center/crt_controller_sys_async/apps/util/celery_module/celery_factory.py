import os
import sys
import time
import logging
import asyncio

from os.path import dirname, realpath
from datetime import timedelta
from celery.schedules import crontab
from celery import Celery, loaders
from celery.loaders.app import AppLoader
from logging.handlers import RotatingFileHandler

root_project_dir = dirname(dirname(dirname(dirname(realpath(__file__)))))
if root_project_dir not in sys.path:
    sys.path.append(root_project_dir)


def logger_init(logger_name):
    logger = logging.getLogger(logger_name)
    # log_path = 'D:\\MyProject\\new_crt_v1.0\\api_server_v1.0\\trunk\\crt_server_center\\logs\\celery.log'
    log_path = f'{dirname(root_project_dir)}/logs/celery.log'
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


logger = logger_init(logger_name='worker')


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


class CeleryLoader(AppLoader):
    def on_worker_process_init(self):
        asyncio.set_event_loop(asyncio.new_event_loop())


class ThreadLoop:
    loop_pool = {}


class CeleryFactory:
    # celery_app = Celery(loader=CeleryLoader)
    celery_app = Celery()

    from apps.util.redis_module import redis_factory
    from apps.util.db_module import db_factory
    # redis初始化
    redis_factory.from_config(MyConfig)
    redis = redis_factory.connecting()
    # mysql初始化
    db_factory.from_config(MyConfig)

    @classmethod
    def set_config(cls):
        cls.celery_app.conf.broker_url = 'redis://:@127.0.0.1:16379/3'
        cls.celery_app.conf.backend_url = 'redis://:@127.0.0.1:16379/3'
        # cls.celery_app.conf.broker_url = 'redis://:@112.124.25.173:16379/3'
        # cls.celery_app.conf.backend_url = 'redis://:@112.124.25.173:16379/3'

        # 注册任务
        cls.celery_app.conf.imports = ('crt_controller_sys_async.apps.util.celery_module.tasks',)

        # 时区
        cls.celery_app.conf.timezone = 'Asia/Shanghai'
        # 是否使用UTC
        cls.celery_app.conf.enable_utc = False
        # 任务过期时间
        cls.celery_app.conf.result_expires = 60 * 60

        # 任务的定时配置
        cls.celery_app.conf.beat_schedule = {
            'add_task': {
                'task': 'crt_controller_sys_async.apps.util.celery_module.tasks.timing_task',
                'schedule': timedelta(seconds=3),
                # 'schedule': crontab(hour=8, day_of_week=1),  # 每周一早八点
                'args': (30, 20),  # 参数
            },
        }

        logger.info(f'celery config >>>')
        logger.info(f'broker_url: {cls.celery_app.conf.broker_url}')
        logger.info(f'backend_url: {cls.celery_app.conf.backend_url}')
        logger.info(f' <<<')


celery_factory = CeleryFactory
celery_factory.set_config()
celery_app = CeleryFactory.celery_app
redis = CeleryFactory.redis
loop_pool = ThreadLoop.loop_pool


if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
