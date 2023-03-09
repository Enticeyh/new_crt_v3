import datetime

from functools import partial
from sqlalchemy import select, func
from attrdict import AttrDict

from . import BaseHandler, CfResponse, get_args, ErrorCode, db
from crt_api_sys.apps.util.db_module.models import TabArea, TabBuild, TabFloor, TabProjectPicture
from crt_api_sys.apps.util.async_db_api import async_load_alarm_logs_by_params, async_load_alarm_log_by_id, \
    async_load_build_drawings_by_params, async_load_assign_devices_by_params, async_load_controller_op_logs_by_params, \
    async_load_maintenance_logs_by_params, async_load_shift_records_by_params, async_load_system_logs_by_params, \
    async_load_picture_type_by_id


class AlarmLogsList(BaseHandler):
    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            is_clear = get_field("is_clear", field_type=int)  # 是否清除（0 否 1 是）

            description = get_field("description")
            st = get_field("st")
            et = get_field("et")
            area_id = get_field("area_id", field_type=int)
            build_id = get_field("build_id", field_type=int)
            floor_id = get_field("floor_id", field_type=int)
            controller_num = get_field("controller_num", field_type=int)
            loop_num = get_field("loop_num", field_type=int)
            addr_num = get_field("addr_num", field_type=int)
            equipment_num = get_field("equipment_num", field_type=int)
            module_num = get_field("module_num", field_type=int)
            alarm_type_id = get_field("alarm_type_id", field_type=int)
            alarm_status = get_field("alarm_status", field_type=int)
            alarm_type = get_field("alarm_type", field_type=int)
            device_id = get_field("device_id", field_type=int)
            export_flag = get_field("export_flag", field_type=int)

            if is_clear is not None and is_clear not in [0, 1]:
                self.logger.error(f'is_clear: {is_clear}错误！只能为0或1')
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

            if export_flag is not None and export_flag != 1:
                self.logger.error(f'export_flag: {export_flag}错误！只能为1')
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

            device_type_ids = None
            if alarm_type_id in [7, 8]:
                device_type_ids = request.app.config.VL_DEVICE_TYPES
                if alarm_type_id == 7:
                    alarm_type_id = 4
                elif alarm_type_id == 8:
                    alarm_type_id = 5

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            records = await async_load_alarm_logs_by_params(redis=self.redis, page=page, per_page=per_page, st=st,
                                                            et=et, is_clear=is_clear, description=description,
                                                            area_id=area_id, build_id=build_id, floor_id=floor_id,
                                                            controller_num=controller_num, loop_num=loop_num,
                                                            addr_num=addr_num, equipment_num=equipment_num,
                                                            module_num=module_num, alarm_type_id=alarm_type_id,
                                                            alarm_status=alarm_status, alarm_type=alarm_type,
                                                            device_id=device_id, device_type_ids=device_type_ids,
                                                            origin='db')
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        if records['items']:
            for record in records['items']:
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
        records['items'] = [{k: record[k] for k in attrs if k in record} for record in records.get('items')]

        if export_flag is not None:
            datas = records.get("items")
            file_name = f"报警记录"
            mapping = [
                ('ID', {'title': 'id'}),
                ('发生时间', {'title': 'occurred_alarm_time'}),
                ('描述', {'title': 'description'}),
                ('报警源', {'title': 'alarm_current'}),
                ('通道号', {'title': 'pass_num'}),
                ('设备类型', {'title': 'device_type_name'}),
                ('报警类型', {'title': 'alarm_type_name'}),
                ('小区名称', {'title': 'area_name'}),
                ('楼宇名称', {'title': 'build_name'}),
                ('楼层名称', {'title': 'floor_name'}),
                ('报警状态', {'title': 'alarm_status', 'value': {'0': '消失', '1': '出现', '2': '丢弃'}}),
                ('事件国标类型', {'title': 'gb_evt_type_name'}),
                ('报警类型', {'title': 'alarm_type', 'value': {'0': '真实报警', '1': '模拟报警'}}),
            ]
            return await self.write_excel(file_name=file_name, datas=datas, mapping=mapping)

        return await self.write_json(CfResponse(data=records))


class AlarmLog(BaseHandler):

    async def get(self, _, alarm_log_id):

        try:
            record = await async_load_alarm_log_by_id(redis=self.redis, alarm_log_id=alarm_log_id)
            if not record:
                msg = f'alarm_log_id: {alarm_log_id} 数据库无匹配记录！'
                self.logger.info(msg)
                msg = '暂无相关报警信息！'
                return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_NO_RECORD, msg=msg, status=200))

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        record['occurred_alarm_time'] = record.create_time

        # 报警源
        if record.controller_num is None and record.loop_num is None and record.addr_num is None:
            record['alarm_current'] = None
        else:
            loop_num = record.loop_num if record.loop_num else '_'
            addr_num = record.addr_num if record.addr_num else '_'
            record['alarm_current'] = f"{record.controller_num}-{loop_num}-{addr_num}"

        record['device_type_name'] = '未知设备类型' if record.device_type_name is None else record.device_type_name

        attrs = {'id', 'occurred_alarm_time', 'description', 'alarm_current', 'pass_num', 'device_type_name',
                 'area_name', 'build_name', 'floor_id', 'floor_name', 'device_id', 'alarm_type_id', 'assign_status',
                 'alarm_type_name', 'gb_evt_type_id', 'gb_evt_type_name', 'alarm_status', 'alarm_type'}
        record = {k: record[k] for k in attrs if k in record}

        return await self.write_json(CfResponse(data=record))


class BuildDrawings(BaseHandler):
    """图纸"""

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            area_id = get_field("area_id", field_type=int)
            build_id = get_field("build_id", field_type=int)
            floor_id = get_field("floor_id", field_type=int)
            is_alarm = get_field("is_alarm", field_type=int)
            state = get_field("state", field_type=int)  # 1 火警 2 联动 3 反馈 4 故障 5 屏蔽 6 监管 7 声光故障 8 声光屏蔽

            export_flag = get_field("export_flag", field_type=int)

            if is_alarm is not None and is_alarm not in [0, 1]:
                self.logger.error(f'is_alarm: {is_alarm}错误！只能为0或1')
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

            if export_flag is not None and export_flag != 1:
                self.logger.info(f'export_flag: {export_flag}错误！只能为1')
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            records = await async_load_build_drawings_by_params(redis=self.redis, page=page, per_page=per_page,
                                                                area_id=area_id, build_id=build_id, floor_id=floor_id,
                                                                is_alarm=is_alarm, state=state)
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        if records['items']:
            for record in records['items']:
                # 是否报警
                record['is_alarm'] = 1 if record.get('alarm') else 0

        attrs = {'id', 'name', 'path', 'quick_svg_path', 'picture_type_id', 'picture_type_name',
                 'area_id', 'area_name', 'build_id', 'build_name', 'is_alarm'}
        records['items'] = [{k: record[k] for k in attrs if k in record} for record in records.get('items')]

        if export_flag is not None:
            datas = records.get("items")
            file_name = f"图纸列表"
            mapping = [
                ('ID', {'title': 'id'}),
                ('楼层名称', {'title': 'name'}),
                ('图片地址', {'title': 'path'}),
                ('svg图片地址', {'title': 'quick_svg_path'}),
                ('图片类型名称', {'title': 'picture_type_name'}),
                ('小区名称', {'title': 'area_name'}),
                ('楼宇名称', {'title': 'build_name'})
            ]

            return await self.write_excel(file_name=file_name, datas=datas, mapping=mapping)

        return await self.write_json(CfResponse(data=records))


class DeviceAssignLogsList(BaseHandler):
    """布点记录"""

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            floor_id = get_field("floor_id", field_type=int)
            device_status = get_field("device_status", field_type=int)  # 设备状态 0 正常 其他为设备最新一条报警事件的国标设备类型id

            export_flag = get_field("export_flag", field_type=int)

            if device_status is not None and device_status not in [0, 1]:
                self.logger.error(f'device_status: {device_status}错误！只能为0或1')
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

            if export_flag is not None and export_flag != 1:
                self.logger.info(f'export_flag: {export_flag}错误！只能为1')
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            records = await async_load_assign_devices_by_params(redis=self.redis, page=page, per_page=per_page,
                                                                floor_id=floor_id, device_status=device_status)
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        records['items'] = [AttrDict(record) for record in records['items']]
        if records['items']:
            for record in records['items']:
                # 布点时间
                record['assign_time'] = record.create_time

                # 报警源
                if record.controller_num is None and record.loop_num is None and record.addr_num is None:
                    record['device_address'] = None
                else:
                    loop_num = record.loop_num if record.loop_num else '_'
                    addr_num = record.addr_num if record.addr_num else '_'
                    record['device_address'] = f"{record.controller_num}-{loop_num}-{addr_num}"

        attrs = {'id', 'assign_time', 'coordinate_X', 'coordinate_Y', 'rate', 'angle', 'device_type_id', 'device_id',
                 'device_type_name', 'path', 'description', 'device_status', 'psn', 'device_address', 'floor_id'}
        records['items'] = [{k: record[k] for k in attrs if k in record} for record in records.get('items')]

        if export_flag is not None:
            datas = records.get("items")
            file_name = f"布点记录列表"
            mapping = [
                ('ID', {'title': 'id'}),
                ('布点时间', {'title': 'assign_time'}),
                ('X轴坐标', {'title': 'coordinate_X'}),
                ('Y轴坐标', {'title': 'coordinate_Y'}),
                ('显示比例', {'title': 'rate'}),
                ('角度', {'title': 'angle'}),
                ('事件国标类型名称', {'title': 'device_type_name'}),
                ('图标地址', {'title': 'path'}),
                ('描述', {'title': 'description'}),
                ('psn', {'title': 'psn'}),
                ('设备地址', {'title': 'device_address'}),
            ]

            return await self.write_excel(file_name=file_name, datas=datas, mapping=mapping)

        return await self.write_json(CfResponse(data=records))


class ControllerOpLogsList(BaseHandler):
    """控制器操作记录"""

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            st = get_field("st")
            et = get_field("et")
            controller_id = get_field("controller_id", field_type=int)
            controller_num = get_field("controller_num", field_type=int)
            controller_name = get_field("controller_name")
            gb_evt_type_id = get_field("gb_evt_type_id", field_type=int)
            description = get_field("description")

            export_flag = get_field("export_flag", field_type=int)

            if export_flag is not None and export_flag != 1:
                self.logger.info(f'export_flag: {export_flag}错误！只能为1')
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            records = await async_load_controller_op_logs_by_params(redis=self.redis, page=page, per_page=per_page,
                                                                    st=st, et=et, controller_id=controller_id,
                                                                    controller_num=controller_num,
                                                                    controller_name=controller_name,
                                                                    gb_evt_type_id=gb_evt_type_id,
                                                                    description=description,
                                                                    origin='db')
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        if records['items']:
            for record in records['items']:
                # 布点时间
                record['op_time'] = record.create_time

        attrs = {'id', 'op_time', 'controller_id', 'controller_num', 'controller_name', 'gb_evt_type_id',
                 'gb_evt_type_name', 'description'}
        records['items'] = [{k: record[k] for k in attrs if k in record} for record in records.get('items')]

        if export_flag is not None:
            datas = records.get("items")
            file_name = f"控制器操作记录列表"
            mapping = [
                ('ID', {'title': 'id'}),
                ('操作时间', {'title': 'op_time'}),
                ('控制器号', {'title': 'controller_num'}),
                ('控制器名称', {'title': 'controller_name'}),
                ('操作描述', {'title': 'description'})
            ]

            return await self.write_excel(file_name=file_name, datas=datas, mapping=mapping)

        return await self.write_json(CfResponse(data=records))


class MaintenanceLogsList(BaseHandler):
    """维保记录"""

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            st = get_field("st")
            et = get_field("et")
            description = get_field("description")
            user_id = get_field("user_id", field_type=int)
            project_id = get_field("project_id", field_type=int)

            export_flag = get_field("export_flag", field_type=int)

            if export_flag is not None and export_flag != 1:
                self.logger.info(f'export_flag: {export_flag}错误！只能为1')
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            records = await async_load_maintenance_logs_by_params(redis=self.redis, page=page, per_page=per_page,
                                                                  st=st, et=et, description=description,
                                                                  user_id=user_id, project_id=project_id,
                                                                  origin='db')
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        if records['items']:
            for record in records['items']:
                # 布点时间
                record['maintenance_time'] = record.create_time

        attrs = {'id', 'maintenance_time', 'description', 'operator_name', 'project_id', 'user_id', 'user_name'}
        records['items'] = [{k: record[k] for k in attrs if k in record} for record in records.get('items')]

        if export_flag is not None:
            datas = records.get("items")
            file_name = f"维保记录列表"
            mapping = [
                ('ID', {'title': 'id'}),
                ('维保时间', {'title': 'maintenance_time'}),
                ('描述', {'title': 'description'}),
                ('维保名称', {'title': 'operator_name'}),
                ('项目id', {'title': 'project_id'}),
                ('维保人员id', {'title': 'user_id'}),
                ('维保人员名称', {'title': 'user_name'}),
            ]

            return await self.write_excel(file_name=file_name, datas=datas, mapping=mapping)

        return await self.write_json(CfResponse(data=records))


class ShiftRecordsList(BaseHandler):
    """换班记录"""

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            st = get_field("st")
            et = get_field("et")
            watch_user_id = get_field("watch_user_id", field_type=int)
            change_user_id = get_field("change_user_id", field_type=int)

            export_flag = get_field("export_flag", field_type=int)

            if export_flag is not None and export_flag != 1:
                self.logger.info(f'export_flag: {export_flag}错误！只能为1')
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            records = await async_load_shift_records_by_params(redis=self.redis, page=page, per_page=per_page,
                                                               st=st, et=et, watch_user_id=watch_user_id,
                                                               change_user_id=change_user_id,
                                                               origin='db')
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        if records['items']:
            for record in records['items']:
                # 换班时间
                record['shift_time'] = record.create_time

        attrs = {'id', 'shift_time', 'watch_user_id', 'watch_user_name', 'change_user_id', 'change_user_name'}
        records['items'] = [{k: record[k] for k in attrs if k in record} for record in records.get('items')]

        if export_flag is not None:
            datas = records.get("items")
            file_name = f"换班记录列表"
            mapping = [
                ('ID', {'title': 'id'}),
                ('维保时间', {'title': 'shift_time'}),
                ('值班用户名', {'title': 'watch_user_name'}),
                ('换班用户名', {'title': 'change_user_name'})
            ]

            return await self.write_excel(file_name=file_name, datas=datas, mapping=mapping)

        return await self.write_json(CfResponse(data=records))


class SystemLogsList(BaseHandler):
    """系统操作记录"""

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            st = get_field("st")
            et = get_field("et")
            description = get_field("description")
            user_id = get_field("user_id")

            export_flag = get_field("export_flag", field_type=int)

            if export_flag is not None and export_flag != 1:
                self.logger.info(f'export_flag: {export_flag}错误！只能为1')
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            records = await async_load_system_logs_by_params(redis=self.redis, page=page, per_page=per_page,
                                                             st=st, et=et, description=description,
                                                             user_id=user_id, origin='db')
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        if records['items']:
            for record in records['items']:
                # 操作时间
                record['op_time'] = record.create_time

        attrs = {'id', 'op_time', 'description', 'user_id', 'user_name'}
        records['items'] = [{k: record[k] for k in attrs if k in record} for record in records.get('items')]

        if export_flag is not None:
            datas = records.get("items")
            file_name = f"系统操作记录列表"
            mapping = [
                ('ID', {'title': 'id'}),
                ('操作时间', {'title': 'op_time'}),
                ('操作人名称', {'title': 'user_name'}),
                ('操作描述', {'title': 'description'})
            ]

            return await self.write_excel(file_name=file_name, datas=datas, mapping=mapping)

        return await self.write_json(CfResponse(data=records))


class Files(BaseHandler):

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            project_id = get_field("project_id", field_type=int)
            area_id = get_field("area_id", field_type=int)
            build_id = get_field("build_id", field_type=int)
            floor_id = get_field("floor_id", field_type=int)
            is_home = get_field("is_home", field_type=int)
            picture_type_id = get_field("picture_type_id", field_type=int)

            if not picture_type_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

            picture_type = await async_load_picture_type_by_id(picture_type_id, redis=self.redis)
            if not picture_type:
                msg = '图片类型id错误！'
                return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

            async with db.slice_session() as session:
                area_ids = []
                if project_id and picture_type.type in [2, 3]:
                    area_qry_func = select(TabArea).where(TabArea.is_delete == 0, TabArea.project_id == project_id)
                    areas = await session.execute(area_qry_func)
                    areas = areas.scalars().all()
                    area_ids = [area.id for area in areas]

                if picture_type.type in [2]:  # 查询楼宇列表
                    count_qry_func = select(func.count(TabBuild.id)).where(TabBuild.is_delete == 0)
                    qry_func = select(TabBuild).where(TabBuild.is_delete == 0)

                    if area_ids:
                        count_qry_func = count_qry_func.filter(TabBuild.area_id.in_(area_ids))
                        qry_func = qry_func.filter(TabBuild.area_id.in_(area_ids))

                    if area_id:
                        count_qry_func = count_qry_func.filter(TabBuild.area_id == area_id)
                        qry_func = qry_func.filter(TabBuild.area_id == area_id)

                    if build_id:
                        count_qry_func = count_qry_func.filter(TabBuild.id == build_id)
                        qry_func = qry_func.filter(TabBuild.id == build_id)

                    if page == 1:
                        # 计算分页信息
                        total = (await session.execute(count_qry_func)).scalar()
                        divisor, remainder = divmod(total, per_page)
                        result['record_size'] = total
                        result['page_size'] = divisor + 1 if remainder > 0 else divisor

                    if page > 0:
                        offset = (page - 1) * per_page
                        qry_func = qry_func.limit(per_page).offset(offset)
                    else:
                        total = (await session.execute(count_qry_func)).scalar()
                        if page == 0:
                            result['record_size'] = total

                    records = await session.execute(qry_func)
                    records = records.scalars().all()
                    records = [record.to_dict() for record in records]

                    for record in records:
                        result['items'].append(
                            {
                                "name": record.name,
                                "picture_type_id": picture_type_id,
                                "picture_type_name": picture_type.name,
                                "path": record.path
                            }
                        )

                elif picture_type.type in [3]:  # 查询楼层列表
                    count_qry_func = select(func.count(TabFloor.id)).where(TabFloor.is_delete == 0)
                    qry_func = select(TabFloor).where(TabFloor.is_delete == 0)

                    if area_ids:
                        count_qry_func = count_qry_func.filter(TabFloor.area_id.in_(area_ids))
                        qry_func = qry_func.filter(TabFloor.area_id.in_(area_ids))

                    if area_id:
                        count_qry_func = count_qry_func.filter(TabFloor.area_id == area_id)
                        qry_func = qry_func.filter(TabFloor.area_id == area_id)

                    if build_id:
                        count_qry_func = count_qry_func.filter(TabFloor.build_id == build_id)
                        qry_func = qry_func.filter(TabFloor.build_id == build_id)

                    if floor_id:
                        count_qry_func = count_qry_func.filter(TabFloor.id == floor_id)
                        qry_func = qry_func.filter(TabFloor.id == floor_id)

                    if page == 1:
                        # 计算分页信息
                        total = (await session.execute(count_qry_func)).scalar()
                        divisor, remainder = divmod(total, per_page)
                        result['record_size'] = total
                        result['page_size'] = divisor + 1 if remainder > 0 else divisor

                    if page > 0:
                        offset = (page - 1) * per_page
                        qry_func = qry_func.limit(per_page).offset(offset)
                    else:
                        total = (await session.execute(count_qry_func)).scalar()
                        if page == 0:
                            result['record_size'] = total

                    records = await session.execute(qry_func)
                    records = records.scalars().all()
                    records = [record.to_dict() for record in records]

                    for record in records:
                        result['items'].append(
                            {
                                "name": record.name,
                                "picture_type_id": picture_type_id,
                                "picture_type_name": picture_type.name,
                                "path": record.path
                            }
                        )

                else:  # 查询项目图片列表
                    count_qry_func = select(func.count(TabProjectPicture.id)).where(TabProjectPicture.is_delete == 0)
                    qry_func = select(TabProjectPicture).where(TabProjectPicture.is_delete == 0)

                    if project_id:
                        count_qry_func = count_qry_func.filter(TabProjectPicture.project_id == project_id)
                        qry_func = qry_func.filter(TabProjectPicture.project_id == project_id)

                    if picture_type_id:
                        count_qry_func = count_qry_func.filter(TabProjectPicture.picture_type_id == picture_type_id)
                        qry_func = qry_func.filter(TabProjectPicture.picture_type_id == picture_type_id)

                    if picture_type.type in [1, 4, 6] and is_home:
                        count_qry_func = count_qry_func.filter(TabProjectPicture.is_home == 1)
                        qry_func = qry_func.filter(TabProjectPicture.is_home == 1)

                    if page == 1:
                        # 计算分页信息
                        total = (await session.execute(count_qry_func)).scalar()
                        divisor, remainder = divmod(total, per_page)
                        result['record_size'] = total
                        result['page_size'] = divisor + 1 if remainder > 0 else divisor

                    if page > 0:
                        offset = (page - 1) * per_page
                        qry_func = qry_func.limit(per_page).offset(offset)
                    else:
                        total = (await session.execute(count_qry_func)).scalar()
                        if page == 0:
                            result['record_size'] = total

                    records = await session.execute(qry_func)
                    records = records.scalars().all()
                    records = [record.to_dict() for record in records]

                    for record in records:
                        result['items'].append(
                            {
                                "name": record.name,
                                "picture_type_id": picture_type_id,
                                "picture_type_name": record.picture_type_name,
                                "path": record.path
                            }
                        )
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse(data=result))
