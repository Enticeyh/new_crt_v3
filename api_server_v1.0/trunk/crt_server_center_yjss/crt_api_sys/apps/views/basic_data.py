from functools import partial
from sqlalchemy import select

from . import BaseHandler, CfResponse, ErrorCode, get_args, get_forms, db
from crt_api_sys.apps.util.db_module.models import TabIcon
from crt_api_sys.apps.util.async_db_api import async_load_roles, async_load_device_type, async_load_picture_type, \
    async_load_alarm_type, async_load_gb_evt_type, async_load_device_icon, async_load_device_type_by_id, \
    async_load_gb_evt_type_by_id


class Roles(BaseHandler):
    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            if per_page == 0:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            records = await async_load_roles(page=page, per_page=per_page, redis=self.redis)
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        attrs = {'id', 'name'}
        records['items'] = [{k: record[k] for k in attrs if k in record} for record in records.get('items')]

        return await self.write_json(CfResponse(data=records))


class DeviceType(BaseHandler):
    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            if per_page == 0:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            records = await async_load_device_type(page=page, per_page=per_page, redis=self.redis, origin='db')
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        attrs = {'id', 'gb_device_type', 'name', 'zx_device_type', 'priority'}
        records['items'] = [{k: record[k] for k in attrs if k in record} for record in records.get('items')]

        return await self.write_json(CfResponse(data=records))


class PictureType(BaseHandler):
    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            records = await async_load_picture_type(page=page, per_page=per_page, redis=self.redis)
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        attrs = {'id', 'name', 'type', 'file_type'}
        records['items'] = [{k: record[k] for k in attrs if k in record} for record in records.get('items')]

        return await self.write_json(CfResponse(data=records))


class AlarmType(BaseHandler):
    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            records = await async_load_alarm_type(page=page, per_page=per_page, redis=self.redis)
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        attrs = {'id', 'name'}
        records['items'] = [{k: record[k] for k in attrs if k in record} for record in records.get('items')]

        return await self.write_json(CfResponse(data=records))


class GbEvtType(BaseHandler):
    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            records = await async_load_gb_evt_type(page=page, per_page=per_page, redis=self.redis)
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        attrs = {'id', 'name', 'type_id', 'type_name', 'event_state'}
        records['items'] = [{k: record[k] for k in attrs if k in record} for record in records.get('items')]

        return await self.write_json(CfResponse(data=records))


class DeviceIcon(BaseHandler):
    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            records = await async_load_device_icon(page=page, per_page=per_page, redis=self.redis)
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        records['items'] = sorted(records.get('items'), key=lambda x: x.get('id'))

        attrs = {'id', 'name', 'path', 'device_type_id', 'device_type_name', 'gb_evt_type_id', 'gb_evt_type_name'}
        records['items'] = [{k: record[k] for k in attrs if k in record} for record in records.get('items')]

        return await self.write_json(CfResponse(data=records))

    async def post(self, request):
        get_field = partial(get_forms, request)

        try:
            icon = request.files.get("icon")
            device_type_id = get_field("device_type_id", field_type=int)
            gb_evt_type_id = get_field("gb_evt_type_id", field_type=int)

            if not all([icon, device_type_id]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            device_type = await async_load_device_type_by_id(device_type_id, redis=self.redis)
            if not device_type:
                msg = f"设备类型不存在！"
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

            gb_evt_type = None
            if gb_evt_type_id:
                gb_evt_type = await async_load_gb_evt_type_by_id(gb_evt_type_id, redis=self.redis)
                if not gb_evt_type:
                    msg = f"国标事件类型不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

            async with db.slice_session() as session:
                qry_func = select(TabIcon).where(TabIcon.is_delete == 0, TabIcon.device_type_id == device_type_id)
                icon_record = await session.execute(qry_func)
                icon_record = icon_record.scalars().all()
                if icon_record:
                    msg = f"该设备类型图标已存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

            path = f'/static/icon_image/{icon.name}'
            with open(f'{request.app.config.STATIC_ROOT_PATH}{path}', 'wb') as f:
                f.write(icon.body)

        except Exception as e:
            msg = f'保存图片出错！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, msg=msg, status=500))

        try:
            async with db.slice_session() as session:
                icon = {
                    "name": device_type.name,
                    "path": path,
                    "device_type_id": device_type_id,
                    "device_type_name": device_type.name,
                    "gb_evt_type_id": gb_evt_type_id,
                    "gb_evt_type_name": gb_evt_type.name if gb_evt_type else None,
                }
                session.add(TabIcon(**icon))
                await session.flush()

            # 删除缓存
            try:
                await self.redis.delete('tab_device_icon-records:')
            except Exception as e:
                msg = '删除缓存错误！'
                self.logger.info(msg)
                self.logger.exception(e)
                return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM))

        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def put(self, request):
        get_field = partial(get_forms, request)

        try:
            icon_id = get_field("icon_id", field_type=int)
            icon = request.files.get("icon")

            if not icon_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询图标是否存在
                qry_func = select(TabIcon).where(TabIcon.is_delete == 0, TabIcon.id == icon_id)
                icon_record = await session.execute(qry_func)
                icon_record = icon_record.scalars().first()

                if not icon_record:
                    msg = f"图标不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                if icon and icon.body:
                    try:
                        path = f'/static/icon_image/{icon.name}'
                        with open(f'{request.app.config.STATIC_ROOT_PATH}{path}', 'wb') as f:
                            f.write(icon.body)

                        icon_record.path = path
                    except Exception as e:
                        msg = f'保存图片出错！'
                        self.logger.error(msg)
                        self.logger.exception(e)
                        return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, msg=msg, status=500))

                if icon_record in session.dirty:
                    await session.flush()

                # 删除缓存
                try:
                    await self.redis.delete('tab_device_icon-records:')
                except Exception as e:
                    msg = '删除缓存错误！'
                    self.logger.info(msg)
                    self.logger.exception(e)
                    return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM))
        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def delete(self, request):
        get_field = partial(get_args, request)

        try:
            icon_id = get_field("icon_id", field_type=int)

            if not icon_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询图标是否存在
                qry_func = select(TabIcon).where(TabIcon.is_delete == 0, TabIcon.id == icon_id)
                icon = await session.execute(qry_func)
                icon = icon.scalars().first()

                if not icon:
                    msg = f"图标不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 删除图标
                icon.is_delete = 1

                if icon in session.dirty:
                    await session.flush()

                # 删除缓存
                try:
                    await self.redis.delete('tab_device_icon-records:')
                except Exception as e:
                    msg = '删除缓存错误！'
                    self.logger.info(msg)
                    self.logger.exception(e)
                    return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM))
        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())
