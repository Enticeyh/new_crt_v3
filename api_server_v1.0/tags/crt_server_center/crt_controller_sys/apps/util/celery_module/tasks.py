import sys
import time
import json
import datetime
import requests
import logging

from functools import wraps
from attrdict import AttrDict
from os.path import dirname, realpath
from sqlalchemy import select, update, func, delete

from crt_controller_sys.apps.util.async_func import hash_func_params
from crt_controller_sys.apps.util.snowflakeid import snow_fake_factory
from crt_controller_sys.apps.util.celery_module.celery_factory import celery_app, conn, cfg_class
from crt_controller_sys.apps.util.db_module.models import TabControllerOpLog, TabAlarmLog, TabSystemLog
from crt_controller_sys.apps.util.constant import CrtConstant
from crt_controller_sys.apps.util.redis_module import redis_factory
from crt_controller_sys.apps.util.db_module.sqlalchemy_factory import db_factory as db
from crt_controller_sys.apps.util.db_module.models import TabDevice, TabAssignDevice, TabFloor
from crt_controller_sys.apps.util.sync_db_api import sync_load_controller_by_num, sync_load_gb_evt_type_by_id, \
    sync_load_assign_device_by_floor_id, sync_load_device_by_floor_id, sync_load_center, sync_load_device_by_location, \
    sync_load_alarm_type, sync_load_floor_by_id, sync_load_system_param, sync_load_device_type

root_project_dir = dirname(dirname(dirname(dirname(dirname(realpath(__file__))))))
if root_project_dir not in sys.path:
    sys.path.append(root_project_dir)

logger = logging.getLogger(__name__)


def task_wrapper(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            logger.info('------------ Start ------------')
            start = time.time()
            logger.info(f'Received data: [{args}] [{kwargs}]')
            result = func(*args, **kwargs)
            spend_time = time.time() - start
            logger.info(f'spend time: {spend_time}!')
            logger.info('------------ End ------------')
            return result
        except Exception as e:
            logger.error(e)
            logger.exception(e)
        return False

    return _wrapper


@celery_app.task
@task_wrapper
def add(x, y):
    time.sleep(5)
    return x + y


@celery_app.task
@task_wrapper
def controller_adjust_time(device_num):
    try:
        controller = sync_load_controller_by_num(controller_num=device_num, conn=conn)

        if controller:
            with db.slice_session() as session:
                op_log = {
                    'controller_id': controller.id,
                    'controller_num': device_num,
                    'controller_name': controller.name,
                    'description': "时间校准",
                }
                session.add(TabControllerOpLog(**op_log))
                session.flush()

    except Exception as e:
        logger.exception(e)


@celery_app.task
@task_wrapper
def old_controller_report(all_data):
    """老版控制器报警记录处理"""
    for data in all_data:
        device_num = int(data.get("device_num", 0))  # 控制器号
        loop_num = int(data.get("loop_num", 0))  # 回路号
        addr_num = int(data.get("addr_num", 0))  # 地址号

        equipment_num = int(data.get("equipment_num", 0))  # 设备号
        module_num = int(data.get("module_num", 0))  # 模块号

        pass_num = data.get("pass_num", 0)  # 通道号
        alarm_time = data.get("datetime")  # 发生时间
        event_type = data.get("event_type", '0')  # 报警类型
        event_state = data.get("event_state", '0')  # 状态 出现 消失 丢弃
        event_state_type = data.get("event_statetype", '0')  # 状态类型
        device_type_id = int(data.get("type", 0))  # 设备类型
        alarm_type = int(data.get("alarm_type", 0))  # 报警类型 0 真实报警 1 模拟报警

        snow_id = data.get("snow_id", 0)  # 雪花id

        if type(event_type) == str and event_type.isdigit():
            event_type = int(event_type)
        elif type(event_type) == str and not event_type.isdigit():
            event_type = 0

        pass_num = int(pass_num) if pass_num else None
        event_state = int(event_state) if event_state.isdigit() else 0
        event_state_type = int(event_state_type) if event_state_type.isdigit() else 0

        # 丢弃
        if event_type == 3 and event_state == 2:
            logger.info("事件丢弃！")
            continue

        gb_evt_type_id = CrtConstant.RJ45_TO_CAN_EVENT.get(f'{event_type}-{event_state}-{event_state_type}')

        report_data = {
            'alarm_time': alarm_time,  # 控制器上报报警时间
            'controller_num': device_num,  # 控制器号
            'loop_num': loop_num,  # 回路号
            'addr_num': addr_num,  # 地址号
            'equipment_num': equipment_num,  # 设备号
            'module_num': module_num,  # 模块号
            'pass_num': pass_num,  # 通道号
            'alarm_type_id': event_type,  # 报警类型id
            'gb_evt_type_id': gb_evt_type_id,  # 国标类型id
            'device_type_id': device_type_id,  # 设备类型id
            'alarm_type': alarm_type,  # 报警类型 0 真实报警 1 模拟报警
            'snow_id': snow_id  # 雪花id
        }

        if event_type == 1:
            controller_report.apply_async(kwargs=report_data, priority=9)
        else:
            controller_report.apply_async(kwargs=report_data, priority=20)


@celery_app.task
@task_wrapper
def old_controller_operate(all_data):
    """老版控制器操作记录处理"""
    for data in all_data:
        device_num = int(data.get("device_num", 0))  # 控制器号
        operate_type = data.get("operate_type", 0)  # 操作类型
        date_time = data.get("datetime", 0)  # 发生时间
        snow_id = data.get("snow_id", 0)  # 雪花id

        gb_evt_type_id = CrtConstant.RJ45_TO_CAN_OP.get(operate_type)

        report_data = {
            'date_time': date_time,  # 控制器上报时间
            'controller_num': device_num,  # 控制器号
            'gb_evt_type_id': gb_evt_type_id,  # 国标类型id
            'snow_id': snow_id,  # 雪花id
        }

        # 复位事件优先执行
        if gb_evt_type_id == 122:
            controller_operate.apply_async(kwargs=report_data, priority=8)
        else:
            controller_operate.apply_async(kwargs=report_data, priority=20)


@celery_app.task
@task_wrapper
def new_controller_state(state):
    """
    新版控制器最新状态同步（心跳)
    :param state:
    :return:
    """
    logger.info(f"新版控制器最新状态同步:  {type(state)}   {state}")

    # 对比首页缓存和轮询接口取到的数据是否一致
    alarm_statistics = redis_factory.get_hash_cache('alarm_info_statistics', conn=conn)
    evt_num = state.get('evt_num') - state.get('operate_evt_num')  # 报警总数去除操作事件总数
    evt_num = evt_num if evt_num > 0 else 0

    # 同步计数
    if int(alarm_statistics.get('all_alarm')) != evt_num:
        conn.hset('alarm_info_statistics', 'all_alarm', evt_num)
    if int(alarm_statistics.get('fire')) != state.get('alarm_evt_num'):
        conn.hset('alarm_info_statistics', 'fire', state.get('alarm_evt_num'))
    if int(alarm_statistics.get('linkage')) != state.get('action_evt_num'):
        conn.hset('alarm_info_statistics', 'linkage', state.get('action_evt_num'))
    if int(alarm_statistics.get('feedback')) != state.get('feedback_evt_num'):
        conn.hset('alarm_info_statistics', 'feedback', state.get('feedback_evt_num'))
    if int(alarm_statistics.get('malfunction')) != state.get('fault_evt_num'):
        conn.hset('alarm_info_statistics', 'malfunction', state.get('fault_evt_num'))
    if int(alarm_statistics.get('shielding')) != state.get('shielding_evt_num'):
        conn.hset('alarm_info_statistics', 'shielding', state.get('shielding_evt_num'))
    if int(alarm_statistics.get('supervise')) != state.get('supervisor_evt_num'):
        conn.hset('alarm_info_statistics', 'supervise', state.get('supervisor_evt_num'))
    if int(alarm_statistics.get('vl_malfunction')) != state.get('vl_fault_evt_num', 0):
        conn.hset('alarm_info_statistics', 'vl_malfunction', state.get('vl_fault_evt_num', 0))
    if int(alarm_statistics.get('vl_shielding')) != state.get('vl_shielding_evt_num', 0):
        conn.hset('alarm_info_statistics', 'vl_shielding', state.get('vl_shielding_evt_num', 0))

    # 连接新版控制器时，首页轮播图纸需要更新，更新缓存标记
    if state.get('is_update'):
        conn.hset('alarm_info_statistics', 'is_assign_update', 1)

    # 更新控制器心跳
    controller_heartbeats.apply_async(priority=10)

    logger.info(f'\n\n task_name：new_controller_state state：{state} \n\n')


@celery_app.task
@task_wrapper
def new_controller_alarm(all_data):
    """新版控制器报警记录处理"""
    logger.info(f"新版控制器报警记录处理:  {type(all_data)}   {all_data}")

    gb_evt_types = {}

    for data in all_data:
        try:
            alarm_time = datetime.datetime.strptime(data.get('datetime'), '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            logger.debug(f"新版控制器，数据报文时间格式错误！\n {e}")
            alarm_time = datetime.datetime.now()

        gb_evt_type = gb_evt_types.get(data.get('evt_code'))
        if not gb_evt_type:
            gb_evt_type = sync_load_gb_evt_type_by_id(gb_evt_type_id=data.get('evt_code'), conn=conn)
            gb_evt_types[data.get('evt_code')] = gb_evt_type

        controller_report_id = int(data.get('id', 0))  # 新版控制器上报记录id
        controller_num = int(data.get('ctrl_num', 0))  # 控制器号
        loop_num = int(data.get('loop_num', 0))  # 回路号
        addr_num = int(data.get('addr_num', 0))  # 地址号

        equipment_num = int(data.get('dev_num', 0))  # 设备号
        module_num = int(data.get('module_num', 0))  # 模块号

        pass_num = int(data.get("pass_num", 0))  # 通道号
        device_type_id = int(data.get("device_gb_type", 0))  # 国标设备类型

        # 根据国标事件码查询报警类型
        gb_evt_type_id = gb_evt_type.get('id')
        alarm_type_id = gb_evt_type.get('type_id')

        report_data = {
            'create_time': alarm_time.strftime('%Y-%m-%d %H:%M:%S'),
            'alarm_time': alarm_time.strftime("%Y%m%d%H%M%S"),  # 控制器上报报警时间
            'controller_num': controller_num,  # 控制器号
            'loop_num': loop_num,  # 回路号
            'addr_num': addr_num,  # 地址号
            'equipment_num': equipment_num,  # 设备号
            'module_num': module_num,  # 模块号
            'pass_num': pass_num,  # 通道号
            'alarm_type_id': alarm_type_id,  # 报警类型id
            'gb_evt_type_id': gb_evt_type_id,  # 国标类型id
            'device_type_id': device_type_id,  # 设备类型id
            'alarm_type': 0,  # 报警类型 0 真实报警 1 模拟报警
            'snow_id': snow_fake_factory.get_id(),  # 雪花id
            'controller_report_id': controller_report_id  # 新版控制器上报记录id
        }

        if alarm_type_id == 1:
            controller_report.apply_async(kwargs=report_data, priority=9)
        else:
            controller_report.apply_async(kwargs=report_data, priority=20)

        logger.info(f'\n\n task_name：new_controller_alarm all_data：{all_data} \n\n')


@celery_app.task
@task_wrapper
def new_controller_operate(all_data):
    """新版控制器操作记录处理"""
    logger.info(f"新版控制器操作记录处理:  {type(all_data)}   {all_data}")

    start = time.time()

    for data in all_data:
        try:
            alarm_time = datetime.datetime.strptime(data.get('datetime'), '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            logger.debug(f"新版控制器，数据报文时间格式错误！\n {e}")
            alarm_time = datetime.datetime.now()

        gb_evt_type_id = int(data.get("evt_code", 0))  # 国标事件类型
        controller_num = int(data.get('ctrl_num', 0))  # 控制器号

        operate_data = {
            'create_time': alarm_time.strftime('%Y-%m-%d %H:%M:%S'),
            'date_time': alarm_time.strftime("%Y%m%d%H%M%S"),  # 控制器上报报警时间
            'controller_num': controller_num,  # 控制器号
            'gb_evt_type_id': gb_evt_type_id,  # 国标类型id
            'snow_id': snow_fake_factory.get_id()  # 雪花id
        }

        # 复位事件优先执行
        if gb_evt_type_id == 122:
            controller_operate.apply_async(kwargs=operate_data, priority=8)
        else:
            controller_operate.apply_async(kwargs=operate_data, priority=20)

        logger.info(f'\n\n task_name：new_controller_operate all_data：{all_data} 序号 1 {time.time() - start}  \n\n')


@celery_app.task
@task_wrapper
def controller_report(*_, alarm_time, controller_num, loop_num, addr_num, pass_num, alarm_type_id, gb_evt_type_id,
                      device_type_id, alarm_type, snow_id, equipment_num=None, module_num=None, error=False,
                      alarm_log_id=None, controller_report_id=None, create_time=None):
    """
    控制器事件上报处理
    :param _:
    :param alarm_time: 控制器上报报警时间
    :param controller_num: 控制器号
    :param loop_num: 回路号
    :param addr_num: 地址号
    :param pass_num: 通道号
    :param alarm_type_id: 报警类型id
    :param gb_evt_type_id: 国标类型id
    :param device_type_id: 设备类型id
    :param alarm_type: 报警类型 0 真实报警 1 模拟报警
    :param snow_id: 雪花id
    :param equipment_num: 设备号（应急疏散才会使用）
    :param module_num: 模块号（应急疏散才会使用）
    :param error: 是否是错误数据重新录入
    :param alarm_log_id: 错误的报警记录id
    :param controller_report_id: 新版控制器上报记录id
    :param create_time: 新版控制器上报记录中的报警时间
    :return:
    """
    # start = time.time()
    # logger.info(f'\n\n {controller_num}-{loop_num}-{addr_num} 序号 {time.time()-start}  \n\n')
    try:
        is_clear = 0
        last_reset_snow_id = int(conn.get('last_reset_snow_id'))  # 最近一次复位操作的雪花id
        # 如果雪花id小于最近一次的复位雪花id，说明该数据应该是应该被清理的数据
        logger.info(f"数据是否应该被清理（是否为复位前的数据）：{snow_id < last_reset_snow_id}")
        if snow_id < last_reset_snow_id:
            # 如果error为True，说明是定时任务检测到的错误数据，根据报警记录id直接修改就可以
            if error:
                try:
                    with db.slice_session() as session:
                        qry_func = select(TabAlarmLog).where(TabAlarmLog.id == alarm_log_id)
                        records = session.execute(qry_func)
                        alarm_log = records.scalars().first()
                        alarm_log.is_delete = 0
                        alarm_log.is_clear = 1
                        session.flush()
                        return
                except Exception as e:
                    msg = f'alarm_log_id: {alarm_log_id} 修改报警记录错误！'
                    logger.error(msg)
                    logger.exception(e)
            # 如果error为False，说明是控制器下发的错误数据，正常进行alarm_log的新增，不用更新统计信息
            else:
                is_clear = 1

        # 查询控制器信息
        controller = None
        if controller_num is not None:
            controller = sync_load_controller_by_num(controller_num=controller_num, conn=conn)
            if not controller:
                logger.error(f'无相关控制器 controller_num：{controller_num}')

        # 如果控制器被屏蔽 抛弃事件
        if controller.get('is_shielding') == 1:
            return

        alarm_statistics = 'alarm_info_statistics'  # 首页所需数据 缓存name

        if int(conn.hget('alarm_info_statistics', 'controller_linked') or 0) == 0:
            conn.hset('alarm_info_statistics', 'controller_linked', 1)

        # 解析报警时间
        try:
            alarm_time = datetime.datetime.strptime(alarm_time, "%Y%m%d%H%M%S")
        except Exception as e:
            logger.debug(f"老版控制器，上报报文时间格式错误！\n {e}")
            alarm_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        # logger.info(f'\n\n {controller_num}-{loop_num}-{addr_num} 序号 1111  {time.time() - start}  \n\n')

        # 是否为首火警
        first_fire = False
        if alarm_type_id == 1 and int(conn.hget(alarm_statistics, 'first_fire') or '0') == 0:
            first_fire = True
            gb_evt_type_id = 2
            # 先把雪花id放到首警中占位
            conn.hset(alarm_statistics, 'first_fire', snow_id)

        # logger.info(f'\n\n {controller_num}-{loop_num}-{addr_num} 序号 222 {time.time() - start}  \n\n')

        # 查询国标事件类型
        gb_evt_type = {}
        event_state = 1  # 事件默认为出现
        if gb_evt_type_id:
            gb_evt_type = sync_load_gb_evt_type_by_id(gb_evt_type_id=gb_evt_type_id, conn=conn)
            if not gb_evt_type:
                logger.error(f'无相关国标事件类型 gb_evt_type_id：{gb_evt_type_id}')
            else:
                event_state = int(gb_evt_type.get('event_state'))
        else:
            logger.error(f'无相关国标事件类型 gb_evt_type_id：{gb_evt_type_id}')

        alarm_types = sync_load_alarm_type(page=0, conn=conn, fast_to_dict=True)
        alarm_type_name_zh = alarm_types.get(alarm_type_id).get('name') if alarm_types.get(alarm_type_id) else '未知'
        alarm_type_name = CrtConstant.DEVICE_ALARM_STATUS.get(alarm_type_id) or 'unknown'  # 获取报警类型

        # logger.info(f'\n\n {controller_num}-{loop_num}-{addr_num} 序号 3333 {time.time() - start}  \n\n')

        # 要删除的报警记录id数量
        del_alarm_log_num = 1 if event_state == 0 else 0

        # logger.info(f'\n\n {controller_num}-{loop_num}-{addr_num} 序号  4444  {time.time() - start}  \n\n')

        try:
            # 新增alarm_log
            device = AttrDict()
            if controller and loop_num and addr_num:
                device = sync_load_device_by_location(controller_num, loop_num, addr_num, conn=conn)

            # logger.info(f'\n\n {controller_num}-{loop_num}-{addr_num} 序号 55555 {time.time() - start}  \n\n')

            if device and device.device_type_id:
                device_type_id = device.device_type_id
                device_type_name = device.device_type_name
            else:
                if CrtConstant.DEVICE_TYPE_DICT.get(str(device_type_id)):
                    device_type_id, device_type_name = CrtConstant.DEVICE_TYPE_DICT.get(str(device_type_id))
                else:
                    device_type_id, device_type_name = None, None

            if device:
                description = f"{device.description}/{gb_evt_type.get('name') or '未知事件'}"
            elif controller and loop_num and addr_num:
                description = f"{controller.get('name')}-{loop_num}回路-{addr_num}/{gb_evt_type.get('name') or '未知事件'}"
            elif controller and loop_num and not addr_num:
                description = f"{controller.get('name')}-{loop_num}回路/{gb_evt_type.get('name') or '未知事件'}"
            elif controller and not loop_num and not addr_num:
                description = f"{controller.get('name')}/{gb_evt_type.get('name') or '未知事件'}"
            else:
                description = f"未知设备/{gb_evt_type.get('name') or '未知事件'}"

            # logger.info(f'\n\n {controller_num}-{loop_num}-{addr_num} 序号 66666 {time.time() - start}  \n\n')

            # 报警队列key
            params_md5 = hash_func_params(is_clear=0)
            alarm_log_name = f'tab_alarm_log-records:{params_md5}'

            device_alarm = conn.hget('alarm_list', f'{controller_num}-{loop_num}-{addr_num}-{pass_num or 0}-{alarm_type_id}')
            alarm_log_id_list = conn.hget('alarm_log_id_list', f'{controller_num}-{loop_num}-{addr_num}-{pass_num or 0}-{alarm_type_id}')
            new_gb_evt_type_id = gb_evt_type_id if gb_evt_type_id != 2 else 3

            # 如果存在该设备该报警大类的缓存，检查国标事件是否存在
            if device_alarm:
                device_alarm = json.loads(device_alarm) if device_alarm else []
                alarm_log_id_list = json.loads(alarm_log_id_list) if alarm_log_id_list else []
                # 如果该记录的国标事件存在 说明事件重复 该事件抛弃
                if new_gb_evt_type_id in device_alarm:
                    logger.info(f"设备：{controller_num}-{loop_num}-{addr_num}-{pass_num or 0} 已经存在{gb_evt_type.get('name')}，事件抛弃！")
                    return
                # 如果国标事件对应的是消失事件 清除缓存中该设备该报警类型的所有记录
                elif event_state == 0:
                    conn.hdel('alarm_list', f'{controller_num}-{loop_num}-{addr_num}-{pass_num or 0}-{alarm_type_id}')

                    # 清除报警队列对应出现事件
                    for alarm_log_id in alarm_log_id_list:
                        conn.hdel(alarm_log_name, alarm_log_id)
                    del_alarm_log_num = len(alarm_log_id_list)
                    conn.hdel('alarm_log_id_list', f'{controller_num}-{loop_num}-{addr_num}-{pass_num or 0}-{alarm_type_id}')
                # 如果事件为出现且之前没有出现过相同的国标事件 将该国标事件id加入到缓存记录中
                else:
                    device_alarm.append(new_gb_evt_type_id)
                    conn.hset('alarm_list', f'{controller_num}-{loop_num}-{addr_num}-{pass_num or 0}-{alarm_type_id}', json.dumps(device_alarm))
            # 如果没有查到该设备该报警大类的缓存，添加缓存
            else:
                # 如果之前该设备没有该报警大类的出现事件 消失事件抛弃
                if event_state == 0:
                    logger.info(f"设备：{controller_num}-{loop_num}-{addr_num}-{pass_num or 0} 不存在{alarm_type_name_zh}事件，抛弃！")
                    return
                conn.hset('alarm_list', f'{controller_num}-{loop_num}-{addr_num}-{pass_num or 0}-{alarm_type_id}', json.dumps([new_gb_evt_type_id]))

            # logger.info(f'\n\n {controller_num}-{loop_num}-{addr_num} 序号  88888  {time.time() - start}  \n\n')

            device_assign_floor = AttrDict()
            if device and device.assign_floor_id:
                device_assign_floor = sync_load_floor_by_id(floor_id=device.assign_floor_id, conn=conn)

            with db.slice_session() as session:
                alarm_log_data = {
                    'create_time': create_time,
                    'is_clear': is_clear,
                    "alarm_time": str(alarm_time),
                    "description": description,
                    "controller_num": controller_num,
                    "loop_num": loop_num,
                    "addr_num": addr_num,
                    "equipment_num": equipment_num,
                    "module_num": module_num,
                    "pass_num": pass_num,
                    "device_type_id": device_type_id,
                    "device_type_name": device_type_name,
                    "area_id": device_assign_floor.area_id if device_assign_floor else None,
                    "area_name": device_assign_floor.area_name if device_assign_floor else None,
                    "build_id": device_assign_floor.build_id if device_assign_floor else None,
                    "build_name": device_assign_floor.build_name if device_assign_floor else None,
                    "floor_id": device_assign_floor.id if device_assign_floor else None,
                    "floor_name": device_assign_floor.name if device_assign_floor else None,
                    "device_id": device.id if device else None,
                    "alarm_type_id": alarm_type_id,
                    "alarm_type_name": alarm_type_name_zh,
                    "assign_status": device.is_assign if device else None,
                    "alarm_status": gb_evt_type.get('event_state') if gb_evt_type else 1,
                    "gb_evt_type_id": gb_evt_type_id or 0,
                    "gb_evt_type_name": gb_evt_type.get('type_name') if gb_evt_type else '未知事件',
                    "alarm_type": alarm_type,
                    "snow_id": snow_id,
                    "controller_report_id": controller_report_id,
                }
                # 确认是否为首火警
                if first_fire and int(conn.hget(alarm_statistics, 'first_fire') or '0') != snow_id:
                    first_fire = False
                    gb_evt_type_id = 3
                    alarm_log_data["gb_evt_type_name"] = "火警"
                    alarm_log_data["gb_evt_type_id"] = gb_evt_type_id
                    alarm_log_data["description"] = description.replace('首', '')

                # logger.info(f'\n\n {controller_num}-{loop_num}-{addr_num} 序号 9999 {time.time() - start}  \n\n')

                alarm_log = TabAlarmLog(**alarm_log_data)
                session.add(alarm_log)
                session.flush()

                # logger.info(f'\n\n {controller_num}-{loop_num}-{addr_num} 序号 10101010 {time.time() - start}  \n\n')

                # 如果is_clear=1，说明是控制器下发的错误数据，不用进行后续的数据操作
                if is_clear:
                    return

                # 将报警记录加入报警队列
                if event_state == 1:
                    if alarm_log_id_list:
                        if type(alarm_log_id_list) != list:
                            alarm_log_id_list = json.loads(alarm_log_id_list)
                        alarm_log_id_list.append(alarm_log.id)
                        conn.hset('alarm_log_id_list', f'{controller_num}-{loop_num}-{addr_num}-{pass_num or 0}-{alarm_type_id}', json.dumps(alarm_log_id_list))
                    else:
                        conn.hset('alarm_log_id_list', f'{controller_num}-{loop_num}-{addr_num}-{pass_num or 0}-{alarm_type_id}', json.dumps([alarm_log.id]))

                    # 将报警记录放入缓存
                    conn.hset(alarm_log_name, key=alarm_log.id, value=json.dumps(alarm_log.to_dict()))

                # 如果是首警 将报警记录id放入
                if first_fire:
                    conn.hset(alarm_statistics, 'first_fire', alarm_log.id)

                # logger.info(f'\n\n {controller_num}-{loop_num}-{addr_num} 序号 11 {time.time() - start}  \n\n')

        except Exception as e:
            msg = f'新增报警记录错误！'
            logger.error(msg)
            logger.exception(e)

        try:
            # 发送事件到智慧消防
            center = sync_load_center(conn=conn)
            heartbeat_time = conn.get('center_heartbeat_time')
            if center and (alarm_type == 0) and heartbeat_time:
                alarm_data = {
                    "controller_type_code": 330,
                    "controller_num": controller_num,
                    "evt_code": gb_evt_type_id or 0,
                    "datetime": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    "equipment_num": equipment_num,
                    "module_num": module_num,
                    "loop_num": loop_num,
                    "addr_num": addr_num,
                    "chan_num": pass_num,
                }

                data = {
                    'code': center.code,
                    'data': [alarm_data],
                    'link': 1
                }

                url = cfg_class.CENTER_REPORT_URL % (center.ip, center.port)
                try:
                    # 设置aiohttp超时时间, 5s
                    resp = requests.post(url, json=data, timeout=cfg_class.GATEWAY_TIMEOUT)
                    center_resp = json.loads(resp.text)
                    if center_resp.get('code') != 0:
                        logger.error(f"CRT上报报警信息错误:{center_resp.get('msg')}")
                    else:
                        logger.error(f"CRT上报报警信息成功！")
                        # 存入检测中心通讯时间
                        conn.setex('center_heartbeat_time', cfg_class.REDIS_GATEWAY_TIME, int(time.time() * 1000))
                except Exception as e:
                    logger.error(f"CRT报警信息上报错误:{str(e)}")
        except Exception as e:
            logger.error(f"CRT发送报警事件到智慧消防错误:{str(e)}")

        # logger.info(f'\n\n {controller_num}-{loop_num}-{addr_num} 序号 12 {time.time() - start}  \n\n')

        # 检查是否为声光故障和声光屏蔽
        is_vl_malfunction, is_vl_shielding = 0, 0
        if alarm_type_id == 4 and device_type_id in CrtConstant.VL_DEVICE_TYPES:
            is_vl_malfunction = 1
        elif alarm_type_id == 5 and device_type_id in CrtConstant.VL_DEVICE_TYPES:
            is_vl_shielding = 1

        conn.rpush("alarm_info_list", f'{alarm_type},{alarm_type_id},{event_state}')
        if is_vl_malfunction:
            conn.rpush("alarm_info_list", f'{alarm_type},{7},{event_state}')
        elif is_vl_shielding:
            conn.rpush("alarm_info_list", f'{alarm_type},{8},{event_state}')

        if alarm_type == 0:
            # 更新心跳时间
            if not conn.get('http_heartbeat'):
                conn.set('http_heartbeat', 1)  # 标记为http数据采集 停用can数据采集
            conn.setex('heartbeat_time', cfg_class.REDIS_HEARTBEAT_TIME, int(time.time() * 1000))

        # logger.info(f'\n\n {controller_num}-{loop_num}-{addr_num} 序号 13 {time.time() - start}  \n\n')

        # 更新设备状态  清除设备缓存  更新布点状态  更新布点图状态
        assign, floor = None, None

        is_assign_update = False  # 如果图纸报警数量从0到1，或者从1到0 说明首页轮播图纸需要更新，更新缓存
        if controller_num is not None and loop_num and addr_num:
            with db.slice_session() as session:
                device_qry_func = select(TabDevice).where(TabDevice.is_delete == 0,
                                                          TabDevice.controller_num == controller_num,
                                                          TabDevice.loop_num == loop_num,
                                                          TabDevice.addr_num == addr_num)
                device = session.execute(device_qry_func)
                device = device.scalars().first()
                if not device:
                    logger.error(f'无相关设备 controller_num：{controller_num}，loop_num：{loop_num}，addr_num：{addr_num}')
                else:
                    # 更新设备状态
                    num = getattr(device, alarm_type_name)
                    # event_state  事件状态  0，消失，1，出现
                    if event_state:
                        device.alarm += 1
                        setattr(device, alarm_type_name, num + 1)
                        if is_vl_malfunction:
                            device.vl_malfunction += 1
                        elif is_vl_shielding:
                            device.vl_shielding += 1
                    else:
                        device.alarm = device.alarm - del_alarm_log_num if (device.alarm - del_alarm_log_num) > 0 else 0
                        setattr(device, alarm_type_name, (num - del_alarm_log_num if (num - del_alarm_log_num) > 0 else 0))
                        if is_vl_malfunction:
                            device.vl_malfunction = device.vl_malfunction - del_alarm_log_num if (device.vl_malfunction - del_alarm_log_num) > 0 else 0
                        elif is_vl_shielding:
                            device.vl_shielding = device.vl_shielding - del_alarm_log_num if (device.vl_shielding - del_alarm_log_num) > 0 else 0

                    # 更新设备布点状态
                    if device.is_assign:
                        assign_qry_func = select(TabAssignDevice).where(TabAssignDevice.is_delete == 0,
                                                                        TabAssignDevice.device_id == device.id)
                        assign = session.execute(assign_qry_func)
                        assign = assign.scalars().first()
                        if not assign:
                            logger.error(f'无布点信息 device_id：{device.id}')
                        else:
                            assign.device_status = (gb_evt_type_id or -1) if device.alarm else 0  # 如果报警被清空说明设备正常

                            # 更新图纸状态
                            floor_qry_func = select(TabFloor).where(TabFloor.is_delete == 0, TabFloor.id == assign.floor_id)
                            floor = session.execute(floor_qry_func)
                            floor = floor.scalars().first()
                            if not floor:
                                logger.error(f'无图纸信息 floor_id：{floor.id}')
                            else:
                                num = getattr(floor, alarm_type_name)

                                # 新版控制器 判断首页是否需要更新图纸
                                if int(conn.get('controller_type') or 2) == 2:
                                    if (floor.alarm == 0 and event_state == 1) or (floor.alarm == 1 and event_state == 0):
                                        is_assign_update = True

                                # event_state  事件状态  0，消失，1，出现
                                if event_state:
                                    floor.alarm += 1
                                    setattr(floor, alarm_type_name, num + 1)
                                    if is_vl_malfunction:
                                        floor.vl_malfunction += 1
                                    elif is_vl_shielding:
                                        floor.vl_shielding += 1
                                else:
                                    floor.alarm = floor.alarm - del_alarm_log_num if (floor.alarm - del_alarm_log_num) > 0 else 0
                                    setattr(floor, alarm_type_name, (num - del_alarm_log_num if (num - del_alarm_log_num) > 0 else 0))
                                    if is_vl_malfunction:
                                        floor.vl_malfunction = floor.vl_malfunction - del_alarm_log_num if (floor.vl_malfunction - del_alarm_log_num) > 0 else floor.vl_malfunction
                                    elif is_vl_shielding:
                                        floor.vl_shielding = floor.vl_shielding - del_alarm_log_num if (floor.vl_shielding - del_alarm_log_num) > 0 else floor.vl_shielding

                                # 删除楼层缓存
                                floor_name = f'tab_floor-records:*'
                                floor_keys = conn.keys(floor_name)

                                if floor_keys:
                                    conn.delete(*floor_keys)

            # logger.info(f'\n\n {controller_num}-{loop_num}-{addr_num} 序号 14 {time.time() - start}  \n\n')

            # 更新缓存 设备缓存 布点缓存 图纸缓存
            if device and assign and floor:
                try:
                    logger.info('更新缓存')
                    # 更新图纸缓存
                    params_md5 = hash_func_params(page=0, per_page=10, is_alarm=1)
                    floor_name = f'tab_floor-records:{params_md5}'
                    conn.hset(floor_name, key=floor.id, value=json.dumps(floor.to_dict()))

                    # logger.info(f'\n\n {controller_num}-{loop_num}-{addr_num} 序号 15 {time.time() - start}  \n\n')

                    # 更新布点缓存
                    # sync_load_assign_device_by_floor_id(page=0, conn=conn, refresh_redis=True, floor_id=floor.id)
                    params_md5 = hash_func_params(page=0, per_page=10, floor_id=floor.id)
                    assign_device_name = f'tab_assign_device-records:{params_md5}'
                    if conn.exists(assign_device_name):
                        conn.hset(assign_device_name, key=assign.id, value=json.dumps(assign.to_dict()))
                    else:
                        sync_load_assign_device_by_floor_id(page=0, conn=conn, refresh_redis=True, floor_id=floor.id)
                    # logger.info(f'\n\n {controller_num}-{loop_num}-{addr_num} 序号 16 {time.time() - start}  \n\n')
                    # 更新设备缓存
                    # sync_load_device_by_floor_id(page=0, conn=conn, refresh_redis=True, floor_id=floor.id)
                    params_md5 = hash_func_params(page=0, per_page=10, floor_id=floor.id)
                    device_name = f'tab_device-records:{params_md5}'
                    if conn.exists(device_name):
                        conn.hset(device_name, key=device.id, value=json.dumps(device.to_dict()))
                    else:
                        sync_load_device_by_floor_id(page=0, conn=conn, refresh_redis=True, floor_id=floor.id)

                    # 连接新版控制器时，首页轮播图纸需要更新，更新缓存标记
                    if is_assign_update:
                        conn.hset('alarm_info_statistics', 'is_assign_update', 1)

                except Exception as e:
                    msg = '更新缓存错误！'
                    logger.info(msg)
                    logger.exception(e)

            # logger.info(f'\n\n {controller_num}-{loop_num}-{addr_num} 序号 17 {time.time() - start}  \n\n')

    except Exception as e:
        logger.exception(e)


@celery_app.task
@task_wrapper
def controller_operate(*_, date_time, controller_num, gb_evt_type_id, snow_id, create_time=None):
    """
    控制器操作上报处理
    :param _:
    :param date_time: 控制器上报时间
    :param controller_num: 控制器号
    :param gb_evt_type_id: 国标类型id
    :param snow_id: 雪花id
    :param create_time: 新版控制器上报记录中的报警时间
    :return:
    """
    try:
        # 查询控制器信息
        controller = None
        if controller_num is not None:
            controller = sync_load_controller_by_num(controller_num=controller_num, conn=conn)

        # 如果控制器被屏蔽 抛弃事件
        if controller and controller.get('is_shielding') == 1:
            return

        # 解析报警时间
        try:
            date_time = datetime.datetime.strptime(date_time, "%Y%m%d%H%M%S")
        except Exception as e:
            logger.debug(f"老版控制器，上报报文时间格式错误！\n {e}")
            date_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        # 查询国标事件类型
        gb_evt_type = sync_load_gb_evt_type_by_id(gb_evt_type_id=gb_evt_type_id, conn=conn)
        if gb_evt_type:
            gb_evt_type_name = gb_evt_type.name
        else:
            logger.error(f'无相关国标事件类型 gb_evt_type_id：{gb_evt_type_id}')
            gb_evt_type_name = '未知操作'

        if controller:
            controller_id = controller.id
            controller_num = controller.code
            controller_name = controller.name
        else:
            logger.error(f'无相关控制器 controller_num：{controller_num}')
            controller_id = 0
            controller_num = controller_num
            controller_name = '未知控制器'

        if gb_evt_type and controller and gb_evt_type_id == 122 and controller.controller_type == 1:
            conn.set('last_reset_snow_id', snow_id)

        if controller and controller.controller_type == 2:
            snow_id = None

        description = f'{controller_name}-{gb_evt_type_name}'

        # 写入控制器操作记录
        try:
            with db.slice_session() as session:
                controller_op_data = {
                    "create_time": create_time,
                    "operate_time": str(date_time),
                    "controller_id": controller_id,
                    "controller_num": controller_num,
                    "controller_name": controller_name,
                    "gb_evt_type_id": gb_evt_type_id,
                    "gb_evt_type_name": gb_evt_type_name,
                    "description": description,
                    "snow_id": snow_id,
                }
                controller_op_log = TabControllerOpLog(**controller_op_data)
                session.add(controller_op_log)
                session.flush()

        except Exception as e:
            logger.error(f'新增控制器操作记录错误！')
            logger.exception(e)

        # 更新心跳时间
        if not conn.get('http_heartbeat'):
            conn.set('http_heartbeat', 1)  # 标记为http数据采集 停用can数据采集
        conn.setex('heartbeat_time', cfg_class.REDIS_HEARTBEAT_TIME, int(time.time() * 1000))

        try:
            # 发送事件到智慧消防
            center = sync_load_center(conn=conn)
            heartbeat_time = conn.get('center_heartbeat_time')
            if center and heartbeat_time:
                op_data = {
                    "controller_type_code": 330,
                    "controller_num": controller_num,
                    "evt_code": gb_evt_type_id or 0,
                    "datetime": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                }

                data = {
                    'code': center.code,
                    'data': [op_data],
                    'link': 1
                }

                url = cfg_class.CONTROLLER_OP_URL % (center.ip, center.port)
                try:
                    # 设置aiohttp超时时间, 5s
                    resp = requests.post(url, json=data, timeout=cfg_class.GATEWAY_TIMEOUT)
                    center_resp = json.loads(resp.text)
                    if center_resp.get('code') != 0:
                        logger.error(f"CRT上报控制器操作信息错误:{center_resp.get('msg')}")
                    else:
                        logger.error(f"CRT上报控制器操作信息成功！")
                        # 存入检测中心通讯时间
                        conn.setex('center_heartbeat_time', cfg_class.REDIS_GATEWAY_TIME, int(time.time() * 1000))
                except Exception as e:
                    logger.error(f"CRT控制器操作信息上报错误:{str(e)}")
        except Exception as e:
            logger.error(f"CRT发送控制器操作信息到智慧消防错误:{str(e)}")

        # 控制器复位
        if gb_evt_type and controller and gb_evt_type_id == 122:
            # 控制器号不是主控制器，不执行复位
            if controller.controller_type == 2:
                logger.info(f"controller_id: {controller.id}，为从机，不能进行复位操作！")
                return

            try:
                # 更新设备状态 布点状态 图纸状态 报警
                update_alarm_log = update(TabAlarmLog)
                update_alarm_log = update_alarm_log.where(TabAlarmLog.is_delete == 0, TabAlarmLog.is_clear == 0,
                                                          TabAlarmLog.snow_id < snow_id).values(is_clear=1)

                update_device = update(TabDevice).where(TabDevice.is_delete == 0)
                update_device = update_device.values(alarm=0, fire=0, malfunction=0, vl_malfunction=0, feedback=0,
                                                     supervise=0, shielding=0, vl_shielding=0, linkage=0)

                update_assign_device = update(TabAssignDevice)
                update_assign_device = update_assign_device.where(TabAssignDevice.is_delete == 0)
                update_assign_device = update_assign_device.values(device_status=0)

                update_floor = update(TabFloor).where(TabFloor.is_delete == 0)
                update_floor = update_floor.values(alarm=0, fire=0, malfunction=0, vl_malfunction=0, feedback=0,
                                                   supervise=0, shielding=0, vl_shielding=0, linkage=0)

                with db.slice_session() as session:
                    session.execute(update_device)
                    session.execute(update_assign_device)
                    session.execute(update_floor)
                    session.execute(update_alarm_log)

                center_linked = conn.hget('alarm_info_statistics', 'center_linked')

                # 清除缓存 报警统计 报警列表 报警图纸列表 报警图纸布点列表 报警图纸设备列表 首警信息
                alarm_info_statistics = {
                    "all_alarm_num": 0,
                    "all_alarm": 0,
                    "first_fire": 0,
                    "fire": 0,
                    "linkage": 0,
                    "feedback": 0,
                    "malfunction": 0,
                    "shielding": 0,
                    "supervise": 0,
                    "vl_malfunction": 0,
                    "vl_shielding": 0,
                    "analog_all_alarm": 0,
                    "analog_fire": 0,
                    "analog_linkage": 0,
                    "analog_feedback": 0,
                    "analog_malfunction": 0,
                    "analog_shielding": 0,
                    "analog_supervise": 0,
                    "analog_vl_malfunction": 0,
                    "analog_vl_shielding": 0,
                    "controller_linked": 1,
                    "center_linked": int(center_linked),
                    "is_reset": 1
                }
                conn.hset('alarm_info_statistics', mapping=alarm_info_statistics)

                alarm_log_name = f'tab_alarm_log-records:*'
                alarm_log_keys = conn.keys(alarm_log_name)

                floor_name = f'tab_floor-records:*'
                floor_keys = conn.keys(floor_name)

                assign_device_name = f'tab_assign_device-records:*'
                assign_device_keys = conn.keys(assign_device_name)

                device_name = f'tab_device-records:*'
                device_keys = conn.keys(device_name)

                del_keys = [] + alarm_log_keys + floor_keys + assign_device_keys + device_keys
                if del_keys:
                    # 清除全部缓存键
                    conn.delete(*del_keys)

                # 删除报警去重列表
                conn.delete('alarm_list')
                conn.delete('alarm_log_id_list')

                # 检查有无错误数据
                check_reset_error_data.apply_async(priority=10)

            except Exception as e:
                logger.error(f'新增控制器操作记录错误！')
                logger.exception(e)

    except Exception as e:
        logger.exception(e)


@celery_app.task
@task_wrapper
def controller_heartbeats():
    """
    控制器心跳上报处理
    :return:
    """
    try:
        # 更新心跳时间
        if not conn.get('http_heartbeat'):
            conn.set('http_heartbeat', 1)  # 标记为http数据采集 停用can数据采集
        conn.setex('heartbeat_time', cfg_class.REDIS_HEARTBEAT_TIME, int(time.time() * 1000))

        if int(conn.hget('alarm_info_statistics', 'controller_linked') or 0) == 0:
            conn.hset('alarm_info_statistics', 'controller_linked', 1)

    except Exception as e:
        logger.exception(e)


@celery_app.task
@task_wrapper
def center_heartbeats():
    """
    智慧消防心跳上报
    :return:
    """
    try:
        # 发送心跳到智慧消防
        center = sync_load_center(conn=conn)
        if center:
            data = {
                'code': center.code,
                'datetime': datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
            }

            url = cfg_class.CENTER_HEART_URL % (center.ip, center.port)
            try:
                # 设置aiohttp超时时间, 5s
                resp = requests.post(url, json=data, timeout=cfg_class.GATEWAY_TIMEOUT)
                # resp = requests.post(url, json=data, timeout=cfg_class.GATEWAY_TIMEOUT, headers=headers)
                center_resp = json.loads(resp.text)
                if center_resp.get('code') != 0:
                    logger.error(f"CRT上报心跳信息错误:{center_resp.get('msg')}")
                    return
                # 存入检测中心通讯时间
                conn.setex('center_heartbeat_time', cfg_class.REDIS_GATEWAY_TIME, int(time.time() * 1000))
            except Exception as e:
                logger.error(f"CRT心跳上报错误:{str(e)}")
        else:
            conn.setex('center_heartbeat_time', cfg_class.REDIS_GATEWAY_TIME, int(time.time() * 1000))

    except Exception as e:
        logger.exception(e)


@celery_app.task
@task_wrapper
def check_controller_heartbeats():
    """
    控制器心跳检查
    :return:
    """
    try:
        if not conn.get('start_time'):
            alarm_statistics = 'alarm_info_statistics'  # 首页所需数据 缓存name
            heartbeat_time = conn.get('heartbeat_time')
            if heartbeat_time:
                conn.hset(alarm_statistics, 'controller_linked', 1)
                logger.info('控制器连接恢复！')
            else:
                conn.hset(alarm_statistics, 'controller_linked', 0)
                logger.info('控制器连接断开！')

                if conn.get('http_heartbeat'):
                    conn.delete('http_heartbeat')

            # 上下线发送到智慧消防
    except Exception as e:
        logger.exception(e)


@celery_app.task
@task_wrapper
def check_center_heartbeats():
    """
    智慧消防心跳检查
    :return:
    """
    try:
        if not conn.get('start_time'):
            alarm_statistics = 'alarm_info_statistics'  # 首页所需数据 缓存name
            center_linked = conn.hget(alarm_statistics, 'center_linked')
            center_linked = int(center_linked) if center_linked is not None else None
            center = sync_load_center(conn=conn)
            if center:
                heartbeat_time = conn.get('center_heartbeat_time')
                if heartbeat_time and center_linked == 0:
                    conn.hset(alarm_statistics, 'center_linked', 1)
                    logger.info('智慧消防远程传输信息已配置，中心通讯连接正常！')
                elif heartbeat_time is None and center_linked == 1:
                    conn.hset(alarm_statistics, 'center_linked', 0)
                    logger.info('智慧消防远程传输信息已配置，中心通讯无法连接！')
            elif center_linked == 0:
                conn.hset(alarm_statistics, 'center_linked', 1)
                logger.info('智慧消防远程传输信息未配置，中心通讯连接正常！')

            # 上下线发送到智慧消防
    except Exception as e:
        logger.exception(e)


@celery_app.task
@task_wrapper
def check_reset_error_data():
    try:
        last_reset_snow_id = int(conn.get('last_reset_snow_id'))  # 最近一次复位操作的雪花id
        with db.slice_session() as session:
            # 查询出所有误删的真实报警
            error_data = select(TabAlarmLog).where(TabAlarmLog.is_delete == 0, TabAlarmLog.is_clear == 1)
            error_data = error_data.where(TabAlarmLog.alarm_type == 0, TabAlarmLog.snow_id > last_reset_snow_id)
            records = session.execute(error_data)
            error_data = records.scalars().all()

            if error_data:
                for alarm_log in error_data:
                    # 将错误数据删除
                    alarm_log.is_delete = 1
                    session.flush()

                    # 重新执行时间上报
                    report_data = {
                        'alarm_time': alarm_log.alarm_time.strftime("%Y%m%d%H%M%S"),  # 控制器上报报警时间
                        'controller_num': alarm_log.controller_num,  # 控制器号
                        'loop_num': alarm_log.loop_num,  # 回路号
                        'addr_num': alarm_log.addr_num,  # 地址号
                        'equipment_num': alarm_log.equipment_num,  # 设备号
                        'module_num': alarm_log.module_num,  # 模块号
                        'pass_num': alarm_log.pass_num,  # 通道号
                        'alarm_type_id': alarm_log.alarm_type_id,  # 报警类型id
                        'gb_evt_type_id': alarm_log.gb_evt_type_id,  # 国标类型id
                        'device_type_id': alarm_log.device_type_id,  # 设备类型id
                        'alarm_type': alarm_log.alarm_type,  # 报警类型 0 真实报警 1 模拟报警
                        'snow_id': alarm_log.snow_id,  # 雪花id
                        'error': True,
                        'alarm_log_id': alarm_log.id
                    }

                    if alarm_log.alarm_type_id == 1:
                        controller_report.apply_async(kwargs=report_data, priority=9)
                    else:
                        controller_report.apply_async(kwargs=report_data, priority=20)

    except Exception as e:
        logger.exception(e)


@celery_app.task
@task_wrapper
def check_controller_status():
    """
    检查新版控制状态 是否存在新的报警 2秒查询一次
    :return:
    """
    try:
        # 轮询接口单例运行
        if int(conn.get('controller_update_evt_task_running') or '0'):
            logger.info('查询新版控制器状态任务已经在执行，放弃重复任务！')
            return
        conn.set('check_controller_status_task_running', 1, ex=30)

        # 请求失败超过一定次数，说明没有连接新版控制器，关闭请求 每次服务重启会重新计数
        controller_communication_failure = int(conn.get('controller_communication_failure') or '0')
        if controller_communication_failure > 50:
            logger.info('新版控制器状态查询跳过！')
            conn.delete('heartbeat_time')
            return

        # crt序列号生成后存储在mysql的tab_system_param表中 项目初始化的时候读取到redis中
        system_param = sync_load_system_param(conn)
        crt_sn = system_param.get('crt_sn')

        data = {'crt_sn': crt_sn, 'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        headers = {"Connection": "close"}

        url = cfg_class.CONTROLLER_URL % (cfg_class.CONTROLLER_HOST, cfg_class.CONTROLLER_PORT, 'qry_state_api')
        resp = requests.post(url, json=data, timeout=cfg_class.GATEWAY_TIMEOUT, headers=headers)
        controller_resp = json.loads(resp.text)
        if controller_resp.get('code') != 0:
            logger.error(f"查询控制器状态信息错误:{controller_resp.get('msg')}")
            return

        logger.info(f'控制器状态查询：{controller_resp}\n')

        # 更新检测控制器过期时间
        if not conn.get('http_heartbeat'):
            conn.set('http_heartbeat', 1)  # 标记为http数据采集 停用can数据采集
        conn.setex('heartbeat_time', cfg_class.REDIS_HEARTBEAT_TIME, int(time.time() * 1000))

        # 如果连接成功，重置请求失败的计数器 检查连接控制器类型标志位，如果为1 需要修改为2   1 老版控制器 2 新版控制器
        if controller_communication_failure:
            conn.set('controller_communication_failure', 0, ex=600)
        if int(conn.get('controller_type') or 2) == 1:
            conn.set('controller_type', 2)

        controller_resp = controller_resp.get('data')
        update_evt_num = controller_resp.get('update_evt_num')

        # 检测是否存在新增数据 如果存在 且查询增量数据任务没有被调用 调用查询增量数据任务
        if update_evt_num > 0 and not int(conn.get('controller_update_evt_task_running') or '0'):
            logger.info('控制器存在增量数据，执行增量数据查询任务！')
            get_controller_update_evt.apply_async(priority=10)
            conn.set('controller_update_evt_task_running', 1, ex=125)

        # 对比首页缓存和轮询接口取到的数据是否一致
        alarm_statistics = redis_factory.get_hash_cache('alarm_info_statistics', conn=conn)
        evt_num = controller_resp.get('evt_num') - controller_resp.get('operate_evt_num')
        evt_num = evt_num if evt_num > 0 else 0
        if int(alarm_statistics.get('all_alarm')) != evt_num:
            conn.hset('alarm_info_statistics', 'all_alarm', evt_num)

        if int(alarm_statistics.get('fire')) != controller_resp.get('alarm_evt_num'):
            conn.hset('alarm_info_statistics', 'fire', controller_resp.get('alarm_evt_num'))
            # 说明火警数量增加，优先处理火警
            conn.set('fire_evt_update', 1)

        if int(alarm_statistics.get('linkage')) != controller_resp.get('action_evt_num'):
            conn.hset('alarm_info_statistics', 'linkage', controller_resp.get('action_evt_num'))
        if int(alarm_statistics.get('feedback')) != controller_resp.get('feedback_evt_num'):
            conn.hset('alarm_info_statistics', 'feedback', controller_resp.get('feedback_evt_num'))
        if int(alarm_statistics.get('malfunction')) != controller_resp.get('fault_evt_num'):
            conn.hset('alarm_info_statistics', 'malfunction', controller_resp.get('fault_evt_num'))
        if int(alarm_statistics.get('shielding')) != controller_resp.get('shielding_evt_num'):
            conn.hset('alarm_info_statistics', 'shielding', controller_resp.get('shielding_evt_num'))
        if int(alarm_statistics.get('supervise')) != controller_resp.get('supervisor_evt_num'):
            conn.hset('alarm_info_statistics', 'supervise', controller_resp.get('supervisor_evt_num'))

        # 检查有无复位
        if controller_resp.get('reset_flag', 0):
            controller_num = int(controller_resp.get('ctrl_no', 0))  # 控制器号
            gb_evt_type_id = 122  # 国标事件类型 复位

            operate_data = {
                'create_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'date_time': datetime.datetime.now().strftime("%Y%m%d%H%M%S"),  # 控制器上报报警时间
                'controller_num': controller_num,  # 控制器号
                'gb_evt_type_id': gb_evt_type_id,  # 国标类型id
                'snow_id': snow_fake_factory.get_id()  # 雪花id
            }

            logger.info(f'控制器转发至控制器操作事件采集：{operate_data}\n')
            controller_operate.apply_async(kwargs=operate_data, priority=8)

    except requests.exceptions.ConnectTimeout as e:
        num = int(conn.get('controller_communication_failure') or '0')
        conn.set('controller_communication_failure', num + 1, ex=600)
        logger.error(f"新版控制器状态查询超时！")

    except Exception as e:
        num = int(conn.get('controller_communication_failure') or '0')
        conn.set('controller_communication_failure', num + 1, ex=600)
        logger.exception(e)
        logger.error(f"新版控制器状态查询错误:{str(e)}")

    finally:
        conn.set('check_controller_status_task_running', 0, ex=30)


@celery_app.task
@task_wrapper
def get_controller_update_evt(crt_sn=None):
    """
    获取新版控制器增量数据
    :param crt_sn: crt序列号
    :return:
    """
    try:
        # 检查crt_sn是否传递 crt序列号生成后存储在mysql的tab_system_param表中 项目初始化的时候读取到redis中
        if not crt_sn:
            system_param = sync_load_system_param(conn)
            crt_sn = system_param.get('crt_sn')

        url = cfg_class.CONTROLLER_URL % (cfg_class.CONTROLLER_HOST, cfg_class.CONTROLLER_PORT, 'qry_update_evt_api')
        headers = {"Connection": "close"}
        request_data = {'crt_sn': crt_sn, "page_size": 20}

        # 每25次自动停止，防止增量数据过多，任务卡死
        for i in range(25):
            # 如果火警事件标识为1 说明存在火警 增加请求参数evt_type=2 为火警
            fire_evt_update = int(conn.get('fire_evt_update') or '0')
            if fire_evt_update:
                request_data['evt_type'] = 2

            logger.info(f'控制器请求增量数据报文请求参数：{request_data} --- {cfg_class.GATEWAY_TIMEOUT} --- {headers}')
            resp = requests.post(url, json=request_data, timeout=cfg_class.GATEWAY_TIMEOUT, headers=headers)

            controller_resp = json.loads(resp.text)
            if controller_resp.get('code') != 0:
                logger.error(f"获取控制器增量数据信息错误:{controller_resp.get('msg')}")
                return

            logger.info(f'控制器增量数据报文：{controller_resp}\n')

            controller_resp = controller_resp.get('data')

            gb_evt_types = {}

            # 如果如果火警事件标识为1 并且拉取的数据为空，说明没有增量的火警事件 重置火警事件标识 并删除请求参数中的事件类型筛选
            if fire_evt_update and not controller_resp.get('records'):
                conn.set('fire_evt_update', 0)
                del request_data['evt_type']

            records = sorted(controller_resp.get('records'), key=lambda x: int(x.get('id')))
            logger.debug(f'根据id升序排序后的报警记录：{records}')

            # 数据处理
            for record in records:
                try:
                    alarm_time = datetime.datetime.strptime(record.get('datetime'), '%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    logger.debug(f"新版控制器，数据报文时间格式错误！\n {e}")
                    alarm_time = datetime.datetime.now()

                gb_evt_type = gb_evt_types.get(record.get('evt_code'))
                if not gb_evt_type:
                    gb_evt_type = sync_load_gb_evt_type_by_id(gb_evt_type_id=record.get('evt_code'), conn=conn)
                    gb_evt_types[record.get('evt_code')] = gb_evt_type

                # 操作事件转发到控制器操作数据采集
                if gb_evt_type.get('type_id') == 7:
                    gb_evt_type_id = int(record.get("evt_code", 0))  # 国标事件类型
                    if gb_evt_type_id == 122:
                        continue

                    controller_num = int(record.get('ctrl_num', 0))  # 控制器号

                    operate_data = {
                        'create_time': alarm_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'date_time': alarm_time.strftime("%Y%m%d%H%M%S"),  # 控制器上报报警时间
                        'controller_num': controller_num,  # 控制器号
                        'gb_evt_type_id': gb_evt_type_id,  # 国标类型id
                        'snow_id': snow_fake_factory.get_id()  # 雪花id
                    }

                    logger.info(f'控制器转发至控制器操作事件采集：{operate_data}\n')
                    controller_operate.apply_async(kwargs=operate_data, priority=20)

                # 设置事件上报数据采集
                else:
                    controller_report_id = int(record.get('id', 0))  # 新版控制器上报记录id
                    controller_num = int(record.get('ctrl_num', 0))  # 控制器号
                    loop_num = int(record.get('loop_num', 0))  # 回路号
                    addr_num = int(record.get('addr_num', 0))  # 地址号

                    equipment_num = int(record.get('dev_num', 0))  # 设备号
                    module_num = int(record.get('module_num', 0))  # 模块号

                    pass_num = int(record.get("pass_num", 0))  # 通道号
                    device_type_id = int(record.get("device_gb_type", 0))  # 国标设备类型

                    # 根据国标事件码查询报警类型
                    gb_evt_type_id = gb_evt_type.get('id')
                    alarm_type_id = gb_evt_type.get('type_id')

                    report_data = {
                        'create_time': alarm_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'alarm_time': alarm_time.strftime("%Y%m%d%H%M%S"),  # 控制器上报报警时间
                        'controller_num': controller_num,  # 控制器号
                        'loop_num': loop_num,  # 回路号
                        'addr_num': addr_num,  # 地址号
                        'equipment_num': equipment_num,  # 设备号
                        'module_num': module_num,  # 模块号
                        'pass_num': pass_num,  # 通道号
                        'alarm_type_id': alarm_type_id,  # 报警类型id
                        'gb_evt_type_id': gb_evt_type_id,  # 国标类型id
                        'device_type_id': device_type_id,  # 设备类型id
                        'alarm_type': 0,  # 报警类型 0 真实报警 1 模拟报警
                        'snow_id': snow_fake_factory.get_id(),  # 雪花id
                        'controller_report_id': controller_report_id  # 新版控制器上报记录id
                    }

                    logger.info(f'控制器转发至控制器事件上报采集：{report_data}\n')
                    controller_report.apply_async(kwargs=report_data, priority=20)

            # 检测是否还有增量数据
            if not controller_resp.get('more_data'):
                break

            time.sleep(0.1)

    except requests.exceptions.ConnectTimeout as e:
        logger.error(f"新版控制器增量事件查询超时！")

    except Exception as e:
        logger.exception(e)
        logger.error(f"采集控制器增量数据错误:{str(e)}")

    finally:
        # 任务运行标识置为0
        conn.set('controller_update_evt_task_running', 0)


@celery_app.task
@task_wrapper
def controller_evt_synchronous():
    """
    首页复位误删数据同步 新版控制器数据同步  首页复位后，重新获取控制器上的数据
    :return:
    """
    try:
        # crt序列号生成后存储在mysql的tab_system_param表中 项目初始化的时候读取到redis中
        system_param = sync_load_system_param(conn)
        crt_sn = system_param.get('crt_sn')

        url = cfg_class.CONTROLLER_URL % (cfg_class.CONTROLLER_HOST, cfg_class.CONTROLLER_PORT, 'qry_evt_ids_api')

        headers = {
            "Connection": "close",
        }
        resp = requests.post(url, json={'crt_sn': crt_sn}, timeout=cfg_class.GATEWAY_TIMEOUT, headers=headers)
        controller_resp = json.loads(resp.text)
        if controller_resp.get('code') != 0:
            logger.error(f"获取控制器事件ids错误:{controller_resp.get('msg')}")
            return

        logger.info(f'控制器事件ids报文：{controller_resp}\n')

        controller_resp = controller_resp.get('data')

        # 数据处理
        ect_ids = controller_resp.get('evt_ids')
        ect_ids = ect_ids.split(',')

        with db.slice_session() as session:
            # 查询出所有被清除的报警
            clear_logs = select(TabAlarmLog).where(TabAlarmLog.is_delete == 0, TabAlarmLog.is_clear == 1)
            clear_logs = clear_logs.where(TabAlarmLog.controller_report_id.in_(ect_ids))
            clear_logs = session.execute(clear_logs)
            clear_logs = clear_logs.scalars().all()

            for alarm_log in clear_logs:
                # 将错误数据删除
                alarm_log.is_delete = 1
                session.flush()

                # 重新执行时间上报
                report_data = {
                    'alarm_time': alarm_log.alarm_time.strftime("%Y%m%d%H%M%S"),  # 控制器上报报警时间
                    'controller_num': alarm_log.controller_num,  # 控制器号
                    'loop_num': alarm_log.loop_num,  # 回路号
                    'addr_num': alarm_log.addr_num,  # 地址号
                    'equipment_num': alarm_log.equipment_num,  # 设备号
                    'module_num': alarm_log.module_num,  # 模块号
                    'pass_num': alarm_log.pass_num,  # 通道号
                    'alarm_type_id': alarm_log.alarm_type_id,  # 报警类型id
                    'gb_evt_type_id': alarm_log.gb_evt_type_id,  # 国标类型id
                    'device_type_id': alarm_log.device_type_id,  # 设备类型id
                    'alarm_type': alarm_log.alarm_type,  # 报警类型 0 真实报警 1 模拟报警
                    'snow_id': alarm_log.snow_id,  # 雪花id
                    'error': True,
                    'alarm_log_id': alarm_log.id
                }
                controller_report.apply_async(kwargs=report_data, priority=20)

    except Exception as e:
        logger.exception(e)
        logger.error(f"采集控制器增量数据错误:{str(e)}")


@celery_app.task
@task_wrapper
def can_data_acquisition():
    """
    can数据处理
    :return:
    """
    try:
        can_info = conn.lpop('can_data')  # 每次定时任务读取
        if not can_info or conn.get('http_heartbeat'):
            return

        can_data = [can_info]

        data = {}  # 缓存多帧数据
        message_time = {}  # 多帧数据时间缓存 用于清除超时还没补齐的多帧数据

        gb_evt_types = {}  # 基于内存的缓存
        device_types = sync_load_device_type(page=0, conn=conn)
        device_types = {device_type.get('zx_device_type'): device_type for device_type in device_types.get('items')}

        for can_info in can_data:
            can_info = json.loads(str(can_info, 'UTF-8'))
            logger.info(f"can数据原始报文：{can_info}")
            data_hex = can_info.get('data_hex')
            sort = can_info.get('sort')  # 时间戳

            while data_hex:
                data_len = data_hex[:2]  # 一帧数据长度（第二位16进制转10进制就是数据长度）
                dlc = int(data_len[-1], 16)  # 一帧数据长度
                one_data_head = data_hex[2:10]  # 帧头
                one_data_data = data_hex[10:10+(dlc*2)]  # 帧数据
                data_hex = data_hex[10 + (dlc * 2):]  # 取出的帧从报文中删除

                logger.debug(f'一帧数据： {data_len + one_data_head + one_data_data}')

                arbitration_id = eval('0x' + one_data_head)
                # 移位分别获取分组号，报文号，源地址，优先级，目的地址，帧类型
                group_id = arbitration_id & 0x7F
                message_id = (arbitration_id >> 7) & 0x3F
                source_address = (arbitration_id >> 13) & 0x3F
                priority = (arbitration_id >> 19) & 0x03
                dest_address = (arbitration_id >> 21) & 0x3F
                frame_type = (arbitration_id >> 27) & 0x03

                # 十进制帧头信息,int(str,进制)
                group_id = int(str(group_id), 16)
                message_id = int(str(message_id), 16)
                source_address = int(str(source_address), 16)
                priority = int(str(priority), 16)
                dest_address = int(str(dest_address), 16)
                frame_type = int(str(frame_type), 16)

                if one_data_data[:2] in ['11', '12']:
                    data[message_id] = {group_id: one_data_data}
                    message_time[message_id] = int(time.time())
                elif data.get(message_id):
                    data[message_id][group_id] = one_data_data

                    if len(data[message_id]) == 4:
                        # 解析完整多帧数据
                        frame_data = data[message_id][1] + data[message_id][2] + data[message_id][3]
                        logger.info(f'多帧数据： {data[message_id]}  {frame_data}')
                        controller_num = int(frame_data[2:4], 16)
                        loop_num = int(frame_data[4:6], 16)
                        addr_num = int(frame_data[6:8], 16)
                        pass_num = int(frame_data[8:10], 16)
                        device_type = int(frame_data[12:14]+frame_data[10:12], 16)
                        event_type = int(frame_data[16:18]+frame_data[14:16], 16)
                        logger.info(f'多帧数据解析： controller_num：{controller_num} loop_num：{loop_num} addr_num：{addr_num} addr_num：{addr_num} pass_num：{pass_num} device_type：{device_type} event_type：{event_type}')

                        gb_evt_type = gb_evt_types.get(event_type)
                        if not gb_evt_type:
                            gb_evt_type = sync_load_gb_evt_type_by_id(gb_evt_type_id=event_type, conn=conn)
                            gb_evt_types[event_type] = gb_evt_type

                        if controller_num and loop_num and addr_num:
                            device = sync_load_device_by_location(controller_num, loop_num, addr_num, conn=conn)
                            device_type_id = device.get('device_type_id')
                        else:
                            device_type = device_types.get(device_type)
                            device_type_id = device_type.get('id') if device_type else 0

                        # 操作事件转发到控制器操作事件解析中 其他报警转发到控制器事件上报记录中
                        if gb_evt_type.get('type_id') == 7:
                            report_data = {
                                'date_time': datetime.datetime.fromtimestamp(sort // 1000).strftime("%Y%m%d%H%M%S"),
                                'controller_num': controller_num,  # 控制器号
                                'gb_evt_type_id': gb_evt_type.get('id'),  # 国标类型id
                                'snow_id': snow_fake_factory.get_id(),  # 雪花id
                            }
                            logger.error("转发到控制器操作事件采集")
                            # 复位事件优先执行
                            if gb_evt_type.get('id') == 122:
                                controller_operate.apply_async(kwargs=report_data, priority=8)
                            else:
                                controller_operate.apply_async(kwargs=report_data, priority=20)

                        else:
                            report_data = {
                                'alarm_time': datetime.datetime.fromtimestamp(sort // 1000).strftime("%Y%m%d%H%M%S"),
                                'controller_num': controller_num,  # 控制器号
                                'loop_num': loop_num,  # 回路号
                                'addr_num': addr_num,  # 地址号
                                'equipment_num': None,  # 设备号
                                'module_num': None,  # 模块号
                                'pass_num': pass_num,  # 通道号
                                'alarm_type_id': gb_evt_type.get('type_id'),  # 报警类型id
                                'gb_evt_type_id': gb_evt_type.get('id'),  # 国标类型id
                                'device_type_id': device_type_id,  # 设备类型id
                                'alarm_type': 0,  # 报警类型 0 真实报警 1 模拟报警
                                'snow_id': snow_fake_factory.get_id(),  # 雪花id
                            }
                            logger.error("转发到事件采集")
                            if gb_evt_type.get('type_id') == 1:
                                controller_report.apply_async(kwargs=report_data, priority=9)
                            else:
                                controller_report.apply_async(kwargs=report_data, priority=20)

                        # 删除已经发出的多帧数据
                        del data[message_id]
                        del message_time[message_id]

                # 应急疏散事件相关
                # if one_data_data[:2] in ['2D', '2E']:
                #     data[message_id] = {group_id: one_data_data}
                # elif data.get(message_id):
                #     data[message_id][group_id] = one_data_data
                #
                #     if len(data[message_id]) == 4:
                #         # 解析完整多帧数据
                #         logger.error(f'3333333 {data[message_id]}')

                else:
                    logger.debug(f'抛弃单帧数据： {data_len + one_data_head + one_data_data}')

                # 三秒刷新一次控制器时间戳
                heartbeat_time = int(conn.get('heartbeat_time') or 0)
                if int(time.time() * 1000) - heartbeat_time > 3000 or not heartbeat_time:
                    conn.setex('heartbeat_time', cfg_class.REDIS_HEARTBEAT_TIME, int(time.time() * 1000))

            # 删除超时还没有补齐的多帧数据
            now_stamp = int(time.time())
            del_message_ids = []
            for message_id, time_stamp in message_time.items():
                if now_stamp - time_stamp > 10:
                    del_message_ids.append(message_id)

            for message_id in del_message_ids:
                del data[message_id]
                del message_time[message_id]

            # 如果还有没超时且未补齐的多帧数据 读取下一条报文
            if data:
                new_can_info = None
                while not new_can_info:
                    time.sleep(0.5)
                    new_can_info = conn.lpop('data')
                can_data.append(new_can_info)

    except Exception as e:
        logger.exception(e)
        logger.error(f"采集控制器can增量数据错误:{str(e)}")


# @celery_app.task
# @task_wrapper
# def update_alarm_info():
#     """
#     更新首页报警统计
#     :return:
#     """
#     while True:
#         is_update_alarm_info = int(conn.get('is_update_alarm_info') or 0)
#         if is_update_alarm_info == 0:
#             break
#         else:
#             time.sleep(1)
#
#     with db.slice_session() as session:
#         qry_func = select(TabAlarmLog).where(TabAlarmLog.is_delete == 0, TabAlarmLog.is_clear == 0)
#         qry_func = qry_func.order_by(TabAlarmLog.snow_id)
#         alarm_logs = session.execute(qry_func)
#         alarm_logs = alarm_logs.scalars().all()
#
#     # 标记正在有任务更新报警统计
#     conn.set('is_update_alarm_info', 1)
#
#     # params_md5 = hash_func_params(is_clear=0)
#     # alarm_log_name = f'tab_alarm_log-records:{params_md5}'
#
#     alarm_info_statistics = {
#         "all_alarm": 0,
#         "first_fire": 0,
#         "fire": 0,
#         "linkage": 0,
#         "feedback": 0,
#         "malfunction": 0,
#         "shielding": 0,
#         "supervise": 0,
#         "vl_malfunction": 0,
#         "vl_shielding": 0,
#         "analog_all_alarm": 0,
#         "analog_fire": 0,
#         "analog_linkage": 0,
#         "analog_feedback": 0,
#         "analog_malfunction": 0,
#         "analog_shielding": 0,
#         "analog_supervise": 0,
#         "analog_vl_malfunction": 0,
#         "analog_vl_shielding": 0,
#         "controller_linked": 1,
#         "center_linked": 1
#     }
#
#     for alarm_log in alarm_logs:
#         # 检查报警列表缓存
#         # device_alarm_key = f'{alarm_log.controller_num}-{alarm_log.loop_num}-{alarm_log.addr_num}-
#         # {alarm_log.pass_num or 0}-{alarm_log.alarm_type_id}'
#
#         # if alarm_log.alarm_status == 0:
#         #     conn.hdel('alarm_list', device_alarm_key)
#         # else:
#         #     device_alarm = conn.hget('alarm_list', device_alarm_key)
#         #     if device_alarm:
#         #         device_alarm = json.loads(device_alarm)
#         #         device_alarm.append(alarm_log.gb_evt_type_id)
#         #         conn.hset('alarm_list', device_alarm_key, json.dumps(device_alarm))
#         #     else:
#         #         conn.hset('alarm_list', device_alarm_key, json.dumps([alarm_log.gb_evt_type_id]))
#
#         # conn.hset(alarm_log_name, key=alarm_log.id, value=json.dumps(alarm_log.to_dict()))
#         if alarm_log.alarm_status == 1:
#             if alarm_log.alarm_type == 0:
#                 alarm_info_statistics['all_alarm'] += 1  # 报警总数+1
#             else:
#                 alarm_info_statistics['analog_all_alarm'] += 1  # 模拟报警总数+1
#             if alarm_log.alarm_type_id == 1:
#                 if alarm_log.alarm_type == 0:
#                     alarm_info_statistics['fire'] += 1
#                 else:
#                     alarm_info_statistics['analog_fire'] += 1
#                 if alarm_info_statistics['first_fire'] == 0:  # 首警
#                     alarm_info_statistics['first_fire'] = alarm_log.id
#                     conn.hset('alarm_info_statistics', 'first_fire', alarm_log.id)
#             elif alarm_log.alarm_type_id == 2:
#                 if alarm_log.alarm_type == 0:
#                     alarm_info_statistics['linkage'] += 1
#                 else:
#                     alarm_info_statistics['analog_linkage'] += 1
#             elif alarm_log.alarm_type_id == 3:
#                 if alarm_log.alarm_type == 0:
#                     alarm_info_statistics['feedback'] += 1
#                 else:
#                     alarm_info_statistics['analog_feedback'] += 1
#             elif alarm_log.alarm_type_id == 4:
#                 if alarm_log.alarm_type == 0:
#                     alarm_info_statistics['malfunction'] += 1
#                     if alarm_log.device_type_id in CrtConstant.VL_DEVICE_TYPES:
#                         alarm_info_statistics['vl_malfunction'] += 1
#                 else:
#                     alarm_info_statistics['analog_malfunction'] += 1
#                     if alarm_log.device_type_id in CrtConstant.VL_DEVICE_TYPES:
#                         alarm_info_statistics['analog_vl_malfunction'] += 1
#             elif alarm_log.alarm_type_id == 5:
#                 if alarm_log.alarm_type == 0:
#                     alarm_info_statistics['shielding'] += 1
#                     if alarm_log.device_type_id in CrtConstant.VL_DEVICE_TYPES:
#                         alarm_info_statistics['vl_shielding'] += 1
#                 else:
#                     alarm_info_statistics['analog_shielding'] += 1
#                     if alarm_log.device_type_id in CrtConstant.VL_DEVICE_TYPES:
#                         alarm_info_statistics['analog_vl_shielding'] += 1
#             elif alarm_log.alarm_type_id == 6:
#                 if alarm_log.alarm_type == 0:
#                     alarm_info_statistics['supervise'] += 1
#                 else:
#                     alarm_info_statistics['analog_supervise'] += 1
#
#         elif alarm_log.alarm_status == 0:
#             alarm_info_statistics['all_alarm'] -= 1  # 报警总数+1
#             if alarm_log.alarm_type_id == 1:
#                 alarm_info_statistics['fire'] -= 1
#             elif alarm_log.alarm_type_id == 2:
#                 alarm_info_statistics['linkage'] -= 1
#             elif alarm_log.alarm_type_id == 3:
#                 alarm_info_statistics['feedback'] -= 1
#             elif alarm_log.alarm_type_id == 4:
#                 alarm_info_statistics['malfunction'] -= 1
#                 if alarm_log.device_type_id in CrtConstant.VL_DEVICE_TYPES:
#                     alarm_info_statistics['vl_malfunction'] -= 1
#             elif alarm_log.alarm_type_id == 5:
#                 alarm_info_statistics['shielding'] -= 1
#                 if alarm_log.device_type_id in CrtConstant.VL_DEVICE_TYPES:
#                     alarm_info_statistics['vl_shielding'] -= 1
#             elif alarm_log.alarm_type_id == 6:
#                 alarm_info_statistics['supervise'] -= 1
#
#     conn.hset('alarm_info_statistics', mapping=alarm_info_statistics)
#
#     # 标记没有任务更新报警统计
#     conn.set('is_update_alarm_info', 0)
    

@celery_app.task
@task_wrapper
def read_and_update_alarm_info():
    """
    从队列中读取数据，更新报警计数   单个数据：1,0,1  第一位（1 模拟报警 0 真实报警）  第二位（报警类型）  第三位（0，消失，1，出现）
    :return:
    """
    is_update_alarm_info = int(conn.get('is_update_alarm_info') or 0)
    if is_update_alarm_info:
        return

    # 标记正在有任务更新报警统计
    conn.set('is_update_alarm_info', 1)

    while True:
        alarm_info = conn.lpop('alarm_info_list')  # 每次定时任务读取一个数据
        if not alarm_info:
            break

        if not isinstance(alarm_info, str):
            alarm_info = str(alarm_info, encoding='utf-8')

        alarm_info = alarm_info.split(',')
        alarm_type_id = int(alarm_info[1])
        alarm_type_name = CrtConstant.DEVICE_ALARM_STATUS.get(alarm_type_id) or 'unknown'  # 获取报警类型
        event_state = int(alarm_info[2])

        # 如果控制器类型标记为2 说明为新版控制器且为真实报警 不需要执行计数更新任务 只有采集老版控制数据才要执行更新报警计数任务
        if (int(conn.get('controller_type') or 2) == 2) and (alarm_info[0] == '0'):
            return

        if alarm_type_id not in [7, 8]:
            all_alarm_num = int(conn.hget('alarm_info_statistics', 'all_alarm_num') or 0)  # 查询报警总数(所有记录，出现，消失)
            conn.hset('alarm_info_statistics', 'all_alarm_num', all_alarm_num + 1)  # 更新报警总数

        # 真实报警
        if alarm_info[0] == '0':
            # 更新报警数量缓存
            all_alarm = int(conn.hget('alarm_info_statistics', 'all_alarm') or 0)  # 查询报警总数
            # event_state  事件状态  0，消失，1，出现
            if event_state:
                # 报警总数+1
                if alarm_type_id not in [7, 8]:
                    all_alarm += 1
                # 查询分类报警数量
                num = int(conn.hget('alarm_info_statistics', alarm_type_name) or 0)
                num += 1
            else:
                # 报警总数-1
                if alarm_type_id not in [7, 8]:
                    all_alarm = all_alarm - 1 if all_alarm else all_alarm
                # 查询分类报警数量
                num = int(conn.hget('alarm_info_statistics', alarm_type_name) or 0)
                num = num - 1 if num else num

            conn.hset('alarm_info_statistics', 'all_alarm', all_alarm)  # 更新报警总数
            conn.hset('alarm_info_statistics', alarm_type_name, num)  # 更新分类报警数量

        # 模拟报警
        else:
            # 更新模拟报警数量缓存 模拟报警只有新增报警，没有报警消失
            if alarm_type_id not in [7, 8]:
                analog_all_alarm = int(conn.hget('alarm_info_statistics', 'analog_all_alarm') or 0)  # 查询报警总数
                conn.hset('alarm_info_statistics', 'analog_all_alarm', analog_all_alarm + 1)  # 更新报警总数
            # 查询分类报警数量
            num = int(conn.hget('alarm_info_statistics', f'analog_{alarm_type_name}') or 0)
            conn.hset('alarm_info_statistics', f'analog_{alarm_type_name}', num + 1)  # 更新分类报警数量

    # 标记没有任务更新报警统计
    conn.set('is_update_alarm_info', 0)


@celery_app.task
@task_wrapper
def check_and_update_logs():
    """
    检查或清除报警记录、控制器操作记录、系统操作记录 超过50W条数据清理一次 保留5W条数据
    :return:
    """

    # 检查报警记录表数量
    with db.slice_session() as session:
        # 检查报警记录
        count_alarm_qry_func = select(func.count(TabAlarmLog.id))
        alarm_total = (session.execute(count_alarm_qry_func)).scalar()

        if alarm_total > cfg_class.TABLE_MAX_NUMBER:
            qry_func = select(TabAlarmLog.id)
            qry_func = qry_func.order_by(TabAlarmLog.id.desc())
            qry_func = qry_func.limit(cfg_class.TABLE_KEEP_NUMBER - 1).offset(cfg_class.TABLE_KEEP_NUMBER)
            minimum_id = (session.execute(qry_func)).scalar()

            # 删除小于指定id 且 非火警的记录
            delete_role = delete(TabAlarmLog).where(TabAlarmLog.id < minimum_id and TabAlarmLog.alarm_type_id != 1)
            session.execute(delete_role)
            # 删除小于指定id 且 被清除（被复位）的数据
            delete_role = delete(TabAlarmLog).where(TabAlarmLog.id < minimum_id and TabAlarmLog.is_clear == 1)
            session.execute(delete_role)

        # 检查控制器操作记录
        count_ctrl_op_qry_func = select(func.count(TabControllerOpLog.id))
        ctrl_op_total = (session.execute(count_ctrl_op_qry_func)).scalar()

        if ctrl_op_total > cfg_class.TABLE_MAX_NUMBER:
            qry_func = select(TabControllerOpLog.id)
            qry_func = qry_func.order_by(TabControllerOpLog.id.desc())
            qry_func = qry_func.limit(cfg_class.TABLE_KEEP_NUMBER - 1).offset(cfg_class.TABLE_KEEP_NUMBER)
            minimum_id = (session.execute(qry_func)).scalar()

            delete_role = delete(TabControllerOpLog).where(TabControllerOpLog.id < minimum_id)
            session.execute(delete_role)

        # 检查系统操作记录
        count_system_qry_func = select(func.count(TabSystemLog.id))
        system_total = (session.execute(count_system_qry_func)).scalar()

        if system_total > cfg_class.TABLE_MAX_NUMBER:
            qry_func = select(TabSystemLog.id)
            qry_func = qry_func.order_by(TabSystemLog.id.desc())
            qry_func = qry_func.limit(cfg_class.TABLE_KEEP_NUMBER - 1).offset(cfg_class.TABLE_KEEP_NUMBER)
            minimum_id = (session.execute(qry_func)).scalar()

            delete_role = delete(TabSystemLog).where(TabSystemLog.id < minimum_id)
            session.execute(delete_role)
