import json

from sanic import Sanic
from sanic.log import logger
from sqlalchemy import select

from crt_api_sys.apps.util.redis_module import redis_factory
from crt_api_sys.apps.util.async_func import hash_func_params, get_short_id
from crt_api_sys.apps.util.db_module.sqlalchemy_factory import db_factory as db
from crt_api_sys.apps.util.db_module.models import TabControllerOpLog, TabSystemLog, TabAlarmLog, TabFloor, \
    TabSystemParam
from crt_api_sys.apps.util.async_db_api import async_load_roles, async_load_device_type, async_load_picture_type, \
    async_load_alarm_type, async_load_gb_evt_type, async_load_device_icon, async_load_assign_devices_by_params, \
    async_load_devices_by_floor_id, async_load_system_param

# 声光设备device_type  10: 1代火灾声光警报器  127: 2代火灾声光警报器  308: Lora无线声光警报器
VL_DEVICE_TYPES = [10, 127, 308]

app = Sanic.get_app('crt_api_sys')


@app.after_server_start
async def boot_init(*_):
    redis = await redis_factory.connecting()
    is_init = await redis.get('is_init')

    if not is_init:
        await redis.flushdb()
        await redis.set('is_init', 1, ex=20)

        # 标记服务启动时间  用于需要服务启动一段时间再进行的任务
        await redis.set('start_time', 1, ex=120)

        # 标记控制器类型
        await redis.set('controller_type', 2)  # 控制器类型 1 老版控制器 2 新版控制器 默认为新版控制器

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
            "center_linked": 1
        }
        # 先写入缓存进行初始化
        await redis.hset('alarm_info_statistics', mapping=alarm_info_statistics)

        # 用户角色
        logger.info('>>> 初始化加载用户角色 <<<')
        roles = await redis.exists('tab_role-records:')
        if not roles:
            await async_load_roles(page=0, redis=redis)

        # 设备类型
        logger.info('>>> 初始化加载设备类型 <<<')
        device_types = await redis.exists('tab_device_type-records:')
        if not device_types:
            await async_load_device_type(page=0, redis=redis)

        # 图片类型
        logger.info('>>> 初始化加载图片类型 <<<')
        picture_types = await redis.exists('tab_picture_type-records:')
        if not picture_types:
            await async_load_picture_type(page=0, redis=redis)

        # 报警类型
        logger.info('>>> 初始化加载报警类型 <<<')
        alarm_types = await redis.exists('tab_alarm_type-records:')
        if not alarm_types:
            await async_load_alarm_type(page=0, redis=redis)

        # 国标事件类型
        logger.info('>>> 初始化加载国标事件类型 <<<')
        gb_evt_types = await redis.exists('tab_gb_evt_type-records:')
        if not gb_evt_types:
            await async_load_gb_evt_type(page=0, redis=redis)

        # 设备图标
        logger.info('>>> 初始化加载设备图标 <<<')
        device_icons = await redis.exists('tab_device_icon-records:')
        if not device_icons:
            await async_load_device_icon(page=0, redis=redis)

        async with db.slice_session() as session:
            logger.info('>>> 获取最新复位雪花id <<<')
            last_reset_snow_id = await redis.get('last_reset_snow_id')
            if not last_reset_snow_id:
                await redis.delete('last_reset_snow_id')

            ctrl_op_log_qry_func = select(TabControllerOpLog).where(TabControllerOpLog.is_delete == 0)
            ctrl_op_log_qry_func = ctrl_op_log_qry_func.where(TabControllerOpLog.gb_evt_type_id == 122)
            ctrl_op_log_qry_func = ctrl_op_log_qry_func.where(TabControllerOpLog.snow_id.isnot(None))
            ctrl_op_log_qry_func = ctrl_op_log_qry_func.order_by(TabControllerOpLog.snow_id.desc())
            alarm_log = await session.execute(ctrl_op_log_qry_func)
            alarm_log = alarm_log.scalars().first()
            alarm_log_last_snow_id = alarm_log.snow_id if alarm_log else 0

            system_log_qry_func = select(TabSystemLog).where(TabSystemLog.is_delete == 0)
            system_log_qry_func = system_log_qry_func.where(TabSystemLog.snow_id.isnot(None))
            system_log_qry_func = system_log_qry_func.order_by(TabSystemLog.snow_id.desc())
            system_log = await session.execute(system_log_qry_func)
            system_log = system_log.scalars().first()
            system_log_last_snow_id = system_log.snow_id if system_log else 0

            last_reset_snow_id = alarm_log_last_snow_id if alarm_log_last_snow_id > system_log_last_snow_id else system_log_last_snow_id
            await redis.set('last_reset_snow_id', last_reset_snow_id)

            logger.info('>>> 首页信息统计 <<<')
            qry_func = select(TabAlarmLog).where(TabAlarmLog.is_delete == 0, TabAlarmLog.is_clear == 0)
            qry_func = qry_func.order_by(TabAlarmLog.snow_id)
            alarm_logs = await session.execute(qry_func)
            alarm_logs = alarm_logs.scalars().all()

            params_md5 = hash_func_params(is_clear=0)
            alarm_log_name = f'tab_alarm_log-records:{params_md5}'

            for alarm_log in alarm_logs:
                # 检查报警列表缓存
                gb_evt_type_id = alarm_log.gb_evt_type_id if alarm_log.gb_evt_type_id != 2 else 3
                device_alarm_key = f'{alarm_log.project_id}-{alarm_log.controller_num}-{alarm_log.loop_num}-{alarm_log.addr_num}-{alarm_log.pass_num or 0}-{alarm_log.alarm_type_id}'
                alarm_log_id_list = await redis.hget('alarm_log_id_list', device_alarm_key)
                if alarm_log.alarm_status == 0:
                    await redis.hdel('alarm_list', device_alarm_key)

                    # 删除报警队列对应数据
                    if alarm_log_id_list:
                        alarm_log_id_list = json.loads(alarm_log_id_list)
                        for alarm_log_id in alarm_log_id_list:
                            await redis.hdel(alarm_log_name, alarm_log_id)
                        await redis.hdel('alarm_log_id_list', device_alarm_key)
                else:
                    device_alarm = await redis.hget('alarm_list', device_alarm_key)
                    if device_alarm:
                        device_alarm = json.loads(device_alarm)
                        device_alarm.append(gb_evt_type_id)
                        await redis.hset('alarm_list', device_alarm_key, json.dumps(device_alarm))
                    else:
                        await redis.hset('alarm_list', device_alarm_key, json.dumps([gb_evt_type_id]))

                    if alarm_log_id_list:
                        if type(alarm_log_id_list) != list:
                            alarm_log_id_list = json.loads(alarm_log_id_list)
                        alarm_log_id_list.append(alarm_log.id)
                        await redis.hset('alarm_log_id_list', device_alarm_key, json.dumps(alarm_log_id_list))
                    else:
                        await redis.hset('alarm_log_id_list', device_alarm_key, json.dumps([alarm_log.id]))

                    await redis.hset(alarm_log_name, key=alarm_log.id, value=json.dumps(alarm_log.to_dict()))

                if alarm_log.alarm_status == 1:
                    if alarm_log.alarm_type == 0:
                        alarm_info_statistics['all_alarm'] += 1  # 报警总数+1
                    else:
                        alarm_info_statistics['analog_all_alarm'] += 1  # 模拟报警总数+1
                    if alarm_log.alarm_type_id == 1:
                        if alarm_log.alarm_type == 0:
                            alarm_info_statistics['fire'] += 1
                        else:
                            alarm_info_statistics['analog_fire'] += 1
                        if alarm_info_statistics['first_fire'] == 0:  # 首警
                            alarm_info_statistics['first_fire'] = alarm_log.id
                            await redis.hset('alarm_info_statistics', 'first_fire', alarm_log.id)
                    elif alarm_log.alarm_type_id == 2:
                        if alarm_log.alarm_type == 0:
                            alarm_info_statistics['linkage'] += 1
                        else:
                            alarm_info_statistics['analog_linkage'] += 1
                    elif alarm_log.alarm_type_id == 3:
                        if alarm_log.alarm_type == 0:
                            alarm_info_statistics['feedback'] += 1
                        else:
                            alarm_info_statistics['analog_feedback'] += 1
                    elif alarm_log.alarm_type_id == 4:
                        if alarm_log.alarm_type == 0:
                            alarm_info_statistics['malfunction'] += 1
                            if alarm_log.device_type_id in VL_DEVICE_TYPES:
                                alarm_info_statistics['vl_malfunction'] += 1
                        else:
                            alarm_info_statistics['analog_malfunction'] += 1
                            if alarm_log.device_type_id in VL_DEVICE_TYPES:
                                alarm_info_statistics['analog_vl_malfunction'] += 1
                    elif alarm_log.alarm_type_id == 5:
                        if alarm_log.alarm_type == 0:
                            alarm_info_statistics['shielding'] += 1
                            if alarm_log.device_type_id in VL_DEVICE_TYPES:
                                alarm_info_statistics['vl_shielding'] += 1
                        else:
                            alarm_info_statistics['analog_shielding'] += 1
                            if alarm_log.device_type_id in VL_DEVICE_TYPES:
                                alarm_info_statistics['analog_vl_shielding'] += 1
                    elif alarm_log.alarm_type_id == 6:
                        if alarm_log.alarm_type == 0:
                            alarm_info_statistics['supervise'] += 1
                        else:
                            alarm_info_statistics['analog_supervise'] += 1

                elif alarm_log.alarm_status == 0:
                    alarm_info_statistics['all_alarm'] = alarm_info_statistics['all_alarm'] - 1 if alarm_info_statistics['all_alarm'] else 0  # 报警总数-1
                    if alarm_log.alarm_type_id == 1:
                        alarm_info_statistics['fire'] = alarm_info_statistics['fire'] - 1 if alarm_info_statistics['fire'] else 0
                    elif alarm_log.alarm_type_id == 2:
                        alarm_info_statistics['linkage'] = alarm_info_statistics['linkage'] - 1 if alarm_info_statistics['linkage'] else 0
                    elif alarm_log.alarm_type_id == 3:
                        alarm_info_statistics['feedback'] = alarm_info_statistics['feedback'] - 1 if alarm_info_statistics['feedback'] else 0
                    elif alarm_log.alarm_type_id == 4:
                        alarm_info_statistics['malfunction'] = alarm_info_statistics['malfunction'] - 1 if alarm_info_statistics['malfunction'] else 0
                        if alarm_log.device_type_id in VL_DEVICE_TYPES:
                            alarm_info_statistics['vl_malfunction'] = alarm_info_statistics['vl_malfunction'] - 1 if alarm_info_statistics['vl_malfunction'] else 0
                    elif alarm_log.alarm_type_id == 5:
                        alarm_info_statistics['shielding'] = alarm_info_statistics['shielding'] - 1 if alarm_info_statistics['shielding'] else 0
                        if alarm_log.device_type_id in VL_DEVICE_TYPES:
                            alarm_info_statistics['vl_shielding'] = alarm_info_statistics['vl_shielding'] - 1 if alarm_info_statistics['vl_shielding'] else 0
                    elif alarm_log.alarm_type_id == 6:
                        alarm_info_statistics['supervise'] = alarm_info_statistics['supervise'] - 1 if alarm_info_statistics['supervise'] else 0

            await redis.hset('alarm_info_statistics', mapping=alarm_info_statistics)

            #  布点相关
            logger.info('>>> 更新图纸缓存 <<<')
            params_md5 = hash_func_params(page=0, per_page=10, is_alarm=1)
            floor_key = f'tab_floor-records:{params_md5}'

            qry_func = select(TabFloor).where(TabFloor.is_delete == 0, TabFloor.alarm > 0)
            floors = await session.execute(qry_func)
            floors = floors.scalars().all()
            for floor in floors:
                await redis.hset(floor_key, key=floor.id, value=json.dumps(floor.to_dict()))
                logger.info('>>> 更新布点缓存 <<<')
                await async_load_assign_devices_by_params(page=0, redis=redis, floor_id=floor.id, refresh_redis=True)
                logger.info('>>> 更新设备缓存 <<<')
                await async_load_devices_by_floor_id(page=0, redis=redis, floor_id=floor.id, refresh_redis=True)

        # 系统配置
        async with db.slice_session() as session:
            qry_func = select(TabSystemParam).where(TabSystemParam.is_delete == 0)
            qry_func = qry_func.order_by(TabSystemParam.update_time.desc())
            system_param = await session.execute(qry_func)
            system_param = system_param.scalars().first()

            if not system_param:
                data = {
                    'carousel_time': 10,
                    'crt_sn': get_short_id()
                }
                system_param = TabSystemParam(**data)
                session.add(system_param)
                await session.flush()

            elif system_param and not system_param.crt_sn:
                system_param.crt_sn = get_short_id()
                await session.flush()
            await redis.hset('tab_system_param-record:', 'carousel_time', system_param.carousel_time)
            await redis.hset('tab_system_param-record:', 'crt_sn', system_param.crt_sn)

        logger.info('初始化成功！！！')

    else:
        logger.info('跳过初始化！！！')
