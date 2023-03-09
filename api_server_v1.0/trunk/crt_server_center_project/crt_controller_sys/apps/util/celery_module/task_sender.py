from crt_controller_sys.apps.util.celery_module.tasks import controller_adjust_time, controller_report, \
    old_controller_report, old_controller_operate, controller_heartbeats, check_reset_error_data, \
    controller_evt_synchronous


def send_controller_adjust_time(device_num):
    """控制器时间校准"""
    controller_adjust_time.delay(device_num)


def send_controller_report(data):
    """控制器时间上报"""
    controller_report.delay(data)


def send_old_controller_report(data):
    """控制器事件上报"""
    old_controller_report.delay(data)


def send_old_controller_operate(data):
    """控制器操作上报"""
    old_controller_operate.delay(data)


def send_controller_heartbeats():
    """控制器心跳上报"""
    controller_heartbeats.delay()


def send_check_reset_error_data():
    """检测因复位引起的错误数据"""
    check_reset_error_data.delay()


def send_controller_evt_synchronous():
    """首页复位误删数据同步"""
    controller_evt_synchronous.delay()
