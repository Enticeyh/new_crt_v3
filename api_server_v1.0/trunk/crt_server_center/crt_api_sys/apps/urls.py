from sanic import Blueprint

from .views.authentication import Login, ShiftDuty, Logout, User, UpdateUser, CheckSuperPassword
from .views.basic_data import Roles, DeviceType, PictureType, AlarmType, GbEvtType, DeviceIcon
from .views.record import AlarmLogsList, AlarmLog, BuildDrawings, DeviceAssignLogsList, ControllerOpLogsList, \
    MaintenanceLogsList, ShiftRecordsList, SystemLogsList, Files
from .views.drawing import ProjectsList, ProjectPictures, Areas, Builds, Floors, Floor, Controllers, ControllersFile, \
    Devices, DevicesFile, AddressRelationship, CurrentRelationship, AssignDevice, AssignInheritance, Loops, QuickSvg
from .views.other import AlarmInfo, DrawingAssign, Reset, AlarmLogs, MockTest, SystemParam, Center, TestCenter, \
    SmartIotData, Backups, Upgrade, FactoryReset, UpdateReset, UpdateAssign, Help, Template, Projects, LastVersion, \
    Versions
from .views.test import TestRedis, TestMySql, Test


def routes(app):
    # 创建蓝图
    prefix, version = '/api/v', 1
    # authentication = Blueprint("authentication", url_prefix='/authentication')
    authentication = Blueprint("authentication", version_prefix=prefix, version=version)  # 权限
    basic_data = Blueprint("basic_data", url_prefix='/basic_data', version_prefix=prefix, version=version)  # 基础数据
    records = Blueprint("records", url_prefix='/records', version_prefix=prefix, version=version)  # 数据记录
    drawing = Blueprint("build_drawing", url_prefix='/build_drawing', version_prefix=prefix, version=version)  # 布点
    other = Blueprint("other", url_prefix='/other', version_prefix=prefix, version=version)  # 其他
    static = Blueprint("static", url_prefix=f'{prefix}{version}/static')  # 静态资源
    api = Blueprint.group(authentication, basic_data, records, drawing, other, static)  # 蓝图组
    # api = Blueprint.group(authentication, basic_data, records, drawing, other, version_prefix=prefix, version=version)
    # 注册蓝图
    app.blueprint(api)

    # 静态文件
    static.static("/audio", f"{app.config.STATIC_ROOT_PATH}/static/audio", name='audio')
    static.static("/icon_image", f"{app.config.STATIC_ROOT_PATH}/static/icon_image", name='icon_image')
    static.static("/other", f"{app.config.STATIC_ROOT_PATH}/static/other", name='other')
    static.static("/photo", f"{app.config.STATIC_ROOT_PATH}/static/photo", name='photo')
    static.static("/system_file", f"{app.config.STATIC_ROOT_PATH}/static/system_file", name='system_file')

    # 权限
    # * 登录
    authentication.add_route(Login.as_view(), "/login")
    # * 退出
    authentication.add_route(Logout.as_view(), "/logout")
    # * 换班
    authentication.add_route(ShiftDuty.as_view(), "/shift_duty")
    # * 查询用户
    authentication.add_route(User.as_view(), "/user")
    # * 新增用户 修改用户 删除用户
    authentication.add_route(UpdateUser.as_view(), "/update_user")
    # * 验证超级密码
    authentication.add_route(CheckSuperPassword.as_view(), "/check_super_password")

    # 基础数据
    # * 用户角色
    basic_data.add_route(Roles.as_view(), "/roles")
    # * 设备类型
    basic_data.add_route(DeviceType.as_view(), "/device_type")
    # * 图片类型
    basic_data.add_route(PictureType.as_view(), "/picture_type")
    # * 报警类型
    basic_data.add_route(AlarmType.as_view(), "/alarm_type")
    # * 国标事件类型
    basic_data.add_route(GbEvtType.as_view(), "/gb_evt_type")
    # * 设备图标
    basic_data.add_route(DeviceIcon.as_view(), "/device_icons")

    # 记录数据
    # * 设备报警记录列表
    records.add_route(AlarmLogsList.as_view(), "/alarm_logs")
    # * 单条报警记录
    records.add_route(AlarmLog.as_view(), "/alarm_log/<alarm_log_id>")
    # * 图纸（楼层 图纸和楼层绑定）
    records.add_route(BuildDrawings.as_view(), "/build_drawings")
    # * 设备布点记录
    records.add_route(DeviceAssignLogsList.as_view(), "/device_assign_logs")
    # * 控制器操作记录
    records.add_route(ControllerOpLogsList.as_view(), "/controller_op_logs")
    # * 维保记录
    records.add_route(MaintenanceLogsList.as_view(), "/maintenance_logs")
    # * 换班记录
    records.add_route(ShiftRecordsList.as_view(), "/shift_records")
    # * 系统操作记录
    records.add_route(SystemLogsList.as_view(), "/system_logs")
    # * 文件查询
    records.add_route(Files.as_view(), "/files")

    # 布点相关
    # * 项目
    drawing.add_route(ProjectsList.as_view(), "/projects")
    # * 项目图片
    drawing.add_route(ProjectPictures.as_view(), "/project_pictures")
    # * 小区
    drawing.add_route(Areas.as_view(), "/areas")
    # * 楼宇
    drawing.add_route(Builds.as_view(), "/builds")
    # * 楼层
    drawing.add_route(Floors.as_view(), "/floors")
    # * 单个楼层
    drawing.add_route(Floor.as_view(), "/floor/<floor_id>")
    # * 控制器
    drawing.add_route(Controllers.as_view(), "/controllers")
    # * 控制器文件上传
    drawing.add_route(ControllersFile.as_view(), "/controllers_file")
    # * 设备
    drawing.add_route(Devices.as_view(), "/devices")
    # * 设备文件上传
    drawing.add_route(DevicesFile.as_view(), "/devices_file")
    # * 回路号
    drawing.add_route(Loops.as_view(), "/loops")
    # * 地址关系
    drawing.add_route(AddressRelationship.as_view(), "/address_relationship")
    # * 位置源关系
    drawing.add_route(CurrentRelationship.as_view(), "/current_relationship")
    # * 布点
    drawing.add_route(AssignDevice.as_view(), "/assign_devices")
    # * 布点继承
    drawing.add_route(AssignInheritance.as_view(), "/assign_inheritance")
    # * 生成快速svg
    drawing.add_route(QuickSvg.as_view(), "/quick_svg")

    # 其他
    # * 最新报警总数
    other.add_route(AlarmInfo.as_view(), "/alarm_info")
    # * 布点信息
    other.add_route(DrawingAssign.as_view(), "/drawing_assign")
    # * 复位
    other.add_route(Reset.as_view(), "/reset")
    # * 报警队列
    other.add_route(AlarmLogs.as_view(), "/alarm_logs")
    # * 模拟测试
    other.add_route(MockTest.as_view(), "/mock_test")
    # * 系统参数（查询和修改）
    other.add_route(SystemParam.as_view(), "/system_param")
    # * 监管中心（查询、修改、删除）
    other.add_route(Center.as_view(), "/center")
    # * 测试监管中心
    other.add_route(TestCenter.as_view(), "/test_center")
    # * 数据导出
    other.add_route(SmartIotData.as_view(), "/smart_iot_data")
    # * 系统备份
    other.add_route(Backups.as_view(), "/backups")
    # * 数据导入和系统升级
    other.add_route(Upgrade.as_view(), "/upgrade")
    # * 一键恢复出厂
    other.add_route(FactoryReset.as_view(), "/factory_reset")
    # * 重置复位状态
    other.add_route(UpdateReset.as_view(), "/update_reset")
    # * 重置首页拉取报警图纸状态
    other.add_route(UpdateAssign.as_view(), "/update_assign")
    # * help
    other.add_route(Help.as_view(), "/help")
    # * template
    other.add_route(Template.as_view(), "/template")
    # * 全部项目信息
    other.add_route(Projects.as_view(), "/projects")
    # * 查询最新版本信息
    other.add_route(LastVersion.as_view(), "/last_version")
    # * 全部所有版本信息
    other.add_route(Versions.as_view(), "/versions")

    other.add_route(Test.as_view(), "/test")
    other.add_route(TestRedis.as_view(), "/test_redis")
    other.add_route(TestMySql.as_view(), "/test_mysql")
