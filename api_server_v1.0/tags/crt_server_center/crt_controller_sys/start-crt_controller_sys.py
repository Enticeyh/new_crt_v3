# import os
import sys
import logging
import platform

from sanic.log import logger
from os.path import dirname, realpath
# from logging.handlers import RotatingFileHandler

from server import make_app

root_project_dir = dirname(dirname(realpath(__file__)))
if root_project_dir not in sys.path:
    sys.path.append(root_project_dir)


def init_logger(LOGFILE_LOGGER_LEVEL, TERMINAL_LOGGER_LEVEL):
    # 日志器日志格式
    log_format = "[%(asctime)s] [%(process)d] [%(levelname)s] [%(filename)s-%(lineno)d] %(message)s"
    formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S %z")

    if logger.hasHandlers():
        logger.handlers[0].setFormatter(formatter)  # 修改默认日志器的日志格式

    logger.setLevel(LOGFILE_LOGGER_LEVEL)  # 控制台打印

    # log_path = f'{root_project_dir}/logs/crt_controller_sys.log'
    # file_handler = logging.FileHandler(filename=log_path, encoding="utf-8")
    # 日志文件处理器 单个日志文件最大可以50MB 最多保存10个日志文件 （保存最近500MB日志）
    # file_handler = RotatingFileHandler(filename=log_path, maxBytes=1024 * 1024 * 50, backupCount=10, encoding="utf-8")
    # 日志文件记录的日志登录
    # file_handler.setLevel(TERMINAL_LOGGER_LEVEL)
    # 日志文件中日志格式
    # file_handler.setFormatter(formatter)
    # 日志处理器添加到日志器
    # root_logger.addHandler(file_handler)


def main():
    from crt_controller_sys.apps.config import default_config
    cfg_class = default_config['base']

    app = make_app(cfg_class)

    init_logger(cfg_class.LOGFILE_LOGGER_LEVEL, cfg_class.TERMINAL_LOGGER_LEVEL)

    if platform.system() == 'Linux':
        # Linux, 创建多进程处理请求
        import multiprocessing
        workers = multiprocessing.cpu_count()
    else:
        # window, 单进程处理请求
        workers = 1

    app.run(host='0.0.0.0', port=5000, workers=workers, debug=False)

    # import os
    # 启动worker
    # worker = 'celery -A crt_controller_sys.apps.util.celery_module.celery_factory.celery_app worker -l info -P gevent'
    # os.system(worker)
    # 启动定时任务
    # time = 'celery -A crt_controller_sys.apps.util.celery_module.celery_factory.celery_app beat -l info'
    # os.system(time)


if __name__ == '__main__':
    main()
