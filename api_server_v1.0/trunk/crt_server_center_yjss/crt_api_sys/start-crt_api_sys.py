import sys
import logging
import platform

from sanic.log import logger
from os.path import dirname, realpath

from server import make_app

root_project_dir = dirname(dirname(realpath(__file__)))
if root_project_dir not in sys.path:
    sys.path.append(root_project_dir)


def init_logger(LOGFILE_LOGGER_LEVEL):
    # 日志器日志格式
    log_format = "[%(asctime)s] [%(process)d] [%(levelname)s] [%(filename)s-%(lineno)d] %(message)s"
    formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S %z")

    if logger.hasHandlers():
        logger.handlers[0].setFormatter(formatter)  # 修改默认日志器的日志格式

    logger.setLevel(LOGFILE_LOGGER_LEVEL)  # 控制台打印


def main():
    from crt_api_sys.apps.config import default_config
    cfg_class = default_config['base']

    app = make_app(cfg_class)

    # 初始化日志器
    init_logger(cfg_class.LOGFILE_LOGGER_LEVEL)

    # 执行初始化脚本
    from crt_api_sys.apps.util.boot_script import boot_init

    if platform.system() == 'Linux':
        # Linux, 创建多进程处理请求
        import multiprocessing
        workers = multiprocessing.cpu_count()
    else:
        # window, 单进程处理请求
        workers = 1

    # app.run(host='0.0.0.0', port=8000, workers=workers, access_log=True, debug=True)
    # app.run(host='0.0.0.0', port=8000, workers=workers, access_log=True, debug=False)
    app.run(host='0.0.0.0', port=8000, workers=workers, debug=False)

    # 执行初始化脚本
    # from crt_api_sys.apps.util.boot_script import boot_init
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(boot_init())


if __name__ == '__main__':
    main()
