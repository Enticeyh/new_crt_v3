import re
import os
import copy
import json
import time
import shutil
import zipfile
import aiohttp
import datetime
import xlsxwriter

from pathlib import Path
from functools import partial
from attrdict import AttrDict
from sqlalchemy import select, func, update
from asyncio.exceptions import TimeoutError

from . import BaseHandler, CfResponse, get_args, get_jsons, ErrorCode, redis_factory, db, serial_factory
from crt_api_sys.apps.util.async_func import hash_func_params, data_pag, parse_mysql_url, backups_sql, zip_dir, \
    read_many_sheets_excel, md5_encryption, delete_cache
from crt_api_sys.apps.util.authentication import check_token
from crt_api_sys.apps.util.db_module.models import TabSystemParam, TabCenter, TabSystemLog, TabProject, TabArea, \
    TabBuild, TabFloor, TabController, TabDevice, TabAssignDevice, TabAlarmLog, TabVersion
from crt_api_sys.apps.util.async_db_api import async_load_device_by_location, async_load_system_param, \
    async_load_center, async_load_assign_devices_by_floor_id, async_load_devices_by_floor_id, \
    async_load_device_icon, async_load_user_by_user_id, async_load_picture_type, \
    async_load_last_version, async_load_versions


class AlarmInfo(BaseHandler):
    """报警信息（轮询）"""

    async def get(self, _):
        try:
            data = await redis_factory.get_hash_cache('alarm_info_statistics', redis=self.redis)
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        data = {key: int(value) for key, value in data.items()}

        data["all_alarm"] += data["analog_all_alarm"]
        data["fire"] += data["analog_fire"]
        data["linkage"] += data["analog_linkage"]
        data["feedback"] += data["analog_feedback"]
        data["malfunction"] += data["analog_malfunction"]
        data["shielding"] += data["analog_shielding"]
        data["supervise"] += data["analog_supervise"]
        data["vl_malfunction"] += data["analog_vl_malfunction"]
        data["vl_shielding"] += data["analog_vl_shielding"]

        attrs = ["analog_all_alarm", "analog_fire", "analog_linkage", "analog_feedback", "analog_malfunction",
                 "analog_shielding", "analog_supervise", "analog_vl_malfunction", "analog_vl_shielding"]
        data = {key: value for key, value in data.items() if key not in attrs}

        return await self.write_json(CfResponse(data=data))


class DrawingAssign(BaseHandler):
    """布点信息"""

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            floor_id = get_field("floor_id", field_type=int)
            is_alarm = get_field("is_alarm", field_type=int)

            if is_alarm is not None and is_alarm not in [0, 1]:
                self.logger.error(f'is_alarm: {is_alarm}错误！只能为0或1')
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            assign_devices = await async_load_assign_devices_by_floor_id(page=0, redis=self.redis, floor_id=floor_id)
            devices = await async_load_devices_by_floor_id(page=0, redis=self.redis, floor_id=floor_id)
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        devices = {devices.get('id'): devices for devices in devices.get('items')}
        if is_alarm == 1 and assign_devices.get('items'):
            assign_devices['items'] = [assign_device for assign_device in assign_devices.get('items') if assign_device.get('device_status')]
        elif is_alarm == 0 and assign_devices.get('items'):
            assign_devices['items'] = [assign_device for assign_device in assign_devices.get('items') if assign_device.get('device_status') == 0]

        for assign_device in assign_devices.get('items'):
            device_id = assign_device.get('device_id')
            device = devices.get(device_id)
            if not device:
                continue

            assign_device['is_online'] = device.get('is_online')
            assign_device['alarm'] = device.get('alarm')
            assign_device['fire'] = device.get('fire')
            assign_device['malfunction'] = device.get('malfunction')
            assign_device['vl_malfunction'] = device.get('vl_malfunction')
            assign_device['feedback'] = device.get('feedback')
            assign_device['supervise'] = device.get('supervise')
            assign_device['shielding'] = device.get('shielding')
            assign_device['vl_shielding'] = device.get('vl_shielding')
            assign_device['linkage'] = device.get('linkage')

            controller_num = assign_device.get('controller_num')
            loop_num = assign_device.get('loop_num')
            addr_num = assign_device.get('addr_num')
            assign_device['device_address'] = f"{controller_num}-{loop_num}-{addr_num}"

            gb_evt_type_id = assign_device.get('device_status')
            if assign_device.get('device_status') in []:
                # 查询tab_icon表 找到事件对应的图标 替换现有图标
                icons = await async_load_device_icon(page=0, redis=self.redis, fast_to_dict=True)
                for icon in icons.values():
                    if icon.get('gb_evt_type_id') == gb_evt_type_id:
                        assign_device['path'] = icon.get('path')

        records = assign_devices

        attrs = {'id', 'assign_time', 'coordinate_X', 'coordinate_Y', 'rate', 'angle', 'device_type_id',
                 'device_type_name', 'path', 'description', 'device_status', 'device_id', 'psn', 'device_address',
                 'floor_id', 'is_online', 'alarm', 'fire', 'malfunction', 'vl_malfunction', 'feedback', 'supervise',
                 'shielding', 'vl_shielding', 'linkage'}
        data = [{k: record[k] for k in attrs if k in record} for record in records.get('items')]

        return await self.write_json(CfResponse(data=data))


class Reset(BaseHandler):
    """首页复位"""

    async def test(self, request):

        try:
            is_auth, authenticated = check_token(request)
            if is_auth:
                login_user_id = authenticated.get("user_id")
                token = await redis_factory.get_string_cache(k=f'login:{login_user_id}', to_json=False)
                if request.token != token:
                    return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_TOKEN_INVALID, status=401))

            else:
                login_user_id = None
        except Exception as e:
            msg = f'获取登录用户数据错误！'
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        try:
            # 重置新版控制器的采集定时器，并设置每10分钟自动重置一次
            await self.redis.set('controller_communication_failure', 0, ex=600)

            # 查询所有模拟报警
            async with db.slice_session() as session:
                qry_func = select(TabAlarmLog).where(TabAlarmLog.is_delete == 0, TabAlarmLog.is_clear == 0, TabAlarmLog.alarm_type == 1)
                alarm_logs = await session.execute(qry_func)
                alarm_logs = alarm_logs.scalars().all()

                if alarm_logs:
                    device_ids = [alarm_log.device_id for alarm_log in alarm_logs]
                    device_ids = list(set(device_ids))

                    qry_func = select(TabDevice).where(TabDevice.is_delete == 0, TabDevice.id.in_(device_ids))
                    devices = await session.execute(qry_func)
                    devices = devices.scalars().all()
                    devices = {device.id: device for device in devices}

                    qry_func = select(TabAssignDevice).where(TabAssignDevice.is_delete == 0, TabAssignDevice.device_id.in_(device_ids))
                    assign_devices = await session.execute(qry_func)
                    assign_devices = assign_devices.scalars().all()
                    assign_floor_ids = [assign_device.floor_id for assign_device in assign_devices]
                    assign_floor_ids = list(set(assign_floor_ids))
                    assign_devices = {assign_device.device_id: assign_device for assign_device in assign_devices}

                    qry_func = select(TabFloor).where(TabFloor.is_delete == 0, TabFloor.id.in_(assign_floor_ids))
                    assign_floors = await session.execute(qry_func)
                    assign_floors = assign_floors.scalars().all()
                    assign_floors = {floor.id: floor for floor in assign_floors}

                    # 查询首页缓存
                    data = await redis_factory.get_hash_cache('alarm_info_statistics', redis=self.redis)
                    for key in data.keys():
                        data[key] = int(data[key])
                    # 报警队列缓存名称
                    params_md5 = hash_func_params(is_clear=0)
                    alarm_log_name = f'tab_alarm_log-records:{params_md5}'

                    alarm_types = {
                        1: ['fire'],
                        2: ['linkage'],
                        3: ['feedback'],
                        4: ['malfunction'],
                        5: ['shielding'],
                        6: ['supervise'],
                        7: ['malfunction', 'vl_malfunction'],
                        8: ['shielding', 'vl_shielding'],
                    }

                    for alarm_log in alarm_logs:
                        # 清除模拟报警
                        alarm_log.is_clear = 1
                        # 清除报警队列
                        await self.redis.hdel(alarm_log_name, alarm_log.id)

                        device = devices.get(alarm_log.device_id) if devices else None
                        assign_floor = assign_floors.get(device.assign_floor_id) if assign_floors else None

                        # 更新所有模拟报警涉及到的设备状态 更新所有模拟报警涉及到的楼层状态 更新缓存
                        if device:
                            device.alarm = device.alarm - 1 if device.alarm > 0 else 0
                        if assign_floor:
                            assign_floor.alarm = assign_floor.alarm - 1 if assign_floor.alarm > 0 else 0

                        for alarm_type in alarm_types.get(alarm_log.alarm_type_id):

                            if device:
                                device_alarm_num = getattr(device, alarm_type)
                                device_alarm_num = device_alarm_num - 1 if device_alarm_num > 0 else 0
                                setattr(device, alarm_type, device_alarm_num)

                            if assign_floor:
                                assign_floor_alarm_num = getattr(assign_floor, alarm_type)
                                assign_floor_alarm_num = assign_floor_alarm_num - 1 if assign_floor_alarm_num > 0 else 0
                                setattr(assign_floor, alarm_type, assign_floor_alarm_num)

                    # 清除所有模拟报警涉及到的布点状态
                    for device_id, assign_device in assign_devices.items():
                        device = devices.get(device_id)
                        if device.alarm == 0:
                            assign_device.device_status = 0
                        else:
                            qry_func = select(TabAlarmLog).where(TabAlarmLog.is_delete == 0, TabAlarmLog.is_clear == 0)
                            qry_func = qry_func.where(TabAlarmLog.alarm_type == 0, TabAlarmLog.device_id == device_id)
                            qry_func = qry_func.order_by(TabAlarmLog.update_time.desc())
                            alarm_log = await session.execute(qry_func)
                            alarm_log = alarm_log.scalars().first()
                            if alarm_log:
                                assign_device.device_status = alarm_log.gb_evt_type_id

                    # 如果首警是模拟报警 修改首警为真实报警 如果没有真实报警 置为0
                    qry_func = select(TabAlarmLog).where(TabAlarmLog.is_delete == 0, TabAlarmLog.is_clear == 0)
                    qry_func = qry_func.where(TabAlarmLog.alarm_type == 0, TabAlarmLog.alarm_type_id == 1)
                    qry_func = qry_func.order_by(TabAlarmLog.update_time)
                    alarm_log = await session.execute(qry_func)
                    alarm_log = alarm_log.scalars().first()
                    if alarm_log and data['first_fire'] != alarm_log.id:
                        data['first_fire'] = alarm_log.id
                    elif not alarm_log and data['first_fire'] != 0:
                        data['first_fire'] = 0

                    await session.flush()

                    data['analog_all_alarm'] = 0
                    data['analog_fire'] = 0
                    data['analog_linkage'] = 0
                    data['analog_feedback'] = 0
                    data['analog_malfunction'] = 0
                    data['analog_shielding'] = 0
                    data['analog_supervise'] = 0
                    data['analog_vl_malfunction'] = 0
                    data['analog_vl_shielding'] = 0

                    # 更新缓存
                    await self.redis.hset('alarm_info_statistics', mapping=data)
                    await delete_cache(self.redis, "tab_device")
                    await delete_cache(self.redis, "tab_assign_device")
                    await delete_cache(self.redis, "tab_floor")

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        # 创建复位记录
        if login_user_id:
            try:
                user = await async_load_user_by_user_id(user_id=login_user_id, redis=self.redis)

                async with db.slice_session() as session:
                    system_log = {
                        "description": "复位",
                        "user_id": user.id,
                        "user_name": user.user_name
                    }
                    session.add(TabSystemLog(**system_log))
                    await session.flush()

                    # 删除缓存
                    system_log_name = f'tab_device-records:*'
                    system_log_keys = await self.redis.keys(system_log_name)
                    if system_log_keys:
                        # 清除全部缓存键
                        await self.redis.delete(*system_log_keys)
            except Exception as e:
                msg = f'新增登录记录错误！'
                self.logger.error(msg)
                self.logger.exception(e)
                return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def post(self, request):

        try:
            is_auth, authenticated = check_token(request)
            if is_auth:
                login_user_id = authenticated.get("user_id")
                token = await redis_factory.get_string_cache(k=f'login:{login_user_id}', to_json=False)
                if request.token != token:
                    return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_TOKEN_INVALID, status=401))

            else:
                login_user_id = None
        except Exception as e:
            msg = f'获取登录用户数据错误！'
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        try:
            snow_id = None
            # 获取雪花id
            snow_id_url = request.app.config.SNOW_ID_URL  # 雪花id url
            async with aiohttp.ClientSession() as session:
                async with session.post(snow_id_url) as resp:
                    if resp.status == 200:
                        response = await resp.text()
                        response = json.loads(response)
                        if not response.get('ok'):
                            self.logger.info(f'获取雪花id失败! resp: {json.loads(await resp.text())}')
                        snow_id = response.get("data").get("snow_id")

                        self.logger.info(f'获取雪花id成功! resp: {json.loads(await resp.text())}')

            if not snow_id:
                msg = "复位失败，请联系管理员处理或重试！"
                return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg))
        except Exception as e:
            msg = f'获取复位雪花id失败!'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        try:
            # 更新雪花id
            await self.redis.set('last_reset_snow_id', snow_id)

            # 更新设备状态 布点状态 图纸状态 报警
            update_alarm_log = update(TabAlarmLog).where(TabAlarmLog.is_delete == 0, TabAlarmLog.is_clear == 0).values(is_clear=1)
            update_device = update(TabDevice).where(TabDevice.is_delete == 0).values(alarm=0, fire=0, malfunction=0, vl_malfunction=0, feedback=0, supervise=0, shielding=0, vl_shielding=0, linkage=0)
            update_assign_device = update(TabAssignDevice).where(TabAssignDevice.is_delete == 0).values(device_status=0)
            update_floor = update(TabFloor).where(TabFloor.is_delete == 0).values(alarm=0, fire=0, malfunction=0, vl_malfunction=0, feedback=0, supervise=0, shielding=0, vl_shielding=0, linkage=0)

            async with db.slice_session() as session:
                await session.execute(update_alarm_log)
                await session.execute(update_device)
                await session.execute(update_assign_device)
                await session.execute(update_floor)

        except Exception as e:
            msg = f'数据库更新错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        try:
            # 重置新版控制器的采集定时器，并设置每10分钟自动重置一次
            await self.redis.set('controller_communication_failure', 0, ex=600)

            controller_linked = await self.redis.hget('alarm_info_statistics', 'controller_linked')
            center_linked = await self.redis.hget('alarm_info_statistics', 'center_linked')

            # 清除缓存 报警统计 报警列表 报警图纸列表 报警图纸布点列表 报警图纸设备列表
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
                "controller_linked": int(controller_linked),
                "center_linked": int(center_linked),
                "is_reset": 1
            }
            await self.redis.hset('alarm_info_statistics', mapping=alarm_info_statistics)

            alarm_log_name = f'tab_alarm_log-records:*'
            alarm_log_keys = await self.redis.keys(alarm_log_name)

            floor_name = f'tab_floor-records:*'
            floor_keys = await self.redis.keys(floor_name)

            assign_device_name = f'tab_assign_device-records:*'
            assign_device_keys = await self.redis.keys(assign_device_name)

            device_name = f'tab_device-records:*'
            device_keys = await self.redis.keys(device_name)

            del_keys = [] + alarm_log_keys + floor_keys + assign_device_keys + device_keys
            if del_keys:
                # 清除全部缓存键
                await self.redis.delete(*del_keys)

            # 删除报警去重列表
            await self.redis.delete('alarm_list')

            # 检查有无错误数据
            reports_url = request.app.config.CHECK_RESET_ERROR_DATA_URL  # 检查复位错误数据url
            async with aiohttp.ClientSession() as session:
                async with session.post(reports_url) as resp:
                    if resp.status == 200:
                        response = await resp.text()
                        response = json.loads(response)

                        if not response.get('ok'):
                            self.logger.info(f'检查复位错误数据失败! resp: {json.loads(await resp.text())}')

                        self.logger.info(f'检查复位错误数据成功! resp: {json.loads(await resp.text())}')
        except Exception as e:
            msg = f'复位缓存更新错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        controller_communication_failure = await self.redis.get('controller_communication_failure') or '0'
        if int(controller_linked) == 1 and int(controller_communication_failure) < 50:
            try:
                # 首页复位误删数据同步
                controller_evt_synchronous_url = request.app.config.CONTROLLER_EVT_SYNCHRONOUS_URL
                async with aiohttp.ClientSession() as session:
                    async with session.post(controller_evt_synchronous_url) as resp:
                        if resp.status == 200:
                            response = await resp.text()
                            response = json.loads(response)
                            if not response.get('ok'):
                                self.logger.info(f'复位误删数据重新同步任务下发失败! resp: {json.loads(await resp.text())}')

                            self.logger.info(f'复位误删数据重新同步任务下发成功! resp: {json.loads(await resp.text())}')
            except Exception as e:
                msg = f'复位误删数据重新同步任务下发失败!'
                self.logger.error(msg)
                self.logger.exception(e)
                return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        # 创建复位记录
        try:
            if login_user_id:
                user = await async_load_user_by_user_id(user_id=login_user_id, redis=self.redis)
                user_id = user.id
                user_name = user.user_name
            else:
                user_id, user_name = None, None

            async with db.slice_session() as session:
                system_log = {
                    "snow_id": snow_id,
                    "description": "复位",
                    "user_id": user_id,
                    "user_name": user_name
                }
                session.add(TabSystemLog(**system_log))
                await session.flush()

                # 删除缓存
                system_log_name = f'tab_device-records:*'
                system_log_keys = await self.redis.keys(system_log_name)
                if system_log_keys:
                    # 清除全部缓存键
                    await self.redis.delete(*system_log_keys)
        except Exception as e:
            msg = f'新增复位记录错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())


class AlarmLogs(BaseHandler):
    """报警队列"""

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            alarm_type_id = get_field("alarm_type_id", field_type=int)
            description = get_field("description")
        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            params_md5 = hash_func_params(is_clear=0)
            key = f'tab_alarm_log-records:{params_md5}'
            records = await redis_factory.get_hash_cache(key, redis=self.redis)

            data = []
            if alarm_type_id or description:
                for record in records.values():
                    is_alarm_type_id, is_description, is_vl = True, True, True
                    record = AttrDict(json.loads(record))

                    if alarm_type_id in [7, 8]:
                        is_vl = False
                        if record.device_type_id in request.app.config.VL_DEVICE_TYPES:
                            if alarm_type_id == 7 and record.alarm_type_id == 4:
                                is_vl = True
                            elif alarm_type_id == 8 and record.alarm_type_id == 5:
                                is_vl = True
                    elif alarm_type_id:
                        is_alarm_type_id = True if record.alarm_type_id == alarm_type_id else False

                    if description:
                        is_description = True if description in record.description else False

                    if is_alarm_type_id and is_description and is_vl:
                        record = json.dumps(record)
                        data.append(record)

            else:
                data = records

            if isinstance(data, dict):
                data = list(data.values())

            # 排序
            data = [json.loads(record) for record in data]
            data = sorted(data, key=lambda x: datetime.datetime.strptime(x.get('create_time'), "%Y-%m-%d %H:%M:%S"), reverse=True)

            result = data_pag(records=data, page=page, per_page=per_page, to_json=False)

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        result['items'] = [AttrDict(record) for record in result['items']]
        if result['items']:
            for record in result['items']:
                record['occurred_alarm_time'] = record.create_time

                record['device_type_name'] = '未知设备类型' if record.device_type_name is None else record.device_type_name

                # 报警源
                if record.controller_num is None and record.loop_num is None and record.addr_num is None:
                    record['alarm_current'] = None
                else:
                    loop_num = record.loop_num if record.loop_num else '_'
                    addr_num = record.addr_num if record.addr_num else '_'
                    record['alarm_current'] = f"{record.controller_num}-{loop_num}-{addr_num}"

        attrs = {'id', 'occurred_alarm_time', 'description', 'alarm_current', 'pass_num', 'device_type_name',
                 'area_name', 'build_name', 'floor_id', 'floor_name', 'device_id', 'alarm_type_id', 'assign_status',
                 'alarm_type_name', 'gb_evt_type_id', 'gb_evt_type_name', 'alarm_status', 'alarm_type'}

        result['items'] = [{k: record[k] for k in attrs if k in record} for record in result.get('items')]

        return await self.write_json(CfResponse(data=result))


class MockTest(BaseHandler):
    """模拟测试"""

    async def post(self, request):
        get_field = partial(get_jsons, request)

        try:
            controller_num = get_field("controller_num", field_type=int)  # 控制器号
            loop_num = get_field("loop_num", field_type=int)  # 回路号
            addr_num = get_field("addr_num", field_type=int)  # 地址号
            equipment_num = get_field("equipment_num", field_type=int)  # 设备号 应急疏散
            module_num = get_field("module_num", field_type=int)  # 模块号 应急疏散
            pass_num = get_field("pass_num", field_type=int)  # 通道号
            event_type = get_field("alarm_type_id")  # 报警类型

            if event_type == 7:
                event_type = 4
            elif event_type == 8:
                event_type = 5

            if controller_num is None:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK))

            if not all([loop_num, addr_num, event_type]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            if str(event_type) in ['2', '3', '5']:
                event_state = '1'
                event_state_type = '0'
            elif str(event_type) == '4':
                event_state = '1'
                event_state_type = '1'
            elif str(event_type) == '7':
                event_state = '1'
                event_state_type = '1'
            else:
                event_state = '0'
                event_state_type = '0'

            # 查询设备
            device = await async_load_device_by_location(controller_num=int(controller_num), loop_num=int(loop_num),
                                                         addr_num=int(addr_num), redis=self.redis)
            if not device:
                msg = '{controller_num}-{loop_num}-{addr_num} 设备不存在！'
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

            data = {
                "data": [
                    {
                        "device_num": controller_num,
                        "loop_num": loop_num,
                        "addr_num": addr_num,
                        "equipment_num": equipment_num or 0,
                        "module_num": module_num or 0,
                        "pass_num": pass_num,
                        "datetime": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                        "event_type": event_type,
                        'event_state': event_state,
                        'event_statetype': event_state_type,
                        "type": device.device_type_id,
                        'alarm_type': 1,
                    }
                ]
            }

            # 发送到事件处理
            reports_url = request.app.config.REPORTS_URL  # 采集端事件上报url
            async with aiohttp.ClientSession() as session:
                async with session.post(reports_url, data=json.dumps(data)) as resp:
                    if resp.status == 200:
                        response = await resp.text()
                        response = json.loads(response)

                        if not response.get('ok'):
                            self.logger.info(f'模拟测试事件上报失败! resp: {json.loads(await resp.text())}')

                        self.logger.info(f'模拟测试事件上报成功! resp: {json.loads(await resp.text())}')

        except Exception as e:
            msg = f'模拟测试上报失败！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())


class SystemParam(BaseHandler):
    """系统参数"""

    async def get(self, request):
        try:
            record = await async_load_system_param(redis=self.redis)
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        try:
            # 查询当前登陆用户权限
            logger = await async_load_user_by_user_id(user_id=request.ctx.user_id, redis=self.redis)
            temporary_permissions = await self.redis.get(f'temporary_permissions:{logger.id}')
            if logger.role_id not in [0, 1, 2] and not temporary_permissions:
                msg = '当前登陆用户无此权限！'
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg))
        except Exception as e:
            msg = f'权限校验失败！'
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg, status=400))

        if record:
            attrs = {'carousel_time', 'crt_sn'}
            record = {k: record[k] for k in attrs if k in record}

        return await self.write_json(CfResponse(data=record))

    async def put(self, request):
        get_field = partial(get_jsons, request)

        try:
            carousel_time = get_field("carousel_time", field_type=int)
        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

        try:
            # 查询当前登陆用户权限
            logger = await async_load_user_by_user_id(user_id=request.ctx.user_id, redis=self.redis)
            temporary_permissions = await self.redis.get(f'temporary_permissions:{logger.id}')
            if logger.role_id not in [0, 1, 2] and not temporary_permissions:
                msg = '当前登陆用户无此权限！'
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg))
        except Exception as e:
            msg = f'权限校验失败！'
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg, status=400))

        try:
            async with db.slice_session() as session:
                qry_func = select(TabSystemParam).where(TabSystemParam.is_delete == 0).order_by(
                    TabSystemParam.update_time.desc())
                system_param = await session.execute(qry_func)
                system_param = system_param.scalars().first()

                if not system_param:
                    if not all([carousel_time]):
                        return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

                    system_param = {
                        "carousel_time": carousel_time
                    }
                    session.add(TabSystemParam(**system_param))
                    await session.flush()

                else:
                    if carousel_time:
                        system_param.carousel_time = carousel_time

            # 删除缓存
            await self.redis.delete('tab_system_param-record:')

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())


class Center(BaseHandler):
    """监管中心（智慧消防）"""

    async def get(self, request):
        try:
            record = await async_load_center(redis=self.redis)
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        try:
            # 查询当前登陆用户权限
            logger = await async_load_user_by_user_id(user_id=request.ctx.user_id, redis=self.redis)
            temporary_permissions = await self.redis.get(f'temporary_permissions:{logger.id}')
            if logger.role_id not in [0, 1, 2] and not temporary_permissions:
                msg = '当前登陆用户无此权限！'
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg))
        except Exception as e:
            msg = f'权限校验失败！'
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg, status=400))

        if record:
            attrs = {'name', 'ip', 'port', 'protocol', 'code'}
            record = {k: record[k] for k in attrs if k in record}

        return await self.write_json(CfResponse(data=record))

    async def put(self, request):
        get_field = partial(get_jsons, request)

        try:
            name = get_field("name")
            ip = get_field("ip")
            port = get_field("port", field_type=int)
            protocol = get_field("protocol")
            code = get_field("code")

            if ip:
                if '.' in ip and len(ip.split('.')) == 4:
                    pattern = re.compile(r"((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}")
                    if not pattern.findall(ip):
                        msg = f'ip格式错误！'
                        return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))
                else:
                    pattern = re.compile(r"[\w|.|-|+]+\.(com|info|edu|US|org)$")
                    if not pattern.findall(ip):
                        msg = f'ip格式错误！'
                        return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

        try:
            # 查询当前登陆用户权限
            logger = await async_load_user_by_user_id(user_id=request.ctx.user_id, redis=self.redis)
            temporary_permissions = await self.redis.get(f'temporary_permissions:{logger.id}')
            if logger.role_id not in [0, 1, 2] and not temporary_permissions:
                msg = '当前登陆用户无此权限！'
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg))
        except Exception as e:
            msg = f'权限校验失败！'
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg, status=400))

        try:
            async with db.slice_session() as session:
                qry_func = select(TabCenter).where(TabCenter.is_delete == 0).order_by(TabCenter.update_time.desc())
                center = await session.execute(qry_func)
                center = center.scalars().first()

                if not center:
                    if not all([name, ip, port, protocol, code]):
                        return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

                    center = {
                        "name": name,
                        "ip": ip,
                        "port": port,
                        "protocol": protocol,
                        "code": code
                    }
                    session.add(TabCenter(**center))
                    await session.flush()

                else:
                    if name:
                        center.name = name
                    if ip:
                        center.ip = ip
                    if port:
                        center.port = port
                    if protocol:
                        center.protocol = protocol
                    if code:
                        center.code = code

            # 删除缓存
            await self.redis.delete('tab_center-record:')

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def delete(self, request):

        try:
            # 查询当前登陆用户权限
            logger = await async_load_user_by_user_id(user_id=request.ctx.user_id, redis=self.redis)
            temporary_permissions = await self.redis.get(f'temporary_permissions:{logger.id}')
            if logger.role_id not in [0, 1, 2] and not temporary_permissions:
                msg = '当前登陆用户无此权限！'
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg))
        except Exception as e:
            msg = f'权限校验失败！'
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg, status=400))

        try:
            async with db.slice_session() as session:
                qry_func = select(TabCenter).where(TabCenter.is_delete == 0).order_by(TabCenter.update_time.desc())
                center = await session.execute(qry_func)
                center = center.scalars().first()

                if not center:
                    msg = '无监管中心信息！'
                    self.logger.info(msg)
                    return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg))

                center.is_delete = 1

            # 删除缓存
            await self.redis.delete('tab_center-record:')

            # 直接将通讯恢复
            await self.redis.hset('alarm_info_statistics', 'center_linked', 1)

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())


class TestCenter(BaseHandler):
    """测试监管中心"""

    async def get(self, request):

        try:
            center = await async_load_center(redis=self.redis)

            if not center:
                return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_NO_RECORD, msg='没有配置控制中心！'))

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        try:
            # 查询当前登陆用户权限
            logger = await async_load_user_by_user_id(user_id=request.ctx.user_id, redis=self.redis)
            temporary_permissions = await self.redis.get(f'temporary_permissions:{logger.id}')
            if logger.role_id not in [0, 1, 2] and not temporary_permissions:
                msg = '当前登陆用户无此权限！'
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg))
        except Exception as e:
            msg = f'权限校验失败！'
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg, status=400))

        url = request.app.config.CENTER_HEART_URL % (center.ip, center.port)
        data = {
            'code': center.code,
            'datetime': datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        }
        headers = {
            'Content-Type': 'application/json'
        }
        timeout = request.app.config.HTTP_TIMEOUT

        try:
            # 异步点亮传输灯
            request.app.add_task(serial_factory.send_and_wait, name='serial_send')
        except Exception as e:
            self.logger.error('传输灯开启失败！')
            self.logger.debug(e)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=json.dumps(data), headers=headers, timeout=timeout) as resp:
                    try:
                        # 关闭传输灯
                        await request.app.cancel_task('serial_send')
                        request.app.purge_tasks()
                    except Exception as e:
                        self.logger.error('传输灯关闭失败！')
                        self.logger.debug(e)

                    if resp.status == 200:
                        response = await resp.text()
                        response = json.loads(response)

                        if response.get('code') == 0:
                            self.logger.info(f'网络连接测试成功! resp: {json.loads(await resp.text())}')
                            await redis_factory.set_hash_item_cache('alarm_info_statistics', 'center_linked', 1)
                            await redis_factory.set_string_cache('center_heartbeat_time', int(time.time() * 1000), request.app.config.REDIS_GATEWAY_TIME, self.redis)
                            return await self.write_json(CfResponse())

                        elif response.get('code') == 1202:
                            self.logger.info(f'网络连接测试成功，序列号错误! resp: {json.loads(await resp.text())}')
                            await redis_factory.set_hash_item_cache('alarm_info_statistics', 'center_linked', 0)
                            await redis_factory.del_key('center_heartbeat_time')
                            msg, code = f'网络连接测试成功，序列号错误!', 400
                            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_NO_RECORD, msg=msg, code=code))

                        else:
                            self.logger.info(f'网络连接测试失败! resp: {json.loads(await resp.text())}')
                            await redis_factory.set_hash_item_cache('alarm_info_statistics', 'center_linked', 0)
                            await redis_factory.del_key('center_heartbeat_time')
                            msg, code = f'网络连接测试失败!', 400
                            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_NO_RECORD, msg=msg, code=code))

                    else:
                        msg = "网络连接测试请求失败！"
                        return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_NO_RECORD, msg=msg))

        except TimeoutError as e:
            msg = f'网络连接测试请求超时无响应！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg))

        except Exception as e:
            msg = f'网络连接测试请求错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))


class SmartIotData(BaseHandler):

    async def get(self, request):
        """
        如果传递path，使用传递的路径，没有传递path，默认导出到 用户home目录
        导出目录会新增一个smart_iot_data
        导出的目录结构
        smart_iot_data
            -- crt_data.xlsx  # 导出的数据，为excel表格
            -- static
                -- other  # 批量上传的控制器excel文件和设备excel文件
                -- photo  # 布点信息对应的svg图片（楼层图），快速svg图
        """
        get_field = partial(get_args, request)

        try:
            project_id = get_field("project_id", field_type=int)
            path = get_field("path", default=request.app.config.EXPORT_PATH)
            is_system_backups = get_field("is_system_backups", field_type=int, default=0)  # 是否备份系统数据

            if not project_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

            if not path:
                path = os.path.expanduser('~')

            if ' ' in path:
                msg = f"路径 {path} 格式错误，存在空格！"
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))

            if path.endswith('/'):
                path = path[:-1]

            data_path = Path(path)
            if not data_path.is_dir():
                # 如果使用的默认路径 且不存在 创建路径
                if path == request.app.config.EXPORT_PATH:
                    os.makedirs(path, exist_ok=True)
                    os.system(f"chmod 777 {path}")
                else:
                    msg = f"路径 {path} 不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))
        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            # 查询当前登陆用户权限
            logger = await async_load_user_by_user_id(user_id=request.ctx.user_id, redis=self.redis)
            temporary_permissions = await self.redis.get(f'temporary_permissions:{logger.id}')
            if logger.role_id not in [0, 1, 2] and not temporary_permissions:
                msg = '当前登陆用户无此权限！'
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg))
        except Exception as e:
            msg = f'权限校验失败！'
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg, status=400))

        try:
            # 检查导出文件夹数量是否超过5个，超过删除最老的
            dir_list = os.listdir(path)
            export_dir_list = []
            for _dir in dir_list:
                if re.match("^smart_iot_data_.*$", _dir):
                    export_dir_list.append(_dir)
            if len(export_dir_list) >= 5:
                export_dir_list = sorted(export_dir_list, key=lambda x: os.path.getmtime(f'{path}/{x}'))
                shutil.rmtree(f'{path}/{export_dir_list[0]}')

            # 生成导出文件夹名称
            export_dir_name = f'smart_iot_data_{str(datetime.datetime.now().date())}'
            new_export_dir_name = copy.copy(export_dir_name)
            num = 0

            # 检查资源目录是否存在
            while True:
                if Path(f'{path}/{new_export_dir_name}').exists() or Path(f'{path}/{new_export_dir_name}.zip').exists():
                    self.logger.info(f"文件路径 {path}/{new_export_dir_name} 或 {path}/{new_export_dir_name}.zip 被占用！")
                    num += 1
                    new_export_dir_name = f'{export_dir_name}_0{num}' if num < 10 else f'{export_dir_name}_{num}'  # 如果存在，创建新的路径
                    self.logger.info(f'生成新的文件路径 {path}/{new_export_dir_name}！')
                else:
                    export_dir_name = copy.copy(new_export_dir_name)
                    break

        except Exception as e:
            msg = f'生成导出数据文件名称错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, msg=msg, status=500))

        try:
            async with db.slice_session() as session:
                # 检查项目是否存在
                project_qry_func = select(TabProject).where(TabProject.is_delete == 0, TabProject.id == project_id)
                project = await session.execute(project_qry_func)
                project = project.scalars().first()
                if not project:
                    msg = "项目不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_NO_RECORD, msg=msg))

                # 查出项目对应的小区
                area_qry_func = select(TabArea).where(TabArea.is_delete == 0, TabArea.project_id == project_id)
                areas = await session.execute(area_qry_func)
                areas = areas.scalars().all()
                area_ids = [area.id for area in areas]

                # 查出项目对应的楼宇
                build_qry_func = select(TabBuild).where(TabBuild.is_delete == 0, TabBuild.area_id.in_(area_ids))
                builds = await session.execute(build_qry_func)
                builds = builds.scalars().all()

                # 查出项目对应的楼层
                floor_qry_func = select(TabFloor).where(TabFloor.is_delete == 0, TabFloor.area_id.in_(area_ids))
                floors = await session.execute(floor_qry_func)
                floors = floors.scalars().all()
                floor_ids = [floor.id for floor in floors]

                # 查出项目对应的控制器
                controller_qry_func = select(TabController).where(TabController.is_delete == 0)
                controller_qry_func = controller_qry_func.where(TabController.project_id == project_id)
                controllers = await session.execute(controller_qry_func)
                controllers = controllers.scalars().all()
                controller_ids = [controller.id for controller in controllers]

                # 查出项目对应的设备列表
                device_qry_func = select(TabDevice).where(TabDevice.is_delete == 0)
                device_qry_func = device_qry_func.where(TabDevice.controller_id.in_(controller_ids))
                devices = await session.execute(device_qry_func)
                devices = devices.scalars().all()

                # 查出项目对应的布点信息列表
                assign_device_qry_func = select(TabAssignDevice).where(TabAssignDevice.is_delete == 0)
                assign_device_qry_func = assign_device_qry_func.where(TabAssignDevice.floor_id.in_(floor_ids))
                assign_devices = await session.execute(assign_device_qry_func)
                assign_devices = assign_devices.scalars().all()

                # 生成导出文件路径
                self.logger.info("生成资源路径！")
                os.makedirs(f'{path}/{export_dir_name}', exist_ok=True)
                os.makedirs(f'{path}/{export_dir_name}/static', exist_ok=True)

                # 将楼层图复制到指定目录
                try:
                    # 复制静态文件
                    old_file = f'{request.app.config.STATIC_ROOT_PATH}/static/photo'
                    new_file = f'{path}/{export_dir_name}/static/photo'
                    shutil.copytree(old_file, new_file)
                except Exception as e:
                    msg = f'复制布点图错误！'
                    self.logger.error(msg)
                    self.logger.exception(e)
                    return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

                try:
                    # 将数据写入到excel文件，并保存到指定目录
                    excel_path = f'{path}/{export_dir_name}/crt_data.xls'
                    # 创建Excel文件,不保存, 直接输出
                    workbook = xlsxwriter.Workbook(excel_path)

                    # 新增Sheet 项目信息 table_project
                    project_sheet = workbook.add_worksheet("table_project")
                    # 表头
                    title_heads = ["create_time", "update_time", "is_delete", "project_id", "project_name",
                                   "address", "mobile"]
                    project_sheet.write_row(0, 0, title_heads)
                    row_data = [str(project.create_time), str(project.update_time), "False",
                                project.id, project.name, project.address, project.mobile]
                    project_sheet.write_row(1, 0, row_data)

                    # 新增Sheet 小区信息 table_area
                    area_sheet = workbook.add_worksheet("table_area")
                    # 表头
                    title_heads = ["create_time", "update_time", "is_delete", "area_id", "area_name", "project_id"]
                    area_sheet.write_row(0, 0, title_heads)
                    row = 1
                    for area in areas:
                        row_data = [str(area.create_time), str(area.update_time), "False",
                                    area.id, area.name, area.project_id]
                        area_sheet.write_row(row, 0, row_data)
                        row += 1

                    # 新增Sheet 楼宇信息 table_building
                    building_sheet = workbook.add_worksheet("table_building")
                    # 表头
                    title_heads = ["create_time", "update_time", "is_delete", "building_id", "picture_path",
                                   "building_name", "building_describe", "area_id", "picture_type_id"]
                    building_sheet.write_row(0, 0, title_heads)
                    row = 1
                    for build in builds:
                        row_data = [str(build.create_time), str(build.update_time), "False", build.id, build.path,
                                    build.name, build.picture_type_name, build.area_id, build.picture_type_id]
                        building_sheet.write_row(row, 0, row_data)
                        row += 1

                    # 新增Sheet 楼层信息 table_floor
                    floor_sheet = workbook.add_worksheet("table_floor")
                    # 表头
                    title_heads = ["create_time", "update_time", "is_delete", "floor_id", "picture_path",
                                   "floor_name", "floor_describe", "building_id", "picture_type_id"]
                    floor_sheet.write_row(0, 0, title_heads)
                    row = 1
                    for floor in floors:
                        row_data = [str(floor.create_time), str(floor.update_time), "False", floor.id, floor.path,
                                    floor.name, floor.picture_type_name, floor.build_id, floor.picture_type_id]
                        floor_sheet.write_row(row, 0, row_data)
                        row += 1

                    # 新增Sheet 控制器信息 table_controller
                    controller_sheet = workbook.add_worksheet("table_controller")
                    # 表头
                    title_heads = ["create_time", "update_time", "is_delete", "controller_id", "controller_name",
                                   "controller_number", "setup_date", "controller_model", "controller_manufacturer",
                                   "controller_type", "host_controller_id", "is_online", "project_id"]
                    controller_sheet.write_row(0, 0, title_heads)
                    row = 1
                    for controller in controllers:
                        row_data = [str(controller.create_time), str(controller.update_time), "False", controller.id,
                                    controller.name, controller.code, str(controller.setup_date), controller.model,
                                    controller.manufacturer, controller.controller_type, controller.host_id or 0,
                                    "True" if controller.is_online else "False", controller.project_id]
                        controller_sheet.write_row(row, 0, row_data)
                        row += 1

                    # 新增Sheet 设备信息 table_device
                    device_sheet = workbook.add_worksheet("table_device")
                    # 表头
                    title_heads = ["create_time", "update_time", "is_delete", "device_id", "psn", "equipment_id",
                                   "module_id", "loop_number", "position_number", "device_manufacturer", "setup_date",
                                   "device_model", "maintain_cycle", "expiration_date", "notes_info", "controller_id",
                                   "device_type_id", "area", "build", "unit", "floor", "district", "room"]
                    device_sheet.write_row(0, 0, title_heads)
                    row = 1
                    for device in devices:
                        expiration_date = str(device.expiration_date) if device.expiration_date else None
                        row_data = [str(device.create_time), str(device.update_time), "False", device.id, device.psn,
                                    device.equipment_num, device.module_num, device.loop_num, device.addr_num,
                                    device.manufacturer, str(device.setup_date), device.device_model,
                                    device.maintain_cycle, expiration_date, device.description,
                                    device.controller_id, device.device_type_id, device.area,
                                    device.build, device.unit, device.floor, device.district,
                                    device.room]
                        device_sheet.write_row(row, 0, row_data)
                        row += 1

                    # 新增Sheet 布点信息 table_assign_device
                    assign_device_sheet = workbook.add_worksheet("table_assign_device")
                    # 表头
                    title_heads = ["create_time", "update_time", "is_delete", "assign_device_id", "coordinate_X",
                                   "coordinate_Y", "device_status", "rate", "angle", "floor_id", "device_id"]
                    assign_device_sheet.write_row(0, 0, title_heads)
                    row = 1
                    for assign_device in assign_devices:
                        row_data = [str(assign_device.create_time), str(assign_device.update_time), "False",
                                    assign_device.id, assign_device.coordinate_X, assign_device.coordinate_Y,
                                    assign_device.device_status, assign_device.rate, assign_device.angle,
                                    assign_device.floor_id, assign_device.device_id]
                        assign_device_sheet.write_row(row, 0, row_data)
                        row += 1

                    # 保存excel
                    workbook.close()
                except Exception as e:
                    msg = f'生成excel文件错误！'
                    self.logger.error(msg)
                    self.logger.exception(e)
                    return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

                # 系统备份
                if is_system_backups:
                    try:
                        # 系统备份
                        zip_name = f'backups_{str(datetime.datetime.now().date())}'
                        backups_path = f'{path}/{export_dir_name}/{zip_name}'
                        os.makedirs(backups_path, exist_ok=True)

                        # 生成备份sql文件
                        await backups_sql(request.app.config.MYSQL_URL, backups_path)

                        # 复制静态文件
                        old_file = f'{request.app.config.STATIC_ROOT_PATH}/static/photo'
                        new_file = f'{backups_path}/static/photo'
                        shutil.copytree(old_file, new_file)
                    except Exception as e:
                        msg = f'数据库查询错误！'
                        self.logger.error(msg)
                        self.logger.exception(e)
                        return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

                    try:
                        # 压缩并删除备份文件夹
                        os.system(f"cd {path}/{export_dir_name} && zip -m -q -r {zip_name}.zip {zip_name}")
                        self.logger.info(f'生成系统备份数据，系统备份文件为：{backups_path}.zip')
                    except Exception as e:
                        msg = f'压缩失败！'
                        self.logger.error(msg)
                        self.logger.exception(e)
                        return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, status=500))

        try:
            os.system(f"chmod 777 {path}/{export_dir_name}")
        except Exception as e:
            msg = "修改导出文件夹权限失败！"
            self.logger.error(msg)
            self.logger.exception(e)

        return await self.write_json(CfResponse(data=f'导出数据路径为：{path}/{export_dir_name}'))


class Backups(BaseHandler):

    async def get(self, request):
        """
        如果传递path，使用传递的路径，没有传递path，默认备份到 用户home目录
        导出目录会新增一个backups_<date(备份日期)>
        导出的目录结构
        backups_<date>
            -- create_table_backup.sql  # 备份的数据库表结构数据
            -- table_data_backup.sql  # 备份的数据库表数据
            -- static  # 整个静态文件夹
        """
        get_field = partial(get_args, request)

        try:
            path = get_field("path", default=request.app.config.BACKUPS_PATH)
            if not path:
                path = os.path.expanduser('~')

            if ' ' in path:
                msg = f"路径 {path} 格式错误，存在空格！"
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))

            if path.endswith('/'):
                path = path[:-1]

            data_path = Path(path)
            if not data_path.is_dir():
                msg = f"路径 {path} 不存在！"
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, msg=msg, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            # 查询当前登陆用户权限
            logger = await async_load_user_by_user_id(user_id=request.ctx.user_id, redis=self.redis)
            temporary_permissions = await self.redis.get(f'temporary_permissions:{logger.id}')
            if logger.role_id not in [0, 1, 2] and not temporary_permissions:
                msg = '当前登陆用户无此权限！'
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg))
        except Exception as e:
            msg = f'权限校验失败！'
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg, status=400))

        try:
            # 检查备份文件数量是否超过5个，超过删除最老的
            dir_list = os.listdir(path)
            backups_dir_list = []
            for _dir in dir_list:
                if re.match("^backups_.*.zip$", _dir):
                    backups_dir_list.append(_dir)
            if len(backups_dir_list) >= 5:
                backups_dir_list = sorted(backups_dir_list, key=lambda x: os.path.getmtime(f'{path}/{x}'))
                os.remove(f'{path}/{backups_dir_list[0]}')

            zip_name = f'backups_{str(datetime.datetime.now().date())}'
            new_zip_name = copy.copy(zip_name)
            num = 0
            # 检查资源目录是否存在
            while True:
                if Path(f'{path}/{new_zip_name}').exists() or Path(f'{path}/{new_zip_name}.zip').exists():
                    self.logger.info(f"文件路径 {path}/{new_zip_name} 或 {path}/{new_zip_name}.zip 被占用！")
                    num += 1
                    new_zip_name = f'{zip_name}_0{num}' if num < 10 else f'{zip_name}_{num}'  # 如果存在，创建新的路径
                    self.logger.info(f'生成新的文件路径 {path}/{new_zip_name}！')

                else:
                    zip_name = copy.copy(new_zip_name)
                    break

            backups_path = f'{path}/{zip_name}'

            os.makedirs(backups_path, exist_ok=True)

            # 生成备份sql文件
            await backups_sql(request.app.config.MYSQL_URL, backups_path)

            # 复制静态文件
            old_file = f'{request.app.config.STATIC_ROOT_PATH}/static/photo'
            new_file = f'{backups_path}/static/photo'
            shutil.copytree(old_file, new_file)

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        try:
            # 压缩并删除备份文件夹
            os.system(f"cd {path} && zip -m -q -r {zip_name}.zip {zip_name}")
        except Exception as e:
            msg = f'压缩失败！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse(data=f'备份文件路径为：{backups_path}.zip'))


class Upgrade(BaseHandler):

    async def post(self, request):
        """
        一键升级的目录结构
        upgrade
            -- crt_api_sys  # api代码文件
            -- crt_controller_sys  # controller代码文件
            -- upgrade.sql  # sql升级文件
            -- static  # 静态文件
            -- dist  # 前端文件 整个替换
            -- crt_data.xls  # crt导出的excel文件数据
        """
        get_field = partial(get_jsons, request)
        start_time = datetime.datetime.now()  # 用于标记接口用时多久

        try:
            path = get_field("path")
            backups_path = get_field("backups_path", default=request.app.config.BACKUPS_PATH)
            upgrade_type = get_field("upgrade_type", default=1, field_type=int)  # 1. 数据导入 2. 系统升级

            if not path:
                msg = f"请选择升级文件或文件夹！"
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))

            if path.endswith('/'):
                path = path[:-1]

            if not backups_path:
                backups_path = os.path.expanduser('~')

            if backups_path.endswith('/'):
                backups_path = backups_path[:-1]

            if ' ' in path:
                msg = f"路径 {path} 格式错误，存在空格！"
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))

            if ' ' in backups_path:
                msg = f"备份路径 {backups_path} 格式错误，存在空格！"
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))

            if not Path(backups_path).is_dir():
                if backups_path == request.app.config.BACKUPS_PATH:
                    os.makedirs(backups_path, exist_ok=True)
                    os.system(f"chmod 777 {backups_path}")
                else:
                    msg = f"备份路径 {path} 不存在！"
                    return await self.write_json(
                        CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))

            data_path = Path(path)
            if not data_path.exists():
                msg = f"路径 {path} 不存在！"
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            # 查询当前登陆用户权限
            logger = await async_load_user_by_user_id(user_id=request.ctx.user_id, redis=self.redis)
            temporary_permissions = await self.redis.get(f'temporary_permissions:{logger.id}')
            if logger.role_id not in [0, 1, 2] and not temporary_permissions:
                msg = '当前登陆用户无此权限！'
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg))
        except Exception as e:
            msg = f'权限校验失败！'
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg, status=400))

        try:
            is_zip = False
            if data_path.is_file():
                if not path.endswith('zip'):
                    msg = f"文件类型错误，仅支持zip文件！"
                    return await self.write_json(
                        CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))

                try:
                    zip_file = zipfile.ZipFile(path, 'r')
                    zip_name_list = zip_file.namelist()

                    try:
                        zip_name_list[0] = zip_name_list[0].encode('cp437').decode('gbk')
                    except Exception as e:
                        pass

                    if f"{zip_name_list[0]}is_upgraded_backup.txt" in zip_name_list:
                        msg = f"升级备份文件不能直接用于升级！"
                        return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))

                    if upgrade_type == 2 and f"{zip_name_list[0]}version.txt" not in zip_name_list:
                        msg = f"系统升级包不完整，请联系管理员检查系统升级包！"
                        return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))

                    unzip_path = f"{os.path.expanduser('~')}/{zip_name_list[0]}"
                    if Path(unzip_path).exists():
                        self.logger.info(f'解压路径已存在，删除旧文件夹！')
                        shutil.rmtree(unzip_path)

                    os.system(f"unzip -o -q -d {os.path.expanduser('~')} {path}")  # 解压zip文件

                    # 解压后的文件夹路径
                    path = f"{os.path.expanduser('~')}/{zip_name_list[0]}"
                    is_zip = True
                except Exception as e:
                    msg = f'解压文件夹出错，请手动解压后再进行升级！'
                    self.logger.error(msg)
                    self.logger.exception(e)
                    return await self.write_json(
                        CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=500))
            else:
                if Path(f"{os.path.expanduser('~')}/{path.split('/')[-1]}").exists():
                    shutil.rmtree(f"{os.path.expanduser('~')}/{path.split('/')[-1]}")
                shutil.copytree(path, f"{os.path.expanduser('~')}/{path.split('/')[-1]}")
                path = f"{os.path.expanduser('~')}/{path.split('/')[-1]}"

            if path.endswith('/'):
                path = path[:-1]
        except Exception as e:
            self.logger.error('解压失败')
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        if upgrade_type == 1:
            _list_dir = sorted(os.listdir(path))
            if (_list_dir != ['crt_data.xls', 'static']) or (os.listdir(f'{path}/static') != ['photo']):
                msg = f"导入数据包，格式错误！"
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))

        if upgrade_type == 2:
            # 校验超管密码 超级管理员密码规则为superpassword_<year>-<month>-<day>（如superpassword_2022-8-1） md5加密
            now = datetime.datetime.now()
            super_password = md5_encryption(f'{request.app.config.SUPER_PASSWORD}_{now.year}-{now.month}-{now.day}')

            if f'{super_password}.txt' not in os.listdir(path):
                msg = f"导入升级包，格式错误！"
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))

        try:
            # 项目根目录
            root_path = request.app.config.ROOT_PATH
            if root_path.endswith('/'):
                root_path = root_path[:-1]

            root_path_name = root_path.split('/')[-1]
        except Exception as e:
            msg = f'数据校验错误，请重试或联系工程师进行调试！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=500))

        # 只有系统升级需要备份数据
        if upgrade_type == 2:
            try:
                # 备份sql数据
                await backups_sql(request.app.config.MYSQL_URL, root_path)

                # 备份数据不能作为直接升级文件
                is_upgraded_backup = f'{root_path}/is_upgraded_backup.txt'
                os.mknod(is_upgraded_backup)

                # 检查备份文件数量是否超过5个，超过删除最老的
                dir_list = os.listdir(backups_path)
                backups_dir_list = []
                for _dir in dir_list:
                    if re.match("^upgrade_backups_.*.zip$", _dir):
                        backups_dir_list.append(_dir)
                if len(backups_dir_list) >= 5:
                    backups_dir_list = sorted(backups_dir_list, key=lambda x: os.path.getmtime(f'{backups_path}/{x}'))
                    os.remove(f'{backups_path}/{backups_dir_list[0]}')

                # 生成备份路径
                zip_name = f'upgrade_backups_{str(datetime.datetime.now().date())}'
                new_zip_name = copy.copy(zip_name)
                num = 0
                # 检查备份文件路径是否存在
                while True:
                    if Path(f"{backups_path}/{new_zip_name}").exists() or Path(f"{backups_path}/{new_zip_name}.zip").exists():
                        self.logger.info(f"文件路径 {backups_path}/{new_zip_name} 或 {backups_path}/{new_zip_name}.zip 被占用！")
                        num += 1
                        new_zip_name = f'{zip_name}_0{num}' if num < 10 else f'{zip_name}_{num}'
                        self.logger.info(f'生成新的文件路径 {backups_path}/{new_zip_name}！')
                    else:
                        zip_name = f'{copy.copy(new_zip_name)}.zip'
                        break

                backups_zip_path = f'{backups_path}/{zip_name}'

                # 备份整个数据完整代码 并 删除备份sql文件
                os.system(f"cd {root_path} && cd .. &&  zip -q -r {zip_name} {root_path_name} && mv {zip_name} {backups_zip_path}")
                os.system(f"rm {root_path}/*backup.sql && rm {is_upgraded_backup}")

                self.logger.info(f"备份成功！备份路径为：{backups_zip_path}")

                try:
                    os.system(f"chmod 777 {backups_zip_path}")
                except Exception as e:
                    msg = "修改备份文件权限失败！"
                    self.logger.error(msg)
                    self.logger.exception(e)

            except Exception as e:
                self.logger.exception(e)
                return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, status=500))

        try:
            dir_list = os.listdir(path)

            # 项目静态文件目录
            static_root_path = request.app.config.STATIC_ROOT_PATH

            if 'version.txt' in dir_list:
                version_path = f"{path}/version.txt"

                with open(version_path, 'r') as f:
                    data = f.readlines()
                    version_num = data[0][4:].split('.')
                    version_num = int(version_num[0]) * 10000 + int(version_num[1]) * 100 + int(version_num[2])

                    version_info = ""
                    for line in data[2:]:
                        version_info += line

                # 读取最后一个版本号
                last_version = await async_load_last_version(redis=self.redis)
                if last_version and last_version.version_num:
                    old_version_num = last_version.version_num.split('.')
                    old_version_num = int(old_version_num[0]) * 10000 + int(old_version_num[1]) * 100 + int(old_version_num[2])
                    if old_version_num >= version_num:
                        msg = f'系统升级包版本过低，请联系管理员确认！'
                        return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg))

                async with db.slice_session() as session:
                    version = {
                        "version_num": data[0][4:].replace('\n', ''),
                        "notes": version_info,
                    }
                    session.add(TabVersion(**version))

                # 删除缓存
                controller_name = f'tab_version-record*'
                del_keys = await self.redis.keys(controller_name)
                if del_keys:
                    await self.redis.delete(*del_keys)

            if 'crt_api_sys' in dir_list:
                # api 代码文件
                for dir_path, _, filenames in os.walk(f'{path}/crt_api_sys'):
                    for filename in filenames:
                        new_file = f"{root_path}{dir_path.replace(path, '')}/{filename}"
                        old_file = f"{dir_path}/{filename}"
                        shutil.copyfile(old_file, new_file)
                start_time = datetime.datetime.now()  # 重置起始时间 用于睡眠接口 保证文件能被读写到磁盘
                self.logger.info(f"升级api模块成功！")

            if 'crt_controller_sys' in dir_list:
                # controller 代码文件
                for dir_path, _, filenames in os.walk(f'{path}/crt_controller_sys'):
                    for filename in filenames:
                        new_file = f"{root_path}{dir_path.replace(path, '')}/{filename}"
                        old_file = f"{dir_path}/{filename}"
                        shutil.copyfile(old_file, new_file)
                start_time = datetime.datetime.now()  # 重置起始时间 用于睡眠接口 保证文件能被读写到磁盘
                self.logger.info(f"升级controller模块成功！")

            # 遍历文件，查看所有sql文件，create_table_backup.sql为重置或升级表结构，需要放在第一个执行
            sql_files = []
            for file_dir in dir_list:
                if 'create_table_backup.sql' in file_dir:
                    if sql_files:
                        sql_files.insert(0, file_dir)
                    else:
                        sql_files.append(file_dir)
                elif '.sql' in file_dir:
                    if file_dir[:-4].isdigit():
                        version_num = request.app.config.VERSION.split('.')
                        version_num = int(version_num[0]) * 10000 + int(version_num[1]) * 100 + int(version_num[2])
                        if int(file_dir[:-4]) > version_num:
                            sql_files.append(file_dir)
                    else:
                        sql_files.append(file_dir)

            # 执行sql文件
            for file_dir in sql_files:
                # sql 升级文件
                # 解析mysql链接，获取链接信息
                mysql_user, mysql_password, mysql_host, mysql_port, mysql_db = parse_mysql_url(request.app.config.MYSQL_URL)
                self.logger.debug(f"mysql_user: {mysql_user} mysql_password: {mysql_password} mysql_host: {mysql_host} mysql_port: {mysql_port} mysql_db: {mysql_db}")

                # 执行sql文件
                os.system(f"mysql -u{mysql_user} -p{mysql_password} -h {mysql_host} -P {mysql_port} {mysql_db} < {path}/{file_dir}")

                self.logger.info(f"成功执行 {file_dir} ！")

            if 'static' in dir_list:
                # 静态文件
                for dir_path, _, filenames in os.walk(f'{path}/static'):
                    for filename in filenames:
                        new_file = f"{static_root_path}{dir_path.replace(path, '')}/{filename}"
                        old_file = f"{dir_path}/{filename}"
                        shutil.copyfile(old_file, new_file)
                start_time = datetime.datetime.now()  # 重置起始时间 用于睡眠接口 保证文件能被读写到磁盘
                self.logger.info(f"静态文件升级成功！")

            if 'dist' in dir_list:
                # 前端文件
                # new_dir = f"{root_path}/crt_web_sys/dist"
                # old_dir = f"{path}/dist"
                # if Path(new_dir).exists():
                #     shutil.rmtree(new_dir)
                # os.system(f'chmod 777 {root_path}')
                # shutil.copytree(old_dir, new_dir)

                dir_paths = {}
                for dir_path, _, filenames in os.walk(f'{path}/dist'):
                    # 如果复制路径没有在缓存中，创建复制路径和粘贴路径
                    if not dir_paths.get(dir_path):
                        new_dir_path = dir_path.replace(f'{path}/dist', '')
                        new_file_dir = f"{root_path}/crt_web_sys/dist{new_dir_path}"
                        if not Path(new_file_dir).exists():
                            os.makedirs(new_file_dir, exist_ok=True)
                        dir_paths[dir_path] = new_file_dir

                    new_file_dir = dir_paths.get(dir_path, root_path)

                    for filename in filenames:
                        new_file = f"{new_file_dir}/{filename}"
                        old_file = f"{dir_path}/{filename}"
                        shutil.copyfile(old_file, new_file)
                start_time = datetime.datetime.now()  # 重置起始时间 用于睡眠接口 保证文件能被读写到磁盘
                self.logger.info(f"前端升级成功！")

            if 'crt_data.xls' in dir_list:
                async with db.slice_session() as session:
                    # 查询项目是否存在
                    # qry_func = select(TabProject).where(TabProject.is_delete == 0, TabProject.id == project_id)
                    # project = await session.execute(qry_func)
                    # project = project.scalars().first()
                    # if not project:
                    #     msg = f"项目不存在！"
                    #     return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))
                    # project_name = project.name

                    picture_types = await async_load_picture_type(page=0, redis=self.redis, fast_to_dict=True)
                    device_icons = await async_load_device_icon(page=0, redis=self.redis)
                    device_icons = {int(record.get('device_type_id')): record for record in device_icons.get('items')}

                    areas = {}  # 缓存小区id和小区名称
                    builds = {}  # 缓存楼层id和(楼宇名称, 小区id, 小区名称)
                    controllers = {}  # 缓存控制器id和(控制器号, 控制器名称)

                    # crt excel数据解析
                    excel_path = f"{path}/crt_data.xls"
                    all_table_data = read_many_sheets_excel(excel_path, del_excel=False)

                    # 当前登陆用户
                    user_id = request.ctx.user_id
                    user = await async_load_user_by_user_id(user_id=user_id, redis=self.redis)

                    # 将excel数据导入数据库
                    self.logger.info(f"开始进行excel数据导入！")
                    project_ids = []
                    if all_table_data.get('table_project'):
                        table_data = all_table_data.get('table_project')
                        for raw_data in table_data:
                            project = {
                                "id": int(raw_data.get('project_id')),
                                "name": raw_data.get('project_name'),
                                "address": raw_data.get('address'),
                                "mobile": raw_data.get('mobile'),
                                "deploy_users": json.dumps([{"id": user_id, "name": user.user_name}])
                            }
                            session.add(TabProject(**project))
                            await session.flush()
                            project_id = project.get('id')
                            project_name = project.get('name')
                            project_ids.append(project_id)
                    else:
                        project_data = {
                            "name": '默认',
                            "address": '默认',
                            "deploy_users": json.dumps([{"id": user_id, "name": user.user_name}])
                        }
                        project = TabProject(**project_data)
                        session.add(project)
                        await session.flush()
                        project_id = project.id
                        project_name = project.name
                        project_ids.append(project_id)
                    self.logger.info(f"项目数据导入成功！")

                    if all_table_data.get('table_area'):
                        table_data = all_table_data.get('table_area')
                        for raw_data in table_data:
                            project_id_ok = True if int(raw_data.get('project_id')) in project_ids else False
                            project_name_ok = True if project_id_ok and raw_data.get('project_name') else False
                            area = {
                                "id": int(raw_data.get('area_id')),
                                "name": raw_data.get('area_name'),
                                "project_id": int(raw_data.get('project_id')) if project_id_ok else project_id,
                                "project_name": raw_data.get('project_name') if project_name_ok else project_name
                            }
                            session.add(TabArea(**area))
                            await session.flush()
                            areas[int(raw_data.get('area_id'))] = raw_data.get('area_name')
                        self.logger.info(f"小区数据导入成功！")

                    if all_table_data.get('table_building'):
                        table_data = all_table_data.get('table_building')
                        for raw_data in table_data:
                            if raw_data.get('building_describe'):
                                picture_type_name = raw_data.get('building_describe')
                            else:
                                picture_type = picture_types.get(int(raw_data.get('picture_type_id'))) or {}
                                picture_type_name = picture_type.get('name') or ''

                            build = {
                                "id": int(raw_data.get('building_id')),
                                "name": raw_data.get('building_name'),
                                "path": raw_data.get('picture_path'),
                                "picture_type_id": int(raw_data.get('picture_type_id')),
                                "picture_type_name": picture_type_name,
                                "area_id": int(raw_data.get('area_id')),
                                "area_name": areas.get(int(raw_data.get('area_id'))) or ""
                            }
                            session.add(TabBuild(**build))
                            await session.flush()
                            builds[build.get('id')] = (build.get('name'), build.get('area_id'), build.get('area_name'))
                        self.logger.info(f"楼宇数据导入成功！")

                    if all_table_data.get('table_floor'):
                        table_data = all_table_data.get('table_floor')
                        for raw_data in table_data:
                            build_name, area_id, area_name = builds.get(int(raw_data.get('building_id')))
                            if raw_data.get('building_describe'):
                                picture_type_name = raw_data.get('building_describe')
                            else:
                                picture_type = picture_types.get(int(raw_data.get('picture_type_id'))) or {}
                                picture_type_name = picture_type.get('name') or ''
                            floor = {
                                "id": int(raw_data.get('floor_id')),
                                "name": raw_data.get('floor_name'),
                                "path": raw_data.get('picture_path'),
                                "picture_type_id": int(raw_data.get('picture_type_id')),
                                "picture_type_name": picture_type_name,
                                "area_id": area_id,
                                "area_name": area_name,
                                "build_id": int(raw_data.get('building_id')),
                                "build_name": build_name,
                            }
                            session.add(TabFloor(**floor))
                            await session.flush()
                        self.logger.info(f"楼层数据导入成功！")

                    if all_table_data.get('table_controller'):
                        table_data = all_table_data.get('table_controller')
                        for raw_data in table_data:
                            controller = {
                                'id': int(raw_data.get('controller_id')),
                                'project_id': project_id,
                                'project_name': project_name,
                                "name": raw_data.get('controller_name'),
                                "code": int(raw_data.get('controller_number')),
                                "model": raw_data.get('controller_model'),
                                "manufacturer": raw_data.get('controller_manufacturer'),
                                "setup_date": raw_data.get('setup_date') or None,
                                "controller_type": int(raw_data.get('controller_type')),
                                "host_id": int(raw_data.get('host_controller_id')) if raw_data.get('host_controller_id') else None,
                            }
                            session.add(TabController(**controller))
                            await session.flush()
                            controllers[controller.get('id')] = controller.get('code')
                        self.logger.info(f"控制器数据导入成功！")

                    if all_table_data.get('table_device'):
                        table_data = all_table_data.get('table_device')
                        for raw_data in table_data:
                            code = controllers.get(int(raw_data.get('controller_id')))
                            device_icon = device_icons.get(int(raw_data.get('device_type_id')))

                            device = {
                                "id": int(raw_data.get('device_id')),
                                "controller_id": int(raw_data.get('controller_id')),
                                "controller_num": code,
                                "loop_num": int(raw_data.get('loop_number')),
                                "addr_num": int(raw_data.get('position_number')),
                                "equipment_num": int(raw_data.get('equipment_id')) if raw_data.get('equipment_id') else None,
                                "module_num": int(raw_data.get('module_id')) if raw_data.get('module_id') else None,
                                "psn": raw_data.get('psn'),
                                "manufacturer": raw_data.get('device_manufacturer'),
                                "device_model": raw_data.get('device_model'),
                                "maintain_cycle": int(raw_data.get('maintain_cycle')) if raw_data.get('maintain_cycle') else None,
                                "expiration_date": raw_data.get('expiration_date') or None,
                                "description": raw_data.get('notes_info'),
                                "path": device_icon.get('path'),
                                "device_type_id": int(raw_data.get('device_type_id')),
                                "device_type_name": raw_data.get('device_model'),
                                "setup_date": raw_data.get('setup_date') or None,
                                "area": raw_data.get('area') or None,
                                "build": raw_data.get('build') or None,
                                "unit": raw_data.get('unit') or None,
                                "floor": raw_data.get('floor') or None,
                                "district": raw_data.get('district') or None,
                                "room": raw_data.get('room') or None,
                            }
                            session.add(TabDevice(**device))
                            await session.flush()
                        self.logger.info(f"设备数据导入成功！")

                    if all_table_data.get('table_assign_device'):
                        table_data = all_table_data.get('table_assign_device')
                        for raw_data in table_data:
                            device_qry_func = select(TabDevice).where(TabDevice.is_delete == 0, TabDevice.is_assign == 0)
                            device_qry_func = device_qry_func.where(TabDevice.id == int(raw_data.get('device_id')))
                            device = await session.execute(device_qry_func)
                            device = device.scalars().first()
                            if not device:
                                self.logger.info(f"device_id: {int(raw_data.get('device_id'))} 无此设备！")
                                continue
                            device.is_assign = 1
                            device.assign_floor_id = int(raw_data.get('floor_id'))

                            assign_device = {
                                "id": int(raw_data.get('assign_device_id')),
                                "coordinate_X": float(raw_data.get('coordinate_X')),
                                "coordinate_Y": float(raw_data.get('coordinate_Y')),
                                "rate": float(raw_data.get('rate')),
                                "angle": int(raw_data.get('angle')),
                                "width": 1094 * float(raw_data.get('rate')),
                                "height": 1094 * float(raw_data.get('rate')),
                                "device_type_id": device.device_type_id,
                                "device_type_name": device.device_type_name,
                                "path": device.path,
                                "description": device.description,
                                "device_id": int(raw_data.get('device_id')),
                                "psn": device.psn,
                                "controller_num": device.controller_num,
                                "loop_num": device.loop_num,
                                "addr_num": device.addr_num,
                                "equipment_num": device.equipment_num,
                                "module_num": device.module_num,
                                "floor_id": int(raw_data.get('floor_id')),
                            }
                            session.add(TabAssignDevice(**assign_device))
                            await session.flush()

                    self.logger.info(f"布点数据导入成功！")

                self.logger.info(f"excel文件数据导入成功！")

        except Exception as e:
            msg = f'升级出错，请重试或联系工程师进行调试！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        try:
            if is_zip:
                shutil.rmtree(path)
        except Exception as e:
            msg = f'删除解压后文件失败，请手动删除 {path}！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=500))

        # 睡眠30秒 解决CRT升级成功立刻断电重启导致的丢失文件问题
        spend_time = (datetime.datetime.now() - start_time).seconds
        if (30 - spend_time) > 0:
            time.sleep(30 - spend_time)

        return await self.write_json(CfResponse())


class FactoryReset(BaseHandler):

    async def post(self, request):

        try:
            if int(await self.redis.get('factory_reset') or '0'):
                return await self.write_json(CfResponse(data=f'重置正在执行！'))
            await self.redis.set('factory_reset', 1, ex=10)
        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            backups_path = request.app.config.BACKUPS_PATH

            if not Path(backups_path).is_dir():
                os.makedirs(backups_path, exist_ok=True)
                os.system(f"chmod 777 {backups_path}")
        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            # 查询当前登陆用户权限
            logger = await async_load_user_by_user_id(user_id=request.ctx.user_id, redis=self.redis)
            temporary_permissions = await self.redis.get(f'temporary_permissions:{logger.id}')
            if logger.role_id not in [0, 1, 2] and not temporary_permissions:
                msg = '当前登陆用户无此权限！'
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg))
        except Exception as e:
            msg = f'权限校验失败！'
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg, status=400))

        try:
            # 项目根目录
            root_path = request.app.config.ROOT_PATH
            if root_path.endswith('/'):
                root_path = root_path[:-1]

            root_path_name = root_path.split('/')[-1]
        except Exception as e:
            msg = f'数据校验错误，请重试或联系工程师进行调试！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=500))

        try:
            # 备份sql数据
            await backups_sql(request.app.config.MYSQL_URL, root_path)

            # 备份数据不能作为直接升级文件
            is_upgraded_backup = f'{root_path}/is_upgraded_backup.txt'
            if not Path(is_upgraded_backup).exists():
                os.mknod(is_upgraded_backup)

            # 检查备份文件数量是否超过5个，超过删除最老的
            dir_list = os.listdir(backups_path)
            backups_dir_list = []
            for _dir in dir_list:
                if re.match("^upgrade_backups_.*.zip$", _dir):
                    backups_dir_list.append(_dir)
            if len(backups_dir_list) >= 5:
                backups_dir_list = sorted(backups_dir_list, key=lambda x: os.path.getmtime(f'{backups_path}/{x}'))
                os.remove(f'{backups_path}/{backups_dir_list[0]}')

            # 生成备份路径
            zip_name = f'upgrade_backups_{str(datetime.datetime.now().date())}'
            new_zip_name = copy.copy(zip_name)
            num = 0
            # 检查备份文件路径是否存在
            while True:
                if Path(f"{backups_path}/{new_zip_name}").exists() or Path(f"{backups_path}/{new_zip_name}.zip").exists():
                    self.logger.info(f"文件路径 {backups_path}/{new_zip_name} 或 {backups_path}/{new_zip_name}.zip 被占用！")
                    num += 1
                    new_zip_name = f'{zip_name}_0{num}' if num < 10 else f'{zip_name}_{num}'
                    self.logger.info(f'生成新的文件路径 {backups_path}/{new_zip_name}！')
                else:
                    zip_name = f'{copy.copy(new_zip_name)}.zip'
                    break

            backups_zip_path = f'{backups_path}/{zip_name}'

            # 备份整个数据完整代码 并 删除备份sql文件
            os.system(f"cd {root_path} && cd .. &&  zip -q -r {zip_name} {root_path_name} && mv {zip_name} {backups_zip_path}")
            os.system(f"rm {root_path}/*backup.sql && rm {is_upgraded_backup}")

            self.logger.info(f"备份成功！备份路径为：{backups_zip_path}")

            try:
                os.system(f"chmod 777 {backups_zip_path}")
            except Exception as e:
                msg = "修改备份文件权限失败！"
                self.logger.error(msg)
                self.logger.exception(e)

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, status=500))

        try:
            # 重置数据库表数据
            async with db.slice_session() as session:
                table_list = ['tab_alarm_log', 'tab_area', 'tab_assign_device', 'tab_build', 'tab_controller',
                              'tab_controller_op_log', 'tab_device', 'tab_floor', 'tab_maintenance_log',
                              'tab_project', 'tab_project_picture', 'tab_shift_record', 'tab_system_log']

                for table_name in table_list:
                    await session.execute(f"truncate table {table_name}")

            # 重置静态文件 other 和 photo 文件夹
            static_root_path = request.app.config.STATIC_ROOT_PATH  # 项目静态文件目录
            os.system(f"rm {static_root_path}/static/other/*")
            os.system(f"rm {static_root_path}/static/photo/*")

        except Exception as e:
            msg = f'重置数据失败！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=500))

        await self.redis.delete('factory_reset')

        return await self.write_json(CfResponse())


class UpdateReset(BaseHandler):

    async def post(self, _):

        try:
            await self.redis.hdel('alarm_info_statistics', 'is_reset')
        except Exception as e:
            msg = '更新缓存错误！'
            self.logger.info(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM))

        return await self.write_json(CfResponse())


class UpdateAssign(BaseHandler):

    async def post(self, _):

        try:
            await self.redis.hdel('alarm_info_statistics', 'is_assign_update')
        except Exception as e:
            msg = '更新缓存错误！'
            self.logger.info(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM))

        return await self.write_json(CfResponse())


class Help(BaseHandler):

    async def get(self, request):

        data = {
            "help_path": request.app.config.HELP_PATH
        }

        return await self.write_json(CfResponse(data=data))


class Template(BaseHandler):

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            template_type = get_field("template_type", field_type=int)  # 1 设备模板  2 控制器模板

            if not template_type:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        template_path = ''
        if template_type == 1:
            template_path = request.app.config.DEVICE_TEMPLATE_PATH
        elif template_type == 2:
            template_path = request.app.config.CONTROLLER_TEMPLATE_PATH

        data = {
            "template_path": template_path
        }

        return await self.write_json(CfResponse(data=data))


class Projects(BaseHandler):
    """项目"""

    async def get(self, _):
        try:
            async with db.slice_session() as session:
                qry_func = select(TabProject).where(TabProject.is_delete == 0)

                records = await session.execute(qry_func)
                records = records.scalars().all()
                records = [record.to_dict() for record in records]

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        if records:
            for record in records:
                record['deploy_users'] = json.loads(record.get('deploy_users'))

        attrs = {'id', 'name', 'address', 'mobile', 'deploy_users'}
        records = [{k: record[k] for k in attrs if k in record} for record in records]

        return await self.write_json(CfResponse(data=records))


class LastVersion(BaseHandler):

    async def get(self, request):
        try:
            record = await async_load_last_version(redis=self.redis)

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        data = {
            'id': 0,
            'upgrade_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'version_num': request.app.config.VERSION,
            'notes': ''
        }

        if record:
            if record.get('version_num') == request.app.config.VERSION:
                record['upgrade_time'] = record.get('create_time')
                record['notes'] = record.get('notes')

                attrs = {'id', 'upgrade_time', 'version_num', 'notes'}
                data = {k: record[k] for k in attrs if k in record}

        return await self.write_json(CfResponse(data=data))


class Versions(BaseHandler):

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)
        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            records = await async_load_versions(redis=self.redis, page=page, per_page=per_page)

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        if records['items']:
            for record in records['items']:
                record['upgrade_time'] = record.get('create_time')
                record['notes'] = record.notes

        attrs = {'id', 'upgrade_time', 'version_num', 'notes'}
        records['items'] = [{k: record[k] for k in attrs if k in record} for record in records.get('items')]

        return await self.write_json(CfResponse(data=records))

