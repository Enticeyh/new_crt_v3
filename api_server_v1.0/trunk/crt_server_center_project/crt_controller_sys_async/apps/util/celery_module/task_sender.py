from crt_controller_sys_async.apps.util.celery_module.tasks import controller_adjust_time, controller_report_info


def adjust_time(device_num):
    """控制器时间校准"""
    controller_adjust_time.delay(device_num)


def report_info(data):
    """控制器时间上报"""
    controller_report_info.delay(data)
