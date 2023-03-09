from crt_controller_sys.apps.util.celery_module.tasks import controller_adjust_time, controller_report, \
    old_controller_report, old_controller_operate, controller_heartbeats, check_reset_error_data, \
    controller_evt_synchronous, new_controller_state, new_controller_alarm, new_controller_operate


def send_controller_adjust_time(device_num):
    """控制器时间校准"""
    controller_adjust_time.s(device_num).apply_async(priority=10)


def send_controller_report(data):
    """控制器时间上报"""
    controller_report.s(data).apply_async(priority=10)


def send_old_controller_report(data):
    """老版控制器事件上报"""
    old_controller_report.s(data).apply_async(priority=10)


def send_old_controller_operate(data):
    """老版控制器操作上报"""
    old_controller_operate.s(data).apply_async(priority=10)


def send_controller_heartbeats():
    """控制器心跳上报"""
    controller_heartbeats.apply_async(priority=10)


def send_new_controller_state(data):
    """新版控制器最新状态同步（心跳)"""
    # new_controller_state.apply_async(kwargs={'state': data}, priority=1)
    new_controller_state.s(data).apply_async(priority=10)


def send_new_controller_alarm(data):
    """新版控制器报警事件采集"""
    new_controller_alarm.s(data).apply_async(priority=10)


def send_new_controller_operate(data):
    """新版控制器操作事件采集"""
    new_controller_operate.s(data).apply_async(priority=10)


def send_check_reset_error_data():
    """检测因复位引起的错误数据"""
    check_reset_error_data.apply_async(priority=10)


def send_controller_evt_synchronous():
    """首页复位误删数据同步"""
    controller_evt_synchronous.apply_async(priority=10)
