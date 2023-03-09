import logging


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
