import datetime
import time
import logging
import asyncio
import greenlet
import sys
import threading

from os.path import dirname, realpath
from functools import wraps
from sqlalchemy import select, update
from celery.utils.log import get_task_logger
from sqlalchemy.util.concurrency import await_only
from sqlalchemy.util._concurrency_py3k import _AsyncIoGreenlet

from apps.util.celery_module.celery_factory import celery_app, redis, loop_pool
from apps.util.db_module.models import TabControllerOpLog, TabAlarmLog
from apps.util.constant import CrtConstant
from apps.util.db_module.sqlalchemy_factory import db_factory as db
from apps.util.db_module.models import TabDevice, TabAssignDevice, TabFloor
from apps.util.sync_db_api import async_load_controller_by_num, async_load_device_by_location, \
    async_load_device_type_by_id, async_load_gb_evt_type_by_id, async_load_alarm_type

logger = get_task_logger('worker')

root_project_dir = dirname(dirname(dirname(dirname(realpath(__file__)))))
if root_project_dir not in sys.path:
    sys.path.append(root_project_dir)


def running_in_greenlet():
    return isinstance(greenlet.getcurrent(), _AsyncIoGreenlet)


def task_wrapper(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            logger.info('------------ Start ------------')
            logger.info(f'Received data: [{args}] [{kwargs}]')
            # s_time = time.time()
            # if running_in_greenlet:
            #     logger.info(isinstance(greenlet.getcurrent(), _AsyncIoGreenlet))
            #     logger.info(f'异步调用')
            #     result = await_only(func(*args, **kwargs))
            if asyncio.iscoroutinefunction(func):
                logger.info(f'异步调用')
                thread = threading.currentThread()
                logger.info(f'任务线程ID： {thread.ident}')
                if thread.ident not in loop_pool:
                    loop_pool[thread.ident] = asyncio.new_event_loop()
                loop = loop_pool[thread.ident]
                asyncio.set_event_loop(loop)
                # loop = asyncio.get_event_loop()
                result = loop.run_until_complete(func(*args, **kwargs))
            else:
                logger.info(f'直接调用')
                result = func(*args, **kwargs)
            # logger.info(f'Handle Done ==> consume time: {time.time() - s_time}, result: {str(result)}')
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
async def controller_report(x, y):
    gb_evt_type = await async_load_gb_evt_type_by_id(gb_evt_type_id=1, redis=redis)
    print(gb_evt_type)
    add.delay(x, y)
    time.sleep(5)
    return x + y


@celery_app.task
@task_wrapper
async def controller_adjust_time(device_num):
    try:
        controller = await async_load_controller_by_num(controller_num=device_num, redis=redis)

        if controller:
            async with db.slice_session() as session:
                op_log = {
                    'controller_id': controller.id,
                    'controller_num': device_num,
                    'controller_name': controller.name,
                    'description': "时间校准",
                }
                session.add(TabControllerOpLog(**op_log))
                await session.flush()

    except Exception as e:
        logger.exception(e)


@celery_app.task
@task_wrapper
async def controller_report_info(data):
    try:
        alarm_time = datetime.datetime.strptime(data.get('alarm_time'), "%Y%m%d%H%M%S")

        alarm_type_id = data.get('alarm_type_id')
        event_state = data.get('event_state')
        event_statetype = data.get('event_statetype')
        gb_evt_type_id = CrtConstant.RJ45_TO_CAN_EVENT.get(f'{alarm_type_id}-{event_state}-{event_statetype}')

        controller_num = data.get('controller_num')
        loop_num = data.get('loop_num')
        addr_num = data.get('addr_num')

        device_type_id = data.get('device_type_id')

        # 查询国标事件类型
        logger.error(f'gb_evt_type_id: {gb_evt_type_id}')
        gb_evt_type = await async_load_gb_evt_type_by_id(gb_evt_type_id=gb_evt_type_id, redis=redis)
        if not gb_evt_type:
            logger.error(f'无相关国标事件类型 gb_evt_type_id：{gb_evt_type_id}')

        # 查询控制器信息
        controller = None
        if controller_num:
            controller = await async_load_controller_by_num(controller_num=controller_num, redis=redis)
            if not controller:
                logger.error(f'无相关控制器 controller_num：{controller_num}')

        # 检查是否为声光故障和声光屏蔽
        is_vl_malfunction, is_vl_shielding = 0, 0
        if alarm_type_id == 4 and device_type_id in CrtConstant.VL_DEVICE_TYPES:
            is_vl_malfunction = 1
        if alarm_type_id == 5 and device_type_id in CrtConstant.VL_DEVICE_TYPES:
            is_vl_shielding = 1

        # TODO 更新心跳时间

        # TODO 更新报警数量缓存
        name = 'alarm_info_statistics'
        all_alarm = int(await redis.hget(name, 'all_alarm') or 0)  # 查询报警总数
        # 是否为首火警
        fire = int(await redis.hget(name, 'fire') or 0)
        if fire and alarm_type_id == 1:
            await redis.hset(name, 'first_fire', 1)
        await redis.hset(name, 'all_alarm', all_alarm + 1)  # 更新报警总数

        alarm_type = CrtConstant.DEVICE_ALARM_STATUS.get(alarm_type_id)  # 获取报警类型
        num = int(await redis.hget(name, alarm_type) or 0)  # 查询分类报警数量
        await redis.hset(name, alarm_type, num + 1)  # 更新分类报警数量

        if is_vl_malfunction:
            num = int(await redis.hget(name, 'vl_malfunction') or 0)  # 查询分类报警数量
            await redis.hset(name, 'vl_malfunction', num + 1)  # 更新分类报警数量
        elif is_vl_shielding:
            num = int(await redis.hget(name, 'vl_shielding') or 0)  # 查询分类报警数量
            await redis.hset(name, 'vl_shielding', num + 1)  # 更新分类报警数量

        # TODO 更新设备状态  清除设备缓存  更新布点状态  更新布点图状态
        device = None
        if controller_num and loop_num and addr_num:
            async with db.slice_session() as session:
                device_qry_func = select(TabDevice).where(TabDevice.is_delete == 0, TabDevice.controller_num == controller_num, TabDevice.loop_num == loop_num, TabDevice.addr_num == addr_num)
                device = await session.execute(device_qry_func)
                device = device.scalars().first()
                if not device:
                    logger.error(f'无相关设备 controller_num：{controller_num}，loop_num：{loop_num}，addr_num：{addr_num}')
                else:
                    # 更新设备状态
                    if alarm_type_id == 1:
                        device.is_fire = gb_evt_type.get('event_state')
                    elif alarm_type_id == 2:
                        device.is_linkage = gb_evt_type.get('event_state')
                    elif alarm_type_id == 3:
                        device.is_feedback = device.is_linkage = gb_evt_type.get('event_state')
                    elif alarm_type_id == 4:
                        device.is_malfunction = device.is_linkage = gb_evt_type.get('event_state')
                    elif alarm_type_id == 5:
                        device.is_shielding = device.is_linkage = gb_evt_type.get('event_state')

                    if is_vl_malfunction:
                        device.is_vl_malfunction = device.is_linkage = gb_evt_type.get('event_state')
                    elif is_vl_shielding:
                        device.is_vl_shielding = device.is_linkage = gb_evt_type.get('event_state')

                    # 更新设备布点状态
                    if device.is_assign:
                        assign_qry_func = update(TabAssignDevice).set().where(TabAssignDevice.is_delete == 0, TabAssignDevice.device_id == device.id)
                        assign = await session.execute(assign_qry_func)
                        assign = assign.scalars().first()
                        if not assign:
                            logger.error(f'无布点信息 device_id：{device.id}')
                        else:
                            assign.device_status = gb_evt_type.get('event_state')

                            # 更新图纸状态
                            floor_qry_func = select(TabFloor).where(TabFloor.is_delete == 0, TabFloor.id == assign.floor_id)
                            floor = await session.execute(floor_qry_func)
                            floor = floor.scalars().first()
                            if not floor:
                                logger.error(f'无图纸信息 floor_id：{floor.id}')
                            else:
                                floor.is_alarm = gb_evt_type.get('event_state')

                    # TODO 删除缓存 设备缓存 布点缓存 图纸缓存
                    try:
                        records_keys = await redis.keys(f'tab_device-records:*')
                        del_keys = [] + [r.decode() for r in records_keys]
                        if del_keys:
                            # 清除全部缓存键
                            await redis.delete(*del_keys)
                    except Exception as e:
                        msg = '删除缓存错误！'
                        logger.info(msg)
                        logger.exception(e)

                    device = device.to_dict()

        if device:
            description = f"{device.description}_{gb_evt_type.get('name') or '未知事件'}"
        elif controller and loop_num and not addr_num:
            description = f"{controller.get('name')}_{loop_num}回路_{gb_evt_type.get('name') or '未知事件'}"
        elif controller and not loop_num and not addr_num:
            description = f"{controller.get('name')}_{gb_evt_type.get('name') or '未知事件'}"
        else:
            description = f"未知设备_{gb_evt_type.get('name') or '未知事件'}"

        # 创建报警记录
        try:
            async with db.slice_session() as session:
                alarm_log = {
                    "alarm_time": str(alarm_time),
                    "description": description,
                    "controller_num": controller_num,
                    "loop_num": loop_num,
                    "addr_num": addr_num,
                    "equipment_num": data.get('equipment_num'),
                    "module_num": data.get('module_num'),
                    "pass_num": data.get('pass_num'),
                    "device_type_name": device.device_type_name if device else None,
                    "area_name": device.area_name if device else None,
                    "build_name": device.build_name if device else None,
                    "floor_name": device.floor_name if device else None,
                    "device_id": device.id if device else None,
                    "alarm_type_id": alarm_type_id,
                    "alarm_type_name": CrtConstant.ALARM_ID_TO_NAME.get(alarm_type_id),
                    "assign_status": device.is_assign if device else None,
                    "alarm_status": gb_evt_type.get('event_state') if gb_evt_type else None,
                    "gb_evt_type_id": gb_evt_type_id,
                    "gb_evt_type_name": gb_evt_type.get('type_name') if gb_evt_type else '未知事件',
                    "alarm_type": data.get('alarm_type'),
                }
                session.add(TabAlarmLog(**alarm_log))
                await session.flush()
        except Exception as e:
            msg = f'新增报警记录错误！'
            logger.error(msg)
            logger.exception(e)

    except Exception as e:
        logger.exception(e)
