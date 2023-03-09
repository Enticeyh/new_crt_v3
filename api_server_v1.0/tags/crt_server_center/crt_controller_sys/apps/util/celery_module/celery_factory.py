import os
import sys
import logging

from celery import Celery
from datetime import timedelta
from os.path import dirname, realpath
# from logging.handlers import RotatingFileHandler
from celery.signals import after_setup_logger

root_project_dir = dirname(dirname(dirname(dirname(dirname(realpath(__file__))))))
if root_project_dir not in sys.path:
    sys.path.append(root_project_dir)

logger = logging.getLogger(__name__)


@after_setup_logger.connect
def init_logger(*args, **kwargs):
    logger = logging.getLogger()
    # 日志器日志格式
    log_format = "[%(asctime)s] [%(process)d] [%(levelname)s] [%(filename)s-%(lineno)d] %(message)s"
    formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S %z")

    if logger.hasHandlers():
        logger.handlers[0].setFormatter(formatter)  # 修改默认日志器的日志格式

    logger.setLevel(logging.INFO)  # 控制台打印


class CeleryFactory:
    celery_app = Celery()
    from crt_controller_sys.apps.util.snowflakeid import snow_fake_factory
    from crt_controller_sys.apps.util.redis_module import redis_factory
    from crt_controller_sys.apps.util.db_module import db_factory
    from crt_controller_sys.apps.config import default_config
    cfg_class = default_config['base']

    # 日志器初始化
    init_logger(cfg_class.LOGFILE_LOGGER_LEVEL, cfg_class.TERMINAL_LOGGER_LEVEL)

    # 配置雪花id
    snow_fake_factory.from_config(cfg_class)
    # redis初始化
    redis_factory.from_config(cfg_class)
    conn = redis_factory.get_redis()
    # mysql初始化
    # engine配置项
    engine_options = {
        "pool_recycle": 1800,
        "pool_pre_ping": True,
    }
    # session配置项
    session_options = {}
    db_factory.from_config(cfg_class, engine_options=engine_options, session_options=session_options)

    @classmethod
    def set_config(cls):
        # 优先级
        cls.celery_app.CELERY_ACKS_LATE = True,
        cls.celery_app.CELERYD_PREFETCH_MULTIPLIER = 8,

        cls.celery_app.conf.broker_url = cls.cfg_class.BROKER_URL
        cls.celery_app.conf.backend_url = cls.cfg_class.BACKEND_URL

        # 注册任务
        cls.celery_app.conf.imports = ('crt_controller_sys.apps.util.celery_module.tasks',)

        # 时区
        cls.celery_app.conf.timezone = cls.cfg_class.CELERY_TIMEZONE
        # 是否使用UTC
        cls.celery_app.conf.enable_utc = cls.cfg_class.CELERY_IS_UTC
        # 任务过期时间
        cls.celery_app.conf.result_expires = cls.cfg_class.CELERY_RESULT_EXPIRES

        # 任务的定时配置
        cls.celery_app.conf.beat_schedule = {
            # 定时检测控制器心跳时间是否过期
            'check_controller_heartbeats': {
                'task': 'crt_controller_sys.apps.util.celery_module.tasks.check_controller_heartbeats',
                'schedule': timedelta(seconds=2 * 60),
            },
            # 如果配置智慧消防 定时向智慧消防发送心跳 响应成功更新智慧消防过期时间 如果没有配置 默认更新心跳时间
            'center_heartbeats': {
                'task': 'crt_controller_sys.apps.util.celery_module.tasks.center_heartbeats',
                'schedule': timedelta(seconds=3 * 60),
            },
            # 定时检测智慧消防是否过期
            'check_center_heartbeats': {
                'task': 'crt_controller_sys.apps.util.celery_module.tasks.check_center_heartbeats',
                'schedule': timedelta(seconds=6 * 60),
            },
            # 定时检测有无因复位问题导致的错误数据
            'check_reset_error_data': {
                'task': 'crt_controller_sys.apps.util.celery_module.tasks.check_reset_error_data',
                'schedule': timedelta(seconds=6 * 60 * 60),
            },
            # 定时查询新版控制器状态数据
            # 'select_controller_status': {
            #     'task': 'crt_controller_sys.apps.util.celery_module.tasks.check_controller_status',
            #     'schedule': timedelta(seconds=3),
            # },
            # can数据采集
            'can_data_acquisition': {
                'task': 'crt_controller_sys.apps.util.celery_module.tasks.can_data_acquisition',
                'schedule': timedelta(seconds=3),
            },
            # 队列更新报警统计
            'read_and_update_alarm_info': {
                'task': 'crt_controller_sys.apps.util.celery_module.tasks.read_and_update_alarm_info',
                'schedule': timedelta(seconds=3),
            },
            # 定时检查或清除报警记录、控制器操作记录、系统操作记录
            'update_alarm_info': {
                'task': 'crt_controller_sys.apps.util.celery_module.tasks.check_and_update_logs',
                'schedule': timedelta(hours=24),
            },
        }

        logger.info(f'celery config >>>')
        logger.info(f'broker_url: {cls.celery_app.conf.broker_url}')
        logger.info(f'backend_url: {cls.celery_app.conf.backend_url}')
        logger.info(f' <<<')


celery_factory = CeleryFactory
celery_factory.set_config()
celery_app = CeleryFactory.celery_app
conn = CeleryFactory.conn
cfg_class = CeleryFactory.cfg_class

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
