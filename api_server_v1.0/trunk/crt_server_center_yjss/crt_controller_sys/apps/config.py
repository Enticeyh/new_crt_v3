import logging

from attrdict import AttrDict


class Config:
    # 基本配置项
    LOGFILE_LOGGER_LEVEL = logging.INFO
    TERMINAL_LOGGER_LEVEL = logging.DEBUG

    # 加密秘钥
    SECRET = 'njzxaq123@'

    # common/redis_module 模块配置项
    # REDIS_URL = 'redis://:njzx20220512@127.0.0.1:6379/0'
    # REDIS_URL = 'redis://:redis123@112.124.25.173:16379/0'
    REDIS_URL = 'redis://:redis123@127.0.0.1:16379/0'
    REDIS_SHORT_EXPIRE = 10 * 60  # REDIS 短期超时时间 单位：秒
    REDIS_MEDIUM_EXPIRE = 30 * 60  # REDIS 中期超时时间 单位：秒
    REDIS_LONG_EXPIRE = 14 * 24 * 60 * 60  # REDIS 长期超时时间, web token 单位：秒
    REDIS_LONG_LONG_EXPIRE = 30 * 24 * 60 * 60  # REDIS 超长超时时间, apps token 单位：秒

    # MYSQL_URL = 'mysql+pymysql://root:cnfire20220512@127.0.0.1/new_crt_v1'
    # MYSQL_URL = 'mysql+pymysql://root:123456@localhost:13306/crt_test'
    MYSQL_URL = 'mysql+pymysql://root:123456@127.0.0.1:13316/new_crt_yjss'
    # MYSQL_URL = 'mysql+pymysql://root:123456@112.124.25.173:13306/crt_test'

    # celery相关
    BROKER_URL = 'redis://:redis123@127.0.0.1:16379/3'
    BACKEND_URL = 'redis://:redis123@127.0.0.1:16379/3'
    # BROKER_URL = 'redis://:@112.124.25.173:16379/3'
    # BACKEND_URL = 'redis://:@112.124.25.173:16379/3'
    CELERY_TIMEZONE = 'Asia/Shanghai'  # 时区
    CELERY_IS_UTC = False  # 是否使用UTC
    CELERY_RESULT_EXPIRES = 60 * 60  # 任务过期时间

    # 控制器相关
    REDIS_HEARTBEAT_TIME = 2 * 60  # 控制器心跳过期时间 单位：秒

    # 智慧消防相关地址
    CENTER_TEST_URL = "http://%s:%s/te-0/v1/testEvents"
    CENTER_HEART_URL = "http://%s:%s/te-0/v1/heartbeatEvents"
    CENTER_REPORT_URL = "http://%s:%s/te-1/v1/alarmEvents"
    CONTROLLER_OP_URL = "http://%s:%s/te-1/v1/operationEvents"
    CONTROLLER_STATE_URL = "http://%s:%s/te-1/v1/controllerStateEvents"
    GATEWAY_TIMEOUT = 5  # 网关请求过期时间 单位：秒
    REDIS_GATEWAY_TIME = 5 * 60  # 网关心跳过期时间 单位：秒

    # 雪花id相关
    WORKER_ID = 1  # 机器id

    # 新版控制器ip 端口
    CONTROLLER_URL = "http://%s:%s/cf/api/v1/crt/%s"
    CONTROLLER_HOST = "192.168.8.102"
    CONTROLLER_PORT = "8013"


class CrtConfig:
    # 基本配置项
    LOGFILE_LOGGER_LEVEL = logging.INFO
    TERMINAL_LOGGER_LEVEL = logging.DEBUG

    # 加密秘钥
    SECRET = 'njzxaq123@'

    # common/redis_module 模块配置项
    REDIS_URL = 'redis://:njzx20220512@127.0.0.1:6379/0'
    REDIS_SHORT_EXPIRE = 10 * 60  # REDIS 短期超时时间 单位：秒
    REDIS_MEDIUM_EXPIRE = 30 * 60  # REDIS 中期超时时间 单位：秒
    REDIS_LONG_EXPIRE = 14 * 24 * 60 * 60  # REDIS 长期超时时间, web token 单位：秒
    REDIS_LONG_LONG_EXPIRE = 30 * 24 * 60 * 60  # REDIS 超长超时时间, apps token 单位：秒

    MYSQL_URL = 'mysql+pymysql://root:cnfire20220512@127.0.0.1:3306/new_crt'

    # celery相关
    BROKER_URL = 'redis://:njzx20220512@127.0.0.1:6379/3'
    BACKEND_URL = 'redis://:njzx20220512@127.0.0.1:6379/3'
    # BROKER_URL = 'redis://:@112.124.25.173:16379/3'
    # BACKEND_URL = 'redis://:@112.124.25.173:16379/3'
    CELERY_TIMEZONE = 'Asia/Shanghai'  # 时区
    CELERY_IS_UTC = False  # 是否使用UTC
    CELERY_RESULT_EXPIRES = 60 * 60  # 任务过期时间

    # 控制器相关
    REDIS_HEARTBEAT_TIME = 2 * 60  # 控制器心跳过期时间 单位：秒

    # 智慧消防相关地址
    CENTER_TEST_URL = "http://%s:%s/te-0/v1/testEvents"
    CENTER_HEART_URL = "http://%s:%s/te-0/v1/heartbeatEvents"
    CENTER_REPORT_URL = "http://%s:%s/te-1/v1/alarmEvents"
    CONTROLLER_OP_URL = "http://%s:%s/te-1/v1/operationEvents"
    CONTROLLER_STATE_URL = "http://%s:%s/te-1/v1/controllerStateEvents"
    GATEWAY_TIMEOUT = 5  # 网关请求过期时间 单位：秒
    REDIS_GATEWAY_TIME = 5 * 60  # 网关心跳过期时间 单位：秒

    # 雪花id相关
    WORKER_ID = 1  # 机器id

    # 新版控制器ip 端口
    CONTROLLER_URL = "http://%s:%s/cf/api/v1/crt/%s"
    CONTROLLER_HOST = "192.168.8.102"
    CONTROLLER_PORT = "8013"


default_config = AttrDict({
    'base': Config,
    'crt': CrtConfig,
})
