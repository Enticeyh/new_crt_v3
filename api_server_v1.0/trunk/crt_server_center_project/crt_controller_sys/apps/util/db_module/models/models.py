from datetime import date
from sqlalchemy import Column, String, DateTime, Float, Date
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, BIGINT

from ._base import BaseModel


class TabAlarmLog(BaseModel):
    __tablename__ = 'tab_alarm_log'
    __table_args__ = {'comment': '设备报警信息表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    is_clear = Column(TINYINT(1), nullable=False, server_default='0', comment='是否清除（已被清除的历史报警 0 否 1 是）')
    snow_id = Column(BIGINT, nullable=False, comment='雪花id')
    alarm_time = Column(DateTime, nullable=False, comment='控制器报警时间')
    description = Column(String(128), nullable=False, comment='报警描述')
    project_id = Column(INTEGER(11), nullable=False, comment='项目id')
    controller_id = Column(INTEGER(11), nullable=False, comment='控制器id')
    controller_num = Column(INTEGER(11), comment='控制器号')
    loop_num = Column(INTEGER(11), comment='回路号')
    addr_num = Column(INTEGER(11), comment='地址号')
    equipment_num = Column(INTEGER(11), comment='设备号')
    module_num = Column(INTEGER(11), comment='模块号')
    pass_num = Column(INTEGER(11), comment='通道号')
    device_type_id = Column(INTEGER(11), comment='设备类型id')
    device_type_name = Column(String(32), comment='设备类型名称')
    area_id = Column(INTEGER(11), comment='小区id')
    area_name = Column(String(32), comment='小区名称')
    build_id = Column(INTEGER(11), comment='楼宇id')
    build_name = Column(String(32), comment='楼宇名称')
    floor_id = Column(INTEGER(11), comment='楼层id')
    floor_name = Column(String(32), comment='楼层名称')
    device_id = Column(INTEGER(11), comment='报警设备id')
    alarm_type_id = Column(INTEGER(11), nullable=False, comment='报警类型id')
    alarm_type_name = Column(String(32), nullable=False, comment='报警类型名称')
    assign_status = Column(TINYINT(1), nullable=False, server_default='0', comment='布点状态（0 未布点 1 已布点）')
    alarm_status = Column(TINYINT(1), nullable=False, server_default='0', comment='报警状态 （0消失 1出现 2丢弃）')
    gb_evt_type_id = Column(INTEGER(11), comment='事件国标类型id')
    gb_evt_type_name = Column(String(32), comment='事件国标类型名称')
    alarm_type = Column(TINYINT(1), comment='报警类型（0 真实报警 1 模拟报警）')
    controller_report_id = Column(INTEGER(11), comment='新版控制器上报记录id')


class TabAlarmType(BaseModel):
    __tablename__ = 'tab_alarm_type'
    __table_args__ = {'comment': '报警类型表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    name = Column(String(32), nullable=False, comment='报警类型名称')


class TabArea(BaseModel):
    __tablename__ = 'tab_area'
    __table_args__ = {'comment': '小区表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    name = Column(String(128), nullable=False, comment='小区名称')
    project_id = Column(INTEGER(11), nullable=False, comment='项目id')
    project_name = Column(String(32), nullable=False, comment='项目名称')


class TabAssignDevice(BaseModel):
    __tablename__ = 'tab_assign_device'
    __table_args__ = {'comment': '设备布点表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    coordinate_X = Column(Float(asdecimal=True), nullable=False, server_default='0', comment='X轴坐标')
    coordinate_Y = Column(Float(asdecimal=True), nullable=False, server_default='0', comment='Y轴坐标')
    rate = Column(Float(asdecimal=True), nullable=False, comment='显示比例')
    angle = Column(INTEGER(11), server_default='0', comment='角度')
    width = Column(Float(asdecimal=True), nullable=False, comment='初始宽度')
    height = Column(Float(asdecimal=True), nullable=False, comment='初始高度')
    device_type_id = Column(INTEGER(11), nullable=False, comment='国标设备类型id')
    device_type_name = Column(String(32), nullable=False, comment='国标设备类型名称')
    path = Column(String(128), nullable=False, comment='图标地址')
    description = Column(String(128), nullable=False, comment='描述')
    device_status = Column(INTEGER(11), nullable=False, server_default='0', comment='设备状态（0 正常 其他国标事件码）')
    device_id = Column(INTEGER(11), nullable=False, comment='设备id')
    psn = Column(String(32), nullable=False, comment='设备编号')
    project_id = Column(INTEGER(11), nullable=False, comment='项目id')
    controller_id = Column(INTEGER(11), nullable=False, comment='控制器id')
    controller_num = Column(INTEGER(11), nullable=False, comment='控制器号')
    loop_num = Column(INTEGER(11), comment='回路号')
    addr_num = Column(INTEGER(11), comment='地址号')
    equipment_num = Column(INTEGER(11), comment='设备号')
    module_num = Column(INTEGER(11), comment='模块号')
    floor_id = Column(INTEGER(11), nullable=False, comment='楼层id')


class TabBuild(BaseModel):
    __tablename__ = 'tab_build'
    __table_args__ = {'comment': '楼宇信息'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    name = Column(String(32), nullable=False, comment='楼宇名称')
    path = Column(String(128), nullable=False, comment='图片地址')
    picture_type_id = Column(INTEGER(11), nullable=False, comment='图片类型id')
    picture_type_name = Column(String(32), nullable=False, comment='图片类型名称')
    area_id = Column(INTEGER(11), nullable=False, comment='小区id')
    area_name = Column(String(32), nullable=False, comment='小区名称')


class TabCenter(BaseModel):
    __tablename__ = 'tab_center'
    __table_args__ = {'comment': '监管中心'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    name = Column(String(32), nullable=False, comment='监管中心名称')
    ip = Column(String(32), nullable=False, comment='监管中心ip')
    port = Column(INTEGER(11), nullable=False, comment='监管中线端口号')
    protocol = Column(String(32), nullable=False, server_default='TCP/IP', comment='通讯协议类型')
    code = Column(String(32), nullable=False, comment='网关编号')


class TabController(BaseModel):
    __tablename__ = 'tab_controller'
    __table_args__ = {'comment': '控制器信息表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    project_id = Column(INTEGER(11), nullable=False, comment='项目id')
    project_name = Column(String(32), nullable=False, comment='项目名称')
    name = Column(String(32), nullable=False, comment='控制器名称')
    code = Column(INTEGER(11), nullable=False, comment='控制器号')
    model = Column(String(32), nullable=False, comment='控制器版本')
    manufacturer = Column(String(32), nullable=False, comment='制造商')
    setup_date = Column(Date, nullable=False, default=date.today(), comment='装机日期')
    controller_type = Column(TINYINT(1), nullable=False, server_default='2', comment='控制器类型（1 主机 2 从机）')
    host_id = Column(INTEGER(11), comment='主机id')
    is_online = Column(TINYINT(1), nullable=False, server_default='1', comment='是否在线（0 离线 1 在线）')
    power_type = Column(TINYINT(1), nullable=False, server_default='3', comment='电源类型（1 主电 2 备电 3 未知）')


class TabControllerOpLog(BaseModel):
    __tablename__ = 'tab_controller_op_log'
    __table_args__ = {'comment': '控制器操作记录'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    snow_id = Column(BIGINT, comment='雪花id')
    operate_time = Column(DateTime, nullable=False, comment='控制器操作时间')
    controller_id = Column(INTEGER(11), nullable=False, comment='控制器id')
    controller_num = Column(INTEGER(11), nullable=False, comment='控制器号')
    controller_name = Column(String(32), nullable=False, comment='控制器名称')
    gb_evt_type_id = Column(INTEGER(11), nullable=False, comment='国标事件类型id')
    gb_evt_type_name = Column(String(32), nullable=False, comment='国标事件类型名称')
    description = Column(String(128), nullable=False, comment='操作描述')


class TabDevice(BaseModel):
    __tablename__ = 'tab_device'
    __table_args__ = {'comment': '设备信息表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    controller_id = Column(INTEGER(11), nullable=False, comment='控制器id')
    controller_num = Column(INTEGER(11), nullable=False, comment='控制器号')
    loop_num = Column(INTEGER(11), comment='回路号')
    addr_num = Column(INTEGER(11), comment='地址号')
    equipment_num = Column(INTEGER(11), comment='设备号')
    module_num = Column(INTEGER(11), comment='模块号')
    psn = Column(String(32), nullable=False, comment='设备编号')
    manufacturer = Column(String(32), nullable=False, comment='制造商')
    device_model = Column(String(32), nullable=False, comment='设备型号')
    setup_date = Column(Date, nullable=False, default=date.today(), comment='装机日期')
    maintain_cycle = Column(INTEGER(11), comment='维保周期')
    expiration_date = Column(Date, comment='有效期')
    description = Column(String(128), nullable=False, comment='描述')
    path = Column(String(128), comment='设备图标地址')
    is_online = Column(TINYINT(1), nullable=False, server_default='1', comment='是否在线（0 否 1 是）')
    alarm = Column(INTEGER(11), nullable=False, server_default='0', comment='报警数量')
    fire = Column(INTEGER(11), nullable=False, server_default='0', comment='火警数量')
    malfunction = Column(INTEGER(11), nullable=False, server_default='0', comment='故障数量')
    vl_malfunction = Column(INTEGER(11), nullable=False, server_default='0', comment='声光故障数量')
    feedback = Column(INTEGER(11), nullable=False, server_default='0', comment='反馈数量')
    supervise = Column(INTEGER(11), nullable=False, server_default='0', comment='监管数量')
    shielding = Column(INTEGER(11), nullable=False, server_default='0', comment='屏蔽数量')
    vl_shielding = Column(INTEGER(11), nullable=False, server_default='0', comment='声光屏蔽数量')
    linkage = Column(INTEGER(11), nullable=False, server_default='0', comment='联动数量')
    is_assign = Column(TINYINT(1), nullable=False, server_default='0', comment='是否布点（0 否 1 是）')
    assign_floor_id = Column(INTEGER(11), comment='布点楼层id')
    device_type_id = Column(INTEGER(11), nullable=False, comment='设备类型id')
    device_type_name = Column(String(32), nullable=False, comment='设备类型名称')
    device_type = Column(TINYINT(1), nullable=False, server_default='1', comment='设备类型（1 设备 2 控制器）')
    area = Column(String(32), comment='小区名称')
    build = Column(String(32), comment='楼宇名称')
    unit = Column(String(32), comment='单元名称')
    floor = Column(String(32), comment='楼层名称')
    district = Column(String(32), comment='防火分区名称')
    room = Column(String(32), comment='防烟分区名称')


class TabDeviceType(BaseModel):
    __tablename__ = 'tab_device_type'
    __table_args__ = {'comment': '设备类型信息表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    gb_device_type = Column(String(32), nullable=False, comment='国标码')
    name = Column(String(32), nullable=False, comment='设备类型名称')
    zx_device_type = Column(INTEGER(11), nullable=False, comment='内部编码（10进制）')
    priority = Column(INTEGER(11), nullable=False, comment='优先级（用于查询时排序, 数字越小优先级越高）')


class TabFloor(BaseModel):
    __tablename__ = 'tab_floor'
    __table_args__ = {'comment': '楼层信息表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    name = Column(String(32), nullable=False, comment='楼层名称')
    path = Column(String(128), nullable=False, comment='图片地址')
    quick_svg_path = Column(String(128), comment='图片地址（布点后生成的svg图片地址）')
    picture_type_id = Column(INTEGER(11), nullable=False, comment='图片类型id')
    picture_type_name = Column(String(32), nullable=False, comment='图片类型名称')
    area_id = Column(INTEGER(11), nullable=False, comment='小区id')
    area_name = Column(String(32), nullable=False, comment='小区名称')
    build_id = Column(INTEGER(11), nullable=False, comment='楼宇id')
    build_name = Column(String(32), nullable=False, comment='楼宇名称')
    alarm = Column(INTEGER(11), nullable=False, server_default='0', comment='报警数量')
    fire = Column(INTEGER(11), nullable=False, server_default='0', comment='火警数量')
    malfunction = Column(INTEGER(11), nullable=False, server_default='0', comment='故障数量')
    vl_malfunction = Column(INTEGER(11), nullable=False, server_default='0', comment='声光故障数量')
    feedback = Column(INTEGER(11), nullable=False, server_default='0', comment='反馈数量')
    supervise = Column(INTEGER(11), nullable=False, server_default='0', comment='监管数量')
    shielding = Column(INTEGER(11), nullable=False, server_default='0', comment='屏蔽数量')
    vl_shielding = Column(INTEGER(11), nullable=False, server_default='0', comment='声光屏蔽数量')
    linkage = Column(INTEGER(11), nullable=False, server_default='0', comment='联动数量')
    inheritance_template = Column(TINYINT(1), nullable=False, server_default='0', comment='是否作为继承模板（0 否 1 是）')
    inheritance = Column(INTEGER(11), comment='继承（父级楼层id）')


class TabGbEvtType(BaseModel):
    __tablename__ = 'tab_gb_evt_type'
    __table_args__ = {'comment': '国标事件表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    name = Column(String(32), nullable=False, comment='国标事件类型名称')
    type_id = Column(INTEGER(11), nullable=False, comment='报警类型id')
    type_name = Column(String(32), nullable=False, comment='报警类型名称')
    event_state = Column(TINYINT(1), nullable=False, server_default='1', comment='事件状态 （0，消失，1，出现，2，丢弃）')


class TabIcon(BaseModel):
    __tablename__ = 'tab_icon'
    __table_args__ = {'comment': '设备图标表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    name = Column(String(32), nullable=False, comment='图标名称')
    path = Column(String(128), nullable=False, comment='图标地址')
    device_type_id = Column(INTEGER(11), nullable=False, comment='设备类型id')
    device_type_name = Column(String(32), nullable=False, comment='设备类型名称')
    gb_evt_type_id = Column(INTEGER(11), comment='事件类型id')
    gb_evt_type_name = Column(String(32), comment='事件类型名称')


class TabMaintenanceLog(BaseModel):
    __tablename__ = 'tab_maintenance_log'
    __table_args__ = {'comment': '维保记录'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    description = Column(String(128), nullable=False, comment='维保描述')
    operator_name = Column(String(32), nullable=False, comment='操作名称')
    project_id = Column(INTEGER(11), nullable=False, comment='项目id')
    user_id = Column(INTEGER(11), nullable=False, comment='维保人id')
    user_name = Column(String(32), nullable=False, comment='维保人名称')


class TabPictureType(BaseModel):
    __tablename__ = 'tab_picture_type'
    __table_args__ = {'comment': '图片类型表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    name = Column(String(32), nullable=False, comment='图片类型名称')
    type = Column(TINYINT(1), nullable=False, comment='文件分类（1 项目图片 2 楼宇图片 3 楼层图片 4 应急预案 5 控制室信息 6 其他）')
    file_type = Column(TINYINT(1), nullable=False, server_default='1', comment='文件类型（1. 图片 2. pdf 3. word 4. xls）')


class TabProject(BaseModel):
    __tablename__ = 'tab_project'
    __table_args__ = {'comment': '项目表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    name = Column(String(128), nullable=False, comment='项目名称')
    address = Column(String(128), nullable=False, comment='项目地址')
    mobile = Column(String(32), comment='项目联系电话')
    deploy_users = Column(String(128), nullable=False, comment='项目部署人员')  # [{'id':1, 'name':'zhangsan'},{}]
    is_active = Column(TINYINT(1), nullable=False, server_default='1', comment='是否为活跃项目（主项目）')


class TabProjectPicture(BaseModel):
    __tablename__ = 'tab_project_picture'
    __table_args__ = {'comment': '项目图片信息表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    name = Column(String(128), nullable=False, comment='项目图片名称')
    path = Column(String(128), nullable=False, comment='图片地址')
    quick_svg_path = Column(String(128), comment='图片地址（布点后生成的svg图片地址）')
    picture_type_id = Column(INTEGER(11), nullable=False, comment='图片类型id')
    picture_type_name = Column(String(32), nullable=False, comment='图片类型名称')
    project_id = Column(INTEGER(11), nullable=False, comment='项目id')
    is_home = Column(TINYINT(1), nullable=False, server_default='0', comment='是否为主页图片（0 否 1 是）')


class TabRole(BaseModel):
    __tablename__ = 'tab_role'
    __table_args__ = {'comment': '权限表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    name = Column(String(32), nullable=False, comment='角色名称')


class TabShiftRecord(BaseModel):
    __tablename__ = 'tab_shift_record'
    __table_args__ = {'comment': '换班记录表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    watch_user_id = Column(INTEGER(11), nullable=False, comment='值班用户id')
    watch_user_name = Column(String(32), nullable=False, comment='值班用户名')
    change_user_id = Column(INTEGER(11), nullable=False, comment='换班用户id')
    change_user_name = Column(String(32), nullable=False, comment='换班用户名')


class TabSystemLog(BaseModel):
    __tablename__ = 'tab_system_log'
    __table_args__ = {'comment': '系统操作记录表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    snow_id = Column(BIGINT, comment='雪花id')
    description = Column(String(128), nullable=False, comment='操作描述')
    user_id = Column(INTEGER(11), comment='用户id')
    user_name = Column(String(32), comment='用户名')


class TabSystemParam(BaseModel):
    __tablename__ = 'tab_system_param'
    __table_args__ = {'comment': '系统参数'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    carousel_time = Column(INTEGER(11), nullable=False, server_default='8', comment='轮播时长（单位秒）')
    crt_sn = Column(String(32), comment='CRT序列号')


class TabUser(BaseModel):
    __tablename__ = 'tab_user'
    __table_args__ = {'comment': '用户表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    user_name = Column(String(32), nullable=False, comment='用户名')
    password = Column(String(128), nullable=False, comment='密码')
    role_id = Column(INTEGER(11), nullable=False, comment='角色id')
    role_name = Column(String(32), nullable=False, comment='角色名称')


class TabVersion(BaseModel):
    __tablename__ = 'tab_version'
    __table_args__ = {'comment': '系统版本'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    version_num = Column(String(32), comment='版本号')
    notes = Column(String(1024), comment='版本说明')
