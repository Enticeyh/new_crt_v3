import logging

from attrdict import AttrDict
from os.path import dirname, realpath


class Config:
    # 基本配置项
    LOGFILE_LOGGER_LEVEL = logging.INFO
    TERMINAL_LOGGER_LEVEL = logging.DEBUG

    # 加密秘钥
    SECRET = 'njzxaq123@'

    # 过期时间
    REDIS_SHORT_EXPIRE = 10 * 60  # REDIS 短期超时时间
    REDIS_MEDIUM_EXPIRE = 30 * 60  # REDIS 中期超时时间
    REDIS_LONG_EXPIRE = 14 * 24 * 60 * 60  # REDIS 长期超时时间, web token
    REDIS_LONG_LONG_EXPIRE = 30 * 24 * 60 * 60  # REDIS 超长超时时间, apps token

    REDIS_TOKEN_EXPIRE = REDIS_LONG_LONG_EXPIRE  # token过期时间

    # 静态文件路径
    STATIC_ROOT_PATH = f'{dirname(realpath(__file__))}'

    # 项目路径
    ROOT_PATH = f'{dirname(dirname(dirname(realpath(__file__))))}'

    # 采集端
    REPORTS_URL = 'http://127.0.0.1:5000/api/v1_0/reports'
    SNOW_ID_URL = 'http://127.0.0.1:5000/api/v1_0/other/get_snow_id'
    CHECK_RESET_ERROR_DATA_URL = 'http://127.0.0.1:5000/api/v1_0/other/check_reset_error_data'
    CONTROLLER_EVT_SYNCHRONOUS_URL = 'http://127.0.0.1:5000/api/v1_0/other/controller_evt_synchronous'

    # 智慧消防相关地址
    CENTER_TEST_URL = "http://%s:%s/te-0/v1/testEvents"

    # 网络请求过期时间
    HTTP_TIMEOUT = 5

    # 超级用户 超级密码 async_load_user_by_user_id也有一个写死的SUPER_USERNAME
    SUPER_USERNAME = "super"
    # 超级管理员密码规则为<SUPER_PASSWORD>_<year>-<month>（如superpassword_2022-8） md5加密后 取第6位到第11位（共6位）
    SUPER_PASSWORD = "superpassword"

    # 使用说明地址
    HELP_PATH = "/static/system_file/help.pdf"
    # 设备数据导入模板地址
    DEVICE_TEMPLATE_PATH = "/static/system_file/device.xls"
    # 控制器数据导入模板地址
    CONTROLLER_TEMPLATE_PATH = "/static/system_file/controller.xls"

    # 默认楼宇图片地址
    BUILD_IMAGE_PATH = "/static/system_file/build.jpg"

    # 声光设备device_type  10: 1代火灾声光警报器  127: 2代火灾声光警报器  308: Lora无线声光警报器
    VL_DEVICE_TYPES = [10, 127, 308]

    # 新crt设备 传输灯串口信息
    SERIAL_PORT = "/dev/ttyS2"
    SERIAL_BPS = 9600
    SERIAL_TIMEOUT = 5

    # 版本号
    VERSION = "3.0.6"


class BaseConfig(Config):
    # REDIS_URL = 'redis://:njzx20220512@127.0.0.1:6379/0'
    # REDIS_URL = 'redis://:njzx20220512@192.168.5.252:6379/0'
    # REDIS_URL = 'redis://:redis123@112.124.25.173:16379/0'
    REDIS_URL = 'redis://:redis123@127.0.0.1:16379/0'

    # MYSQL_URL = 'mysql+aiomysql://root:cnfire20220512@127.0.0.1/new_crt_v1'
    # MYSQL_URL = 'mysql+aiomysql://cnfire:njzx20220512@192.168.5.252/new_crt'
    # MYSQL_URL = 'mysql+aiomysql://root:123456@127.0.0.1:13306/crt_test'
    MYSQL_URL = 'mysql+aiomysql://root:123456@127.0.0.1:13316/new_crt'
    # MYSQL_URL = 'mysql+aiomysql://root:123456@112.124.25.173:13306/crt_test'

    # 默认导出路径和备份路径
    EXPORT_PATH = "/mnt/d/Desktop/导出数据".encode().decode('utf8')
    BACKUPS_PATH = "/mnt/d/Desktop/备份数据".encode().decode('utf8')


class WebConfig(Config):
    REDIS_URL = 'redis://:redis123@127.0.0.1:16379/0'

    MYSQL_URL = 'mysql+aiomysql://root:123456@localhost:13306/new_crt'

    # 默认导出路径和备份路径
    EXPORT_PATH = "/root/project/new_crt/导出数据".encode().decode('utf8')
    BACKUPS_PATH = "/root/project/new_crt/备份数据".encode().decode('utf8')


class CrtConfig(Config):
    # common/redis_module 模块配置项
    REDIS_URL = 'redis://:njzx20220512@127.0.0.1:6379/0'

    MYSQL_URL = 'mysql+aiomysql://root:cnfire20220512@127.0.0.1:3306/new_crt'

    # 默认导出路径和备份路径
    EXPORT_PATH = "/home/nanjingcrt/Desktop/导出数据".encode().decode('utf8')
    BACKUPS_PATH = "/home/nanjingcrt/Desktop/备份数据".encode().decode('utf8')


default_config = AttrDict({
    'base': BaseConfig,
    'web': WebConfig,
    'crt': CrtConfig,
})
