from sanic import Blueprint

from .views.old_controller import AdjustTime, Reports, DeviceOperateInfo, Heartbeats
from .views.new_controller import UpdateStateApi, AlarmReportsApi, OperateReportsApi
from .views.other import CheckResetErrorData, GetSnowId, ControllerEvtSynchronous
from .views.test import TestRedis, TestMySql


def routes(app):

    old_controller = Blueprint("old_controller", url_prefix='/api/v1_0')  # 旧版控制器http上报接口
    new_controller = Blueprint("new_controller", url_prefix='/api/v1_0/new')  # 新版控制器http上报接口
    other = Blueprint("other", url_prefix='/api/v1_0/other')  # 其他
    test = Blueprint("test", url_prefix='/api/v1_0/test')  # 测试
    collect = Blueprint.group(old_controller, new_controller, other, test)  # 蓝图组
    # 注册蓝图
    app.blueprint(collect)

    # 旧版控制器http接口
    # * 时间校准
    old_controller.add_route(AdjustTime.as_view(), "/adjust_time")
    # * 控制器信息上报
    old_controller.add_route(Reports.as_view(), "/reports")
    # * 控制操作信息上报
    old_controller.add_route(DeviceOperateInfo.as_view(), "/device_operate_info")
    # * 心跳
    old_controller.add_route(Heartbeats.as_view(), "/heartbeats")

    # 新版控制器http接口
    # * 系统状态上报接口（心跳接口）
    new_controller.add_route(UpdateStateApi.as_view(), "/update_state_api")
    # * 控制器报警事件上报
    new_controller.add_route(AlarmReportsApi.as_view(), "/alarm_reports_api")
    # * 控制器操作事件上报
    new_controller.add_route(OperateReportsApi.as_view(), "/operate_reports_api")

    # * 获取雪花id
    other.add_route(GetSnowId.as_view(), "/get_snow_id")
    # * 检查复位错误数据
    other.add_route(CheckResetErrorData.as_view(), "/check_reset_error_data")
    # * 首页复位误删数据同步
    other.add_route(ControllerEvtSynchronous.as_view(), "/controller_evt_synchronous")

    test.add_route(TestRedis.as_view(), "/test_redis")
    test.add_route(TestMySql.as_view(), "/test_mysql")
