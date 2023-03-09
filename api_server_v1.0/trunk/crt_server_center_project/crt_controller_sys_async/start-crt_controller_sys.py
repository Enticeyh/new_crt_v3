import platform
import sys

from os.path import dirname, realpath

from server import make_app

root_project_dir = dirname(realpath(__file__))
if root_project_dir not in sys.path:
    sys.path.append(root_project_dir)


def main():
    # 启动worker
    # celery -A crt_controller_sys_async.apps.util.celery_module.celery_factory.celery_app worker -l info -P gevent
    # 启动定时任务
    # os.system('celery -A crt_controller_sys_async.apps.util.celery_module.celery_factory.celery_app beat -l info')

    app = make_app()

    if platform.system() == 'Linux':
        # Linux, 创建多进程处理请求
        import multiprocessing
        workers = multiprocessing.cpu_count()
    else:
        # window, 单进程处理请求
        workers = 1

    app.run(host='0.0.0.0', port=5000, workers=workers, debug=False)


if __name__ == '__main__':
    main()
