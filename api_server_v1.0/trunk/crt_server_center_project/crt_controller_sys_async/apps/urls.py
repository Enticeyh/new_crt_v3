from sanic import Blueprint

from .views.old_controller import AdjustTime, Reports, DeviceOperateInfo, Heartbeats


def routes(app):

    old_controller = Blueprint("old_controller", url_prefix='/api/v1_0')  # 旧版控制器http上报接口
    new_controller = Blueprint("new_controller")  # 新版控制器http上报接口
    collect = Blueprint.group(old_controller, new_controller)  # 蓝图组
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
