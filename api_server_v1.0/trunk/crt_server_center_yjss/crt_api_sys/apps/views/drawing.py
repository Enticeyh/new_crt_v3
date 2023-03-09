import io
import re
import uuid
import json
import copy
import shutil

from PIL import Image
from base64 import b64encode
from functools import partial
from attrdict import AttrDict
from sqlalchemy import select, func, text, update

from . import BaseHandler, CfResponse, get_args, get_jsons, get_forms, ErrorCode, db
from crt_api_sys.apps.util.async_func import read_excel, delete_cache
from crt_api_sys.apps.util.db_module.models import TabProject, TabProjectPicture, TabArea, TabBuild, TabFloor, \
    TabController, TabDevice, TabAssignDevice, TabAlarmLog, TabControllerOpLog
from crt_api_sys.apps.util.async_db_api import async_load_user_by_user_id, async_load_picture_type_by_id, \
    async_load_device_type, async_load_device_icon, async_load_device_type_by_id, async_load_device_icon_by_id
from crt_api_sys.apps.util.constant import CrtConstant


class ProjectsList(BaseHandler):
    """项目"""

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            name = get_field("name")
            address = get_field("address")
            mobile = get_field("mobile")

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

            async with db.slice_session() as session:
                count_qry_func = select(func.count(TabProject.id)).where(TabProject.is_delete == 0)
                qry_func = select(TabProject).where(TabProject.is_delete == 0)

                if name:
                    count_qry_func = count_qry_func.filter(TabProject.name.like(f'%{name}%'))
                    qry_func = qry_func.filter(TabProject.name.like(f'%{name}%'))

                if address:
                    count_qry_func = count_qry_func.filter(TabProject.address.like(f'%{address}%'))
                    qry_func = qry_func.filter(TabProject.address.like(f'%{address}%'))

                if mobile:
                    count_qry_func = count_qry_func.filter(TabProject.mobile.like(f'%{mobile}%'))
                    qry_func = qry_func.filter(TabProject.mobile.like(f'%{mobile}%'))

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
                result['items'] = [record.to_dict() for record in records]

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        if result['items']:
            for record in result['items']:
                record['deploy_users'] = json.loads(record.get('deploy_users'))

        attrs = {'id', 'name', 'address', 'mobile', 'deploy_users'}
        result['items'] = [{k: record[k] for k in attrs if k in record} for record in result.get('items')]

        return await self.write_json(CfResponse(data=result))

    async def post(self, request):
        get_field = partial(get_jsons, request)

        try:
            name = get_field("name")
            address = get_field("address")
            mobile = get_field("mobile")

            if not all([name, address]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

            user_id = request.ctx.user_id

            # if mobile:
            #     pattern = re.compile(r"1[356789]\d{9}")
            #     if not pattern.findall(mobile):
            #         msg = f'手机号码格式错误！'
            #         return await self.write_json(
            #             CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询项目名是否存在
                qry_func = select(TabProject).where(TabProject.is_delete == 0, TabProject.name == name)
                project = await session.execute(qry_func)
                project = project.scalars().first()
                if project:
                    msg = f"项目名称已存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                user = await async_load_user_by_user_id(user_id=user_id, redis=self.redis)
                project = {
                    "name": name,
                    "address": address,
                    "mobile": mobile,
                    "deploy_users": json.dumps([{"id": user_id, "name": user.user_name}])
                }
                session.add(TabProject(**project))
                await session.flush()

        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def put(self, request):
        get_field = partial(get_jsons, request)

        try:
            project_id = get_field("project_id", field_type=int)
            name = get_field("name")
            address = get_field("address")
            mobile = get_field("mobile")
            user_ids = get_field("user_ids")

            if not project_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

            if mobile:
                pattern = re.compile(r"1[356789]\d{9}")
                if not pattern.findall(mobile):
                    msg = f'手机号码格式错误！'
                    return await self.write_json(
                        CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))

            if user_ids:
                user_ids = [int(user_id) for user_id in user_ids.split(',')]

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询项目是否存在
                qry_func = select(TabProject).where(TabProject.is_delete == 0, TabProject.id == project_id)
                project = await session.execute(qry_func)
                project = project.scalars().first()

                if not project:
                    msg = f"项目不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                else:
                    if name:
                        project.name = name
                        # 修改小区中的项目名称
                        await session.execute(update(TabArea).where(TabArea.project_id == project_id).values(project_name=name))
                        # 修改控制器中的项目名称
                        await session.execute(update(TabController).where(TabController.project_id == project_id).values(project_name=name))
                    if address:
                        project.address = address
                    if mobile:
                        project.mobile = mobile
                    if user_ids:
                        new_deploy_users = []
                        old_deploy_users = json.loads(project.deploy_users)
                        old_deploy_users = {deploy_user.get('id'): deploy_user for deploy_user in old_deploy_users}
                        for user_id in user_ids:
                            if user_id in old_deploy_users:
                                new_deploy_users.append(old_deploy_users[user_id])
                            else:
                                user = await async_load_user_by_user_id(user_id=user_id, redis=self.redis)
                                new_deploy_users.append({"id": user_id, "name": user.user_name})

                        project.deploy_users = json.dumps(new_deploy_users)

                if project in session.dirty:
                    await session.flush()

        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def delete(self, request):
        get_field = partial(get_args, request)

        try:
            project_id = get_field("project_id", field_type=int)

            if not all([project_id]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询项目是否存在
                qry_func = select(TabProject).where(TabProject.is_delete == 0, TabProject.id == project_id)
                project = await session.execute(qry_func)
                project = project.scalars().first()

                if not project:
                    msg = f"项目不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 查询项目对应的小区
                qry_func = select(TabArea).where(TabArea.is_delete == 0, TabArea.project_id == project_id)
                areas = await session.execute(qry_func)
                areas = areas.scalars().all()
                if areas:
                    msg = f"请先手动删除该项目下所有小区信息后，再删除项目信息！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 查询项目对应的控制器
                qry_func = select(TabController).where(TabController.is_delete == 0, TabController.project_id == project_id)
                controllers = await session.execute(qry_func)
                controllers = controllers.scalars().all()
                if controllers:
                    msg = f"请先手动删除该项目下所有控制器后，再删除项目信息！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 删除项目
                project.is_delete = 1

                if project in session.dirty:
                    await session.flush()

        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())


class ProjectPictures(BaseHandler):
    """项目图片"""

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)
            project_id = get_field("project_id", field_type=int)
            picture_type_ids = get_field("picture_type_ids")

            if not picture_type_ids:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

            if picture_type_ids:
                picture_type_ids = picture_type_ids.split(',')
                picture_type_ids = [int(picture_type_id) for picture_type_id in picture_type_ids]

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

            async with db.slice_session() as session:
                count_qry_func = select(func.count(TabProjectPicture.id)).where(TabProjectPicture.is_delete == 0,
                                                                                TabProjectPicture.project_id == project_id)
                qry_func = select(TabProjectPicture).where(TabProjectPicture.is_delete == 0,
                                                           TabProjectPicture.project_id == project_id)

                if picture_type_ids:
                    count_qry_func = count_qry_func.filter(TabProjectPicture.picture_type_id.in_(picture_type_ids))
                    qry_func = qry_func.filter(TabProjectPicture.picture_type_id.in_(picture_type_ids))

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
                result['items'] = [record.to_dict() for record in records]

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        attrs = {'id', 'name', 'path', 'quick_svg_path', 'picture_type_id', 'picture_type_name', 'project_id', 'is_home'}
        result['items'] = [{k: record[k] for k in attrs if k in record} for record in result.get('items')]

        return await self.write_json(CfResponse(data=result))

    async def post(self, request):
        get_field = partial(get_forms, request)

        try:
            project_id = get_field("project_id", field_type=int)
            picture_type_id = get_field("picture_type_id", field_type=int)
            picture = request.files.get("picture")
            is_home = get_field("is_home", 0, field_type=int)

            if not all([project_id, picture_type_id, picture]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            name_uuid = str(uuid.uuid1()).replace('-', '')
            file_format = picture.name.split('.')[-1].lower()
            path = f'/static/photo/project_picture_{name_uuid}.{file_format}'
            with open(f'{request.app.config.STATIC_ROOT_PATH}{path}', 'wb') as f:
                f.write(picture.body)

            picture_type = await async_load_picture_type_by_id(picture_type_id, redis=self.redis)
            if not picture_type:
                msg = f"图片类型不存在！"
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))
        except Exception as e:
            msg = f'保存图片出错！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, msg=msg, status=500))

        try:
            async with db.slice_session() as session:
                project_picture = {
                    "name": f'{picture_type.name}',
                    "path": path,
                    "picture_type_id": picture_type_id,
                    "picture_type_name": picture_type.name,
                    "project_id": project_id,
                    "is_home": is_home,
                }
                _project_picture = TabProjectPicture(**project_picture)
                session.add(_project_picture)
                await session.flush()

                _project_picture.name = f'{_project_picture.name}{_project_picture.id}'

        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def delete(self, request):
        get_field = partial(get_args, request)

        try:
            project_picture_id = get_field("project_picture_id", field_type=int)

            if not project_picture_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询项目图片是否存在
                qry_func = select(TabProjectPicture).where(TabProjectPicture.is_delete == 0,
                                                           TabProjectPicture.id == project_picture_id)
                project_picture = await session.execute(qry_func)
                project_picture = project_picture.scalars().first()

                if not project_picture:
                    msg = f"项目图片不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 删除项目图片
                project_picture.is_delete = 1

                if project_picture in session.dirty:
                    await session.flush()

        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())


class Areas(BaseHandler):
    """小区"""

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            project_id = get_field("project_id", field_type=int)
            name = get_field("name")

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

            async with db.slice_session() as session:
                count_qry_func = select(func.count(TabArea.id)).where(TabArea.is_delete == 0)
                qry_func = select(TabArea).where(TabArea.is_delete == 0)

                if project_id:
                    count_qry_func = count_qry_func.filter(TabArea.project_id == project_id)
                    qry_func = qry_func.filter(TabArea.project_id == project_id)

                if name:
                    count_qry_func = count_qry_func.filter(TabArea.name.like(f'%{name}%'))
                    qry_func = qry_func.filter(TabArea.name.like(f'%{name}%'))

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
                result['items'] = [record.to_dict() for record in records]

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        attrs = {'id', 'name', 'project_id', 'project_name'}
        result['items'] = [{k: record[k] for k in attrs if k in record} for record in result.get('items')]

        return await self.write_json(CfResponse(data=result))

    async def post(self, request):
        get_field = partial(get_jsons, request)

        try:
            name = get_field("name")
            project_id = get_field("project_id", field_type=int)

            if not all([name, project_id]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询项目是否存在
                qry_func = select(TabProject).where(TabProject.is_delete == 0, TabProject.id == project_id)
                project = await session.execute(qry_func)
                project = project.scalars().first()
                if not project:
                    msg = f"项目不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                area = {
                    "name": name,
                    "project_id": project_id,
                    "project_name": project.name
                }
                session.add(TabArea(**area))
                await session.flush()

        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def put(self, request):
        get_field = partial(get_jsons, request)

        try:
            area_id = get_field("area_id", field_type=int)
            name = get_field("name")

            if not area_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询小区是否存在
                qry_func = select(TabArea).where(TabArea.is_delete == 0, TabArea.id == area_id)
                area = await session.execute(qry_func)
                area = area.scalars().first()

                if not area:
                    msg = f"小区不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                else:
                    if name:
                        # 修改小区名称
                        area.name = name
                        # 修改楼宇对应的小区名称
                        await session.execute(update(TabBuild).where(TabBuild.area_id == area_id).values(area_name=name))
                        # 修改楼层对应的小区名称
                        await session.execute(update(TabFloor).where(TabFloor.area_id == area_id).values(area_name=name))
                        # 修改报警记录中对应的小区名称
                        await session.execute(update(TabAlarmLog).where(TabAlarmLog.area_id == area_id).values(area_name=name))

                if area in session.dirty:
                    await session.flush()

        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def delete(self, request):
        get_field = partial(get_args, request)

        try:
            area_id = get_field("area_id", field_type=int)

            if not area_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询小区是否存在
                qry_func = select(TabArea).where(TabArea.is_delete == 0, TabArea.id == area_id)
                area = await session.execute(qry_func)
                area = area.scalars().first()

                if not area:
                    msg = f"小区不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 查询小区对应的楼宇
                qry_func = select(TabBuild).where(TabBuild.is_delete == 0, TabBuild.area_id == area_id)
                builds = await session.execute(qry_func)
                builds = builds.scalars().all()

                if builds:
                    msg = f"请先手动删除该小区下所有楼宇信息后，再删除小区信息！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 删除小区
                area.is_delete = 1

                if area in session.dirty:
                    await session.flush()

        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())


class Builds(BaseHandler):
    """楼宇"""

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            area_id = get_field("area_id", field_type=int)
            build_name = get_field("build_name")

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

            async with db.slice_session() as session:
                count_qry_func = select(func.count(TabBuild.id)).where(TabBuild.is_delete == 0)
                qry_func = select(TabBuild).where(TabBuild.is_delete == 0)

                if area_id:
                    count_qry_func = count_qry_func.filter(TabBuild.area_id == area_id)
                    qry_func = qry_func.filter(TabBuild.area_id == area_id)

                if build_name:
                    count_qry_func = count_qry_func.filter(TabBuild.name.like(f'%{build_name}%'))
                    qry_func = qry_func.filter(TabBuild.name.like(f'%{build_name}%'))

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
                result['items'] = [record.to_dict() for record in records]

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        attrs = {'id', 'name', 'path', 'picture_type_id', 'picture_type_name', 'area_id', 'area_name'}
        result['items'] = [{k: record[k] for k in attrs if k in record} for record in result.get('items')]

        return await self.write_json(CfResponse(data=result))

    async def post(self, request):
        get_field = partial(get_forms, request)

        try:
            name = get_field("name", '')
            start = get_field("start", field_type=int)
            end = get_field("end", field_type=int)
            picture = request.files.get("picture")
            picture_type_id = get_field("picture_type_id", 1, field_type=int)
            area_id = get_field("area_id", field_type=int)

            if not all([area_id]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

            if not name and not all([start, end]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

            if all([start, end]) and (start <= 0 or end <= 0):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

            if all([start, end]) and start > end:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

            names = []  # 存放楼宇名称
            if start or end:
                for i in range(start, end + 1):
                    names.append(f'{name}{i}栋')
            else:
                names.append(name)

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            picture_type = await async_load_picture_type_by_id(picture_type_id, redis=self.redis)
            if not picture_type:
                msg = f"图片类型不存在！"
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

            name_uuid = str(uuid.uuid1()).replace('-', '')

            if picture and picture.body:
                file_format = picture.name.split('.')[-1].lower()
                if file_format not in ["jpg", "jpeg", "png", "svg"]:
                    msg = f"楼宇图片仅支持jpg，jpeg，png，svg类型图片！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, msg=msg, status=400))

                path = f'/static/photo/build_{name_uuid}.{file_format}'
                with open(f'{request.app.config.STATIC_ROOT_PATH}{path}', 'wb') as f:
                    f.write(picture.body)
            else:
                file_format = request.app.config.BUILD_IMAGE_PATH.split('.')[-1].lower()
                def_build_path = f'{request.app.config.STATIC_ROOT_PATH}{request.app.config.BUILD_IMAGE_PATH}'
                path = f'/static/photo/build_{name_uuid}.{file_format}'
                shutil.copy(def_build_path, f'{request.app.config.STATIC_ROOT_PATH}{path}')

        except Exception as e:
            msg = f'保存图片出错！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, msg=msg, status=500))

        try:
            async with db.slice_session() as session:
                # 查询小区是否存在
                qry_func = select(TabArea).where(TabArea.is_delete == 0, TabArea.id == area_id)
                area = await session.execute(qry_func)
                area = area.scalars().first()
                if not area:
                    msg = f"小区不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                if names:
                    for name in names:
                        build = {
                            "name": name,
                            "path": path,
                            "picture_type_id": picture_type_id,
                            "picture_type_name": picture_type.name,
                            "area_id": area_id,
                            "area_name": area.name
                        }
                        session.add(TabBuild(**build))
                        await session.flush()

        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def put(self, request):
        get_field = partial(get_forms, request)

        try:
            build_id = get_field("build_id", field_type=int)
            name = get_field("name")
            picture = request.files.get("picture")
            picture_type_id = get_field("picture_type_id", 1, field_type=int)

            if not build_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        path, picture_type = None, None
        if picture:
            try:
                name_uuid = str(uuid.uuid1()).replace('-', '')
                file_format = picture.name.split('.')[-1].lower()
                path = f'/static/photo/build_{name_uuid}.{file_format}'
                with open(f'{request.app.config.STATIC_ROOT_PATH}{path}', 'wb') as f:
                    f.write(picture.body)

                picture_type = await async_load_picture_type_by_id(picture_type_id, redis=self.redis)
                if not picture_type:
                    msg = f"图片类型不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))
            except Exception as e:
                msg = f'保存图片出错！'
                self.logger.error(msg)
                self.logger.exception(e)
                return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, msg=msg, status=500))

        try:
            async with db.slice_session() as session:
                # 查询项目是否存在
                qry_func = select(TabBuild).where(TabBuild.is_delete == 0, TabBuild.id == build_id)
                build = await session.execute(qry_func)
                build = build.scalars().first()

                if not build:
                    msg = f"楼宇不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                else:
                    if name:
                        build.name = name
                        # 修改报警记录中对应的楼宇名称
                        await session.execute(update(TabAlarmLog).where(TabAlarmLog.build_id == build_id).values(build_name=name))
                        # 修改楼层中对应的楼宇名称
                        await session.execute(update(TabFloor).where(TabFloor.build_id == build_id).values(build_name=name))

                    if picture:
                        build.path = path
                        build.picture_type_id = picture_type_id
                        build.picture_type_name = picture_type.name

                if build in session.dirty:
                    await session.flush()

        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def delete(self, request):
        get_field = partial(get_args, request)

        try:
            build_id = get_field("build_id", field_type=int)

            if not build_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询楼宇是否存在
                qry_func = select(TabBuild).where(TabBuild.is_delete == 0, TabBuild.id == build_id)
                build = await session.execute(qry_func)
                build = build.scalars().first()

                if not build:
                    msg = f"楼宇不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 删除楼宇
                build.is_delete = 1

                qry_func = select(TabFloor).where(TabFloor.is_delete == 0, TabFloor.build_id == build_id)
                floors = await session.execute(qry_func)
                floors = floors.scalars().all()
                if floors:
                    floor_ids = [str(floor.id) for floor in floors]
                    # 删除楼宇对应的楼层 删除楼层对应的布点信息 清除设备对应的信息
                    await session.execute(update(TabFloor).where(TabFloor.build_id == build_id).values(is_delete=1))
                    await session.execute(update(TabAssignDevice).where(TabAssignDevice.floor_id.in_(floor_ids)).values(is_delete=1))
                    await session.execute(update(TabDevice).where(TabDevice.assign_floor_id.in_(floor_ids)).values(is_assign=0, assign_floor_id=None))

        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())


class Floors(BaseHandler):
    """楼层"""

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            area_id = get_field("area_id", field_type=int)
            build_id = get_field("build_id", field_type=int)
            floor_name = get_field("floor_name")
            inheritance_template = get_field("inheritance_template", field_type=int)

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

            async with db.slice_session() as session:
                count_qry_func = select(func.count(TabFloor.id)).where(TabFloor.is_delete == 0)
                qry_func = select(TabFloor).where(TabFloor.is_delete == 0)

                if area_id:
                    count_qry_func = count_qry_func.filter(TabFloor.area_id == area_id)
                    qry_func = qry_func.filter(TabFloor.area_id == area_id)

                if build_id:
                    count_qry_func = count_qry_func.filter(TabFloor.build_id == build_id)
                    qry_func = qry_func.filter(TabFloor.build_id == build_id)

                if floor_name:
                    count_qry_func = count_qry_func.filter(TabFloor.name.like(f'%{floor_name}%'))
                    qry_func = qry_func.filter(TabFloor.name.like(f'%{floor_name}%'))

                if inheritance_template is not None:
                    count_qry_func = count_qry_func.filter(TabFloor.inheritance_template == inheritance_template)
                    qry_func = qry_func.filter(TabFloor.inheritance_template == inheritance_template)

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
                result['items'] = [record.to_dict() for record in records]

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        if result['items']:
            for record in result['items']:
                record['is_alarm'] = 1 if record.alarm else 0

        attrs = {'id', 'name', 'path', 'quick_svg_path', 'picture_type_id', 'picture_type_name', 'area_id', 'area_name',
                 'build_id', 'build_name', 'is_alarm', 'inheritance_template', 'inheritance'}
        result['items'] = [{k: record[k] for k in attrs if k in record} for record in result.get('items')]

        return await self.write_json(CfResponse(data=result))

    async def post(self, request):
        get_field = partial(get_forms, request)

        try:
            name = get_field("name", '')
            start = get_field("start", field_type=int)
            end = get_field("end", field_type=int)
            picture = request.files.get("picture")
            picture_type_id = get_field("picture_type_id", 2, field_type=int)
            area_id = get_field("area_id", field_type=int)
            build_id = get_field("build_id", field_type=int)

            if not all([picture, picture_type_id, area_id, build_id]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

            if not start and not end and not name:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

            names = []  # 存放楼层名称
            if start is not None or end is not None:
                if start is None or end is None:
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

                for i in range(start, end + 1):
                    if i == 0:
                        continue
                    names.append(f'{name}{i}层')
            else:
                names.append(name)

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            name_uuid = str(uuid.uuid1()).replace('-', '')
            file_format = picture.name.split('.')[-1].lower()
            if file_format != "svg":
                msg = f"布点图类型必须为svg图片！"
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

            path = f'/static/photo/floor_{name_uuid}.{file_format}'
            with open(f'{request.app.config.STATIC_ROOT_PATH}{path}', 'wb') as f:
                f.write(picture.body)

            picture_type = await async_load_picture_type_by_id(picture_type_id, redis=self.redis)
            if not picture_type:
                msg = f"图片类型不存在！"
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))
        except Exception as e:
            msg = f'保存图片出错！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, msg=msg, status=500))

        try:
            async with db.slice_session() as session:
                # 查询小区是否存在
                qry_func = select(TabArea).where(TabArea.is_delete == 0, TabArea.id == area_id)
                area = await session.execute(qry_func)
                area = area.scalars().first()
                if not area:
                    msg = f"小区不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 查询楼宇是否存在
                qry_func = select(TabBuild).where(TabBuild.is_delete == 0, TabBuild.id == build_id)
                build = await session.execute(qry_func)
                build = build.scalars().first()
                if not build:
                    msg = f"楼宇不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                if names:
                    for name in names:
                        floor = {
                            "name": name,
                            "path": path,
                            "picture_type_id": picture_type_id,
                            "picture_type_name": picture_type.name,
                            "area_id": area_id,
                            "area_name": area.name,
                            "build_id": build_id,
                            "build_name": build.name,
                        }
                        session.add(TabFloor(**floor))
                        await session.flush()

        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def put(self, request):
        get_field = partial(get_forms, request)

        try:
            floor_id = get_field("floor_id", field_type=int)
            name = get_field("name")
            picture = request.files.get("picture")
            picture_type_id = get_field("picture_type_id", 2, field_type=int)
            quick_svg = request.files.get("quick_svg")

            if not floor_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        path, picture_type = None, None
        if picture:
            try:
                name_uuid = str(uuid.uuid1()).replace('-', '')
                file_format = picture.name.split('.')[-1].lower()
                path = f'/static/photo/floor_{name_uuid}.{file_format}'
                with open(f'{request.app.config.STATIC_ROOT_PATH}{path}', 'wb') as f:
                    f.write(picture.body)

                picture_type = await async_load_picture_type_by_id(picture_type_id, redis=self.redis)
                if not picture_type:
                    msg = f"图片类型不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))
            except Exception as e:
                msg = f'保存图片出错！'
                self.logger.error(msg)
                self.logger.exception(e)
                return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, msg=msg, status=500))

        quick_svg_path = None
        if quick_svg:
            try:
                name_uuid = str(uuid.uuid1()).replace('-', '')
                file_format = quick_svg.name.split('.')[-1].lower()
                quick_svg_path = f'/static/photo/quick_svg_{name_uuid}.{file_format}'
                with open(f'{request.app.config.STATIC_ROOT_PATH}{quick_svg_path}', 'wb') as f:
                    f.write(quick_svg.body)
            except Exception as e:
                msg = f'保存图片出错！'
                self.logger.error(msg)
                self.logger.exception(e)
                return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, msg=msg, status=500))

        try:
            async with db.slice_session() as session:
                # 查询楼层是否存在
                qry_func = select(TabFloor).where(TabFloor.is_delete == 0, TabFloor.id == floor_id)
                floor = await session.execute(qry_func)
                floor = floor.scalars().first()

                if not floor:
                    msg = f"楼层不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                else:
                    if name:
                        floor.name = name
                        # 修改报警记录中对应的楼层名称
                        await session.execute(update(TabAlarmLog).where(TabAlarmLog.floor_id == floor_id).values(floor_name=name))
                    if picture:
                        floor.path = path
                        floor.picture_type_id = picture_type_id
                        floor.picture_type_name = picture_type.name
                    if quick_svg:
                        floor.quick_svg_path = quick_svg_path

                if floor in session.dirty:
                    await session.flush()

        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def delete(self, request):
        get_field = partial(get_args, request)

        try:
            floor_ids = get_field("floor_ids")

            if not floor_ids:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

            floor_ids = floor_ids.split(',')
            floor_ids = [int(floor_id) for floor_id in floor_ids]
            floor_ids = list(set(floor_ids))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询楼层是否存在
                qry_func = select(TabFloor).where(TabFloor.is_delete == 0, TabFloor.id.in_(floor_ids))
                floors = await session.execute(qry_func)
                floors = floors.scalars().all()

                if not floors:
                    msg = f"楼层不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                for floor in floors:
                    # 删除楼层
                    floor.is_delete = 1

                    # 删除楼层对应的布点信息 清除设备对应的信息
                    await session.execute(update(TabAssignDevice).where(TabAssignDevice.floor_id == floor.id).values(is_delete=1))
                    await session.execute(update(TabDevice).where(TabDevice.assign_floor_id == floor.id).values(is_assign=0, assign_floor_id=None))

        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())


class Floor(BaseHandler):

    async def get(self, _, floor_id):

        try:
            record = await TabFloor.async_fetch_record_by_id(record_id=floor_id)

            if not record:
                msg = f'floor_id: {floor_id} 数据库无匹配记录！'
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_NO_RECORD, msg=msg, status=200))

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        record['is_alarm'] = 1 if record.alarm else 0

        attrs = {'id', 'name', 'path', 'quick_svg_path', 'picture_type_id', 'picture_type_name', 'area_id', 'area_name',
                 'build_id', 'build_name', 'is_alarm', 'inheritance_template', 'inheritance'}
        record = {k: record[k] for k in attrs if k in record}

        return await self.write_json(CfResponse(data=record))


class Controllers(BaseHandler):
    """控制器"""

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            project_id = get_field("project_id", field_type=int)

            name = get_field("name")
        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

            async with db.slice_session() as session:
                count_qry_func = select(func.count(TabController.id)).where(TabController.is_delete == 0)
                qry_func = select(TabController).where(TabController.is_delete == 0)

                if name:
                    count_qry_func = count_qry_func.where(TabController.name.like(f"%{name}%"))
                    qry_func = qry_func.where(TabController.name.like(f"%{name}%"))

                if project_id:
                    count_qry_func = count_qry_func.where(TabController.project_id == project_id)
                    qry_func = qry_func.where(TabController.project_id == project_id)

                qry_func = qry_func.order_by(TabController.code)

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
                result['items'] = [record.to_dict() for record in records]

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        attrs = {'id', 'name', 'code', 'model', 'manufacturer', 'setup_date', 'controller_type', 'host_id',
                 'is_online', 'power_type', 'project_id', 'project_name'}
        result['items'] = [{k: record[k] for k in attrs if k in record} for record in result.get('items')]

        return await self.write_json(CfResponse(data=result))

    async def post(self, request):
        get_field = partial(get_jsons, request)

        try:
            project_id = get_field("project_id", field_type=int)

            name = get_field("name")
            code = get_field("code", field_type=int)
            model = get_field("model")
            manufacturer = get_field("manufacturer")
            setup_date = get_field("setup_date")
            controller_type = get_field("controller_type", field_type=int)

            if not all([project_id, name, code, model, manufacturer, setup_date]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询项目信息
                project_qry_func = select(TabProject).where(TabProject.is_delete == 0, TabProject.id == project_id)
                project = await session.execute(project_qry_func)
                project = project.scalars().first()

                if not project:
                    msg = f'项目不存在，请检查提交数据是否正确！'
                    return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg))
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        try:
            async with db.slice_session() as session:
                # 查询控制器信息
                qry_func = select(TabController).where(TabController.is_delete == 0)
                controllers = await session.execute(qry_func)
                controllers = controllers.scalars().all()

                controllers_code = {controller.code: 1 for controller in controllers} if controllers else {}

                if controllers_code.get(code):
                    msg = f'控制器号已存在，请检查提交数据是否正确！'
                    return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg))

                controller = {
                    'project_id': project.id,
                    'project_name': project.name,
                    "name": name,
                    "code": code,
                    "model": model,
                    "manufacturer": manufacturer,
                    "setup_date": setup_date,
                }
                
                if controller_type:
                    controller['controller_type'] = controller_type

                session.add(TabController(**controller))
                await session.flush()

                # 删除缓存
                controller_name = f'tab_controller-record*'
                del_keys = await self.redis.keys(controller_name)
                if del_keys:
                    await self.redis.delete(*del_keys)
        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def put(self, request):
        get_field = partial(get_jsons, request)

        try:
            controller_id = get_field("controller_id", field_type=int)
            name = get_field("name")
            code = get_field("code", field_type=int)
            model = get_field("model")
            manufacturer = get_field("manufacturer")
            setup_date = get_field("setup_date")
            controller_type = get_field("controller_type", field_type=int)
            host_id = get_field("host_id")

            if not controller_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询控制器是否存在
                qry_func = select(TabController).where(TabController.is_delete == 0, TabController.id == controller_id)
                controller = await session.execute(qry_func)
                controller = controller.scalars().first()

                if not controller:
                    msg = f"控制器不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                if code:
                    code_qry_func = select(TabController).where(TabController.is_delete == 0, TabController.code == code)
                    new_code_controller = await session.execute(code_qry_func)
                    new_code_controller = new_code_controller.scalars().first()
                    if new_code_controller:
                        msg = f"控制器号 {code} 已存在，不能出现相同控制器号！"
                        return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                    controller_num = copy.copy(controller.code)
                    controller.code = code
                    await session.execute(update(TabAlarmLog).where(TabAlarmLog.controller_num == controller_num).values(controller_num=code))
                    await session.execute(update(TabAssignDevice).where(TabAssignDevice.controller_num == controller_num).values(controller_num=code))
                    await session.execute(update(TabControllerOpLog).where(TabControllerOpLog.controller_num == controller_num).values(controller_num=code))
                    await session.execute(update(TabDevice).where(TabDevice.controller_num == controller_num).values(controller_num=code))

                if name:
                    controller.name = name
                    await session.execute(update(TabControllerOpLog).where(TabControllerOpLog.controller_id == controller_id).values(controller_name=name))
                if model:
                    controller.model = model
                if manufacturer:
                    controller.manufacturer = manufacturer
                if setup_date:
                    controller.setup_date = setup_date
                if controller_type:
                    controller.controller_type = controller_type
                if host_id:
                    controller.host_id = host_id

                if controller in session.dirty:
                    await session.flush()

                # 删除缓存
                controller_name = f'tab_controller-record*'
                del_keys = await self.redis.keys(controller_name)
                if del_keys:
                    await self.redis.delete(*del_keys)
        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def delete(self, request):
        get_field = partial(get_args, request)

        try:
            controller_id = get_field("controller_id", field_type=int)

            if not controller_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询控制器是否存在
                qry_func = select(TabController).where(TabController.is_delete == 0, TabController.id == controller_id)
                controller = await session.execute(qry_func)
                controller = controller.scalars().first()
                if not controller:
                    msg = f"控制器不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))
                # 删除控制器
                controller.is_delete = 1

                # 更新设备
                await session.execute(update(TabDevice).where(TabDevice.controller_id == controller.id).values(is_delete=1))
                # 更新布点
                await session.execute(update(TabAssignDevice).where(TabAssignDevice.controller_num == controller.code).values(is_delete=1))

            # 删除缓存
            controller_name = f'tab_controller-record*'
            del_keys = await self.redis.keys(controller_name)
            if del_keys:
                await self.redis.delete(*del_keys)
        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())


class ControllersFile(BaseHandler):
    """控制器文件上传"""

    async def post(self, request):
        get_field = partial(get_forms, request)

        try:
            project_id = get_field("project_id", field_type=int)
            is_parse = get_field("is_parse", field_type=int)
            controller_excel = request.files.get("controller_excel")

            if not all([controller_excel]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

            if not project_id and not is_parse:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询项目信息
                project_qry_func = select(TabProject).where(TabProject.is_delete == 0, TabProject.id == project_id)
                project = await session.execute(project_qry_func)
                project = project.scalars().first()

                if not project:
                    msg = f'项目不存在，请检查提交数据是否正确！'
                    return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg))
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        try:
            name_uuid = str(uuid.uuid1()).replace('-', '')
            file_format = controller_excel.name.split('.')[-1].lower()
            if file_format not in ["xlsx", "xls", "csv"]:
                msg = f"文件类型错误，仅支持xlsx，xls，csv格式文件！"
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, msg=msg, status=400))

            path = f'{request.app.config.STATIC_ROOT_PATH}/static/other/controller_{name_uuid}.{file_format}'
            with open(f'{path}', 'wb+') as f:
                f.write(controller_excel.body)
        except Exception as e:
            msg = f'保存excel出错！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, msg=msg, status=500))

        try:
            table_data = read_excel(path)
        except Exception as e:
            msg = f'excel解析错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, msg=msg, status=500))

        if is_parse:
            # 只解析数据返回 不写入数据库
            data = []
            for raw_data in table_data:
                data.append(
                    {
                        "name": raw_data.get('name'),
                        "code": raw_data.get('number'),
                        "model": raw_data.get('model'),
                        "manufacturer": raw_data.get('manufacturer'),
                        "setup_date": raw_data.get('date')
                    }
                )
            return await self.write_json(CfResponse(data=data))

        try:
            if table_data:
                async with db.slice_session() as session:
                    # 查询控制器信息
                    qry_func = select(TabController).where(TabController.is_delete == 0)
                    controllers = await session.execute(qry_func)
                    controllers = controllers.scalars().all()

                    controllers_code = {controller.code: 1 for controller in controllers} if controllers else {}

                    repeat_psn = []  # 存放所有重复的psn
                    for raw_data in table_data:
                        if controllers_code.get(raw_data.get('number')):
                            repeat_psn.append(str(raw_data.get('number')))
                            continue

                        controller = {
                            'project_id': project.id,
                            'project_name': project.name,
                            "name": raw_data.get('name'),
                            "code": raw_data.get('number'),
                            "model": raw_data.get('model'),
                            "manufacturer": raw_data.get('manufacturer'),
                            "setup_date": raw_data.get('date'),
                        }

                        session.add(TabController(**controller))
                    await session.flush()

                    if repeat_psn:
                        repeat_psn = ','.join(repeat_psn)
                        msg = f"控制器编号 {repeat_psn} 已存在，请检查数据后重新上传！"
                        self.logger.info(msg)
                        return await self.write_json(CfResponse(data=msg))
        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())


class Devices(BaseHandler):
    """设备"""

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            controller_num = get_field("controller_num", field_type=int)
            loop_num = get_field("loop_num", field_type=int)
            addr_num = get_field("addr_num", field_type=int)
            area = get_field("area")
            build = get_field("build")
            unit = get_field("unit")
            floor = get_field("floor")
            district = get_field("district")
            room = get_field("room")
            is_assign = get_field("is_assign", field_type=int)
            is_online = get_field("is_online", field_type=int)  # 0 否 1 是
            device_state = get_field("device_state", field_type=int)
            description = get_field("description")

            if area and '--' in area:
                area = area.split('--')[0]
            if build and '--' in build:
                build = build.split('--')[0]
            if unit and '--' in unit:
                unit = unit.split('--')[0]
            if floor and '--' in floor:
                floor = floor.split('--')[0]
            if district and '--' in district:
                district = district.split('--')[0]
            if room and '--' in room:
                room = room.split('--')[0]

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

            async with db.slice_session() as session:
                count_qry_func = select(func.count(TabDevice.id)).where(TabDevice.is_delete == 0)
                qry_func = select(TabDevice).where(TabDevice.is_delete == 0)

                if controller_num is not None:
                    count_qry_func = count_qry_func.where(TabDevice.controller_num == controller_num)
                    qry_func = qry_func.where(TabDevice.controller_num == controller_num)

                if loop_num:
                    count_qry_func = count_qry_func.where(TabDevice.loop_num == loop_num)
                    qry_func = qry_func.where(TabDevice.loop_num == loop_num)

                if addr_num:
                    count_qry_func = count_qry_func.where(TabDevice.addr_num == addr_num)
                    qry_func = qry_func.where(TabDevice.addr_num == addr_num)

                if area:
                    count_qry_func = count_qry_func.where(TabDevice.area == area)
                    qry_func = qry_func.where(TabDevice.area == area)

                if build:
                    count_qry_func = count_qry_func.where(TabDevice.build == build)
                    qry_func = qry_func.where(TabDevice.build == build)

                if unit:
                    count_qry_func = count_qry_func.where(TabDevice.unit == unit)
                    qry_func = qry_func.where(TabDevice.unit == unit)

                if floor:
                    count_qry_func = count_qry_func.where(TabDevice.floor == floor)
                    qry_func = qry_func.where(TabDevice.floor == floor)

                if district:
                    count_qry_func = count_qry_func.where(TabDevice.district == district)
                    qry_func = qry_func.where(TabDevice.district == district)

                if room:
                    count_qry_func = count_qry_func.where(TabDevice.room == room)
                    qry_func = qry_func.where(TabDevice.room == room)

                if is_assign is not None:
                    count_qry_func = count_qry_func.where(TabDevice.is_assign == is_assign)
                    qry_func = qry_func.where(TabDevice.is_assign == is_assign)

                if is_online is not None:
                    count_qry_func = count_qry_func.where(TabDevice.is_online == is_online)
                    qry_func = qry_func.where(TabDevice.is_online == is_online)

                if device_state:
                    if device_state == 1:  # 火警
                        count_qry_func = count_qry_func.filter(TabDevice.fire > 0)
                        qry_func = qry_func.filter(TabDevice.fire > 0)
                    elif device_state == 2:  # 联动
                        count_qry_func = count_qry_func.filter(TabDevice.linkage > 0)
                        qry_func = qry_func.filter(TabDevice.linkage > 0)
                    elif device_state == 3:  # 反馈
                        count_qry_func = count_qry_func.filter(TabDevice.feedback > 0)
                        qry_func = qry_func.filter(TabDevice.feedback > 0)
                    elif device_state == 4:  # 故障
                        count_qry_func = count_qry_func.filter(TabDevice.malfunction > 0)
                        qry_func = qry_func.filter(TabDevice.malfunction > 0)
                    elif device_state == 5:  # 屏蔽
                        count_qry_func = count_qry_func.filter(TabDevice.shielding > 0)
                        qry_func = qry_func.filter(TabDevice.shielding > 0)
                    elif device_state == 6:  # 监管
                        count_qry_func = count_qry_func.filter(TabDevice.supervise > 0)
                        qry_func = qry_func.filter(TabDevice.supervise > 0)
                    elif device_state == 7:  # 声光故障
                        count_qry_func = count_qry_func.filter(TabDevice.vl_malfunction > 0)
                        qry_func = qry_func.filter(TabDevice.vl_malfunction > 0)
                    elif device_state == 8:  # 声光屏蔽
                        count_qry_func = count_qry_func.filter(TabDevice.vl_shielding > 0)
                        qry_func = qry_func.filter(TabDevice.vl_shielding > 0)

                if description:
                    count_qry_func = count_qry_func.filter(TabDevice.description.like(f'%{description}%'))
                    qry_func = qry_func.filter(TabDevice.description.like(f'%{description}%'))

                qry_func = qry_func.order_by(TabDevice.controller_num, TabDevice.loop_num, TabDevice.addr_num)

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
                result['items'] = [record.to_dict() for record in records]

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        for record in result['items']:
            record['current'] = f"{record.controller_num}-{record.loop_num}-{record.addr_num}"

            # 拼接设备状态
            dev_state = []
            if record.is_online:
                dev_state.append('在线')
            else:
                dev_state.append('离线')
            if record.fire:
                dev_state.append('报警')
            if record.malfunction:
                dev_state.append('故障')
            if record.vl_malfunction:
                dev_state.append('声光故障')
            if record.feedback:
                dev_state.append('反馈')
            if record.supervise:
                dev_state.append('监管')
            if record.shielding:
                dev_state.append('屏蔽')
            if record.vl_shielding:
                dev_state.append('声光屏蔽数量')
            if record.linkage:
                dev_state.append('启动')
            record['dev_state'] = '-'.join(dev_state)

        attrs = {'id', 'controller_id', 'controller_num', 'loop_num', 'addr_num', 'current', 'psn', 'manufacturer',
                 'device_model', 'setup_date', 'maintain_cycle', 'expiration_date', 'description', 'path',
                 'dev_state', 'is_online', 'is_assign', 'assign_floor_id', 'device_type_id',
                 'device_type_name', 'area', 'build', 'unit', 'floor', 'district', 'room'}
        result['items'] = [{k: record[k] for k in attrs if k in record} for record in result.get('items')]

        return await self.write_json(CfResponse(data=result))

    async def post(self, request):
        get_field = partial(get_jsons, request)

        try:
            controller_id = get_field("controller_id", field_type=int)
            controller_num = get_field("controller_num", field_type=int)

            loop_num = get_field("loop_num", field_type=int)
            addr_num = get_field("addr_num", field_type=int)
            device_type = get_field("device_type", field_type=int)
            psn = get_field("psn")
            equipment_num = get_field("equipment_num", field_type=int)
            module_num = get_field("module_num", field_type=int)
            manufacturer = get_field("manufacturer")
            date = get_field("date")
            device_model = get_field("device_model")
            maintain_cycle = get_field("maintain_cycle", field_type=int)
            expiration_date = get_field("expiration_date")
            description = get_field("description")

            if not all([controller_id, controller_num, loop_num, addr_num, device_type, psn, manufacturer,
                        device_model, maintain_cycle, expiration_date, description]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询设备信息
                qry_func = select(TabDevice).where(TabDevice.is_delete == 0, TabDevice.controller_num == controller_num, TabDevice.loop_num == loop_num, TabDevice.addr_num == addr_num)
                device = await session.execute(qry_func)
                device = device.scalars().first()

                if device:
                    msg = f'{controller_num}-{loop_num}-{addr_num} 设备已存在!'
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, msg=msg))

                # 查询设备类型
                device_types = await async_load_device_type(page=0, redis=self.redis, fast_to_dict=True)
                # 查询设备图标
                device_icons = await async_load_device_icon(page=0, redis=self.redis, fast_to_dict=True)

                # 若psn存在且长度>=4且合法，则设备类型取psn中获取的内部编码，否则用国标码进行转化
                if psn and len(psn) >= 4 and device_icons.get(int(psn[:4], 16)):
                    device_type_id = int(psn[:4], 16)
                else:
                    device_type_id = int(CrtConstant.DEVICE_TYPE_DICT.get(device_type, ['0', ''])[0])

                device_type = device_types.get(device_type_id)
                device_icon = device_icons.get(device_type_id)

                # 解析描述 拆分出地址信息
                address = None
                if '_' in description and len(description.split('-')) == 7:
                    address = description.split('-')
                    area = address[0] if address[0] != '_' else None
                    build = address[1] if address[1] != '_' else None
                    unit = address[2] if address[2] != '_' else None
                    floor = address[3] if address[3] != '_' else None
                    district = address[4] if address[4] != '_' else None

                device = {
                    "controller_id": controller_id,
                    "controller_num": controller_num,
                    "loop_num": loop_num,
                    "addr_num": addr_num,
                    "equipment_num": equipment_num,
                    "module_num": module_num,
                    "psn": psn,
                    "manufacturer": manufacturer,
                    "device_model": device_type.get('name'),
                    "maintain_cycle": maintain_cycle,
                    "expiration_date": expiration_date or None,
                    "description": description,
                    "path": device_icon.get('path'),
                    "device_type_id": device_type_id,
                    "device_type_name": device_type.get('name')
                }

                if date:
                    device["setup_date"] = date

                address_info = {}
                if address:
                    address_info = {
                        'area': area,
                        'build': build,
                        'unit': unit,
                        'floor': floor,
                        'district': district
                    }

                session.add(TabDevice(**device, **address_info))
                await session.flush()
        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def put(self, request):
        get_field = partial(get_jsons, request)

        try:
            device_id = get_field("device_id", field_type=int)
            device_type_id = get_field("device_type_id", field_type=int)
            psn = get_field("psn")
            description = get_field("description")

            if not device_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

            if description and "-" not in description and len(description.split('-')) != 7:
                msg = "描述格式不符合规范！"
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询设备是否存在
                qry_func = select(TabDevice).where(TabDevice.is_delete == 0, TabDevice.id == device_id)
                device = await session.execute(qry_func)
                device = device.scalars().first()

                if not device:
                    msg = f"设备不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 如果设备已布点，查出布点信息
                if device.is_assign:
                    assign_qry_func = select(TabAssignDevice).where(TabAssignDevice.is_delete == 0,
                                                                    TabAssignDevice.device_id == device_id)
                    assign_device = await session.execute(assign_qry_func)
                    assign_device = assign_device.scalars().first()
                    if not assign_device:
                        msg = f"device_id： {device_id} 设备布点信息和布点状态不匹配！"
                        return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                if device_type_id:
                    # 更新设备类型 设备类型id 设备类型名称 设备型号都要更新
                    device_type = await async_load_device_type_by_id(device_type_id, redis=self.redis)
                    if not device_type:
                        msg = f"设备类型不存在！"
                        return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                    device_icon = await async_load_device_icon_by_id(device_type_id, redis=self.redis)
                    if not device_icon:
                        msg = f"设备图标不存在！"
                        return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                    device.device_model = device_type.get('name')
                    device.device_type_id = device_type_id
                    device.device_type_name = device_type.get('name')
                    device.path = device_icon.get('path')
                    if device.is_assign:
                        assign_device.device_type_id = device_type_id
                        assign_device.device_type_name = device_type.get('name')
                        assign_device.path = device_icon.get('path')
                if psn:
                    # 查询设备是否存在
                    psn_qry_func = select(TabDevice).where(TabDevice.is_delete == 0, TabDevice.psn == psn)
                    psn_device = await session.execute(psn_qry_func)
                    psn_device = psn_device.scalars().first()
                    if psn_device:
                        msg = f"设备psn已存在！"
                        return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))
                    device.psn = psn
                    if device.is_assign:
                        assign_device.psn = psn

                if description:
                    # 更新设备描述
                    device.description = description

                    # 如果未布点 设备的地址信息也需要跟随更新 已布点就不能随意更改地址信息
                    # 单个分区情况
                    if not device.is_assign and '_' in description and len(description.split('-')) == 7:
                        # 解析描述 拆分出地址信息
                        address = description.split('-')
                        area = address[0] if address[0] != '_' else "小区"
                        build = address[1] if address[1] != '_' else "楼宇"
                        unit = address[2] if address[2] != '_' else "单元"
                        floor = address[3] if address[3] != '_' else "楼层"
                        district = address[4] if address[4] != '_' else "防火分区"

                        # 如果有对应的楼层 更新信息
                        if address:
                            device.area = area
                            device.build = build
                            device.unit = unit
                            device.floor = floor
                            device.district = district

                    # 双层分区情况
                    elif not device.is_assign and '_' in description and len(description.split('-')) == 8:
                        # 解析描述 拆分出地址信息
                        address = description.split('-')
                        area = address[0] if address[0] != '_' else "小区"
                        build = address[1] if address[1] != '_' else "楼宇"
                        unit = address[2] if address[2] != '_' else "单元"
                        floor = address[3] if address[3] != '_' else "楼层"
                        district = address[4] if address[4] != '_' else "防火分区"
                        room = address[5] if address[5] != '_' else "防烟分区"

                        # 如果有对应的楼层 更新信息
                        if address:
                            device.area = area
                            device.build = build
                            device.unit = unit
                            device.floor = floor
                            device.district = district
                            device.room = room

                    elif not device.is_assign:
                        # 没有布点且描述规则不符合要求 全部置为None
                        device.area = None
                        device.build = None
                        device.unit = None
                        device.floor = None
                        device.district = None

                    # 如果布点 仅更新布点描述信息
                    else:
                        assign_device.description = description

                if device in session.dirty:
                    await session.flush()

        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def delete(self, request):
        get_field = partial(get_jsons, request)

        try:
            device_ids = get_field("device_ids")

            start_controller_num = get_field("start_controller_num", field_type=int)
            start_loop_num = get_field("start_loop_num", field_type=int)
            start_addr_num = get_field("start_addr_num", field_type=int)
            end_controller_num = get_field("end_controller_num", field_type=int)
            end_loop_num = get_field("end_loop_num", field_type=int)
            end_addr_num = get_field("end_addr_num", field_type=int)

            if not device_ids and not all([start_controller_num, start_loop_num, start_addr_num, end_controller_num, end_loop_num, end_addr_num]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

            if device_ids:
                device_ids = device_ids.split(',')
                device_ids = [int(device_id) for device_id in device_ids]
                device_ids = list(set(device_ids))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            assign_device_ids = []
            # 查出所有需要删除的设备id和布点id
            async with db.slice_session() as session:
                if not device_ids:
                    device_ids = []
                    # 根据控制器，回路号，地址号获取所有设备
                    for controller_num in range(start_controller_num, end_controller_num + 1):
                        for loop_num in range(start_loop_num, end_loop_num + 1):
                            qry_func = select(TabDevice).where(TabDevice.is_delete == 0)
                            qry_func = qry_func.where(TabDevice.controller_num == controller_num)
                            qry_func = qry_func.where(TabDevice.loop_num == loop_num)
                            if controller_num == start_controller_num and loop_num == start_loop_num:
                                qry_func = qry_func.where(TabDevice.addr_num >= start_addr_num)
                            if controller_num == end_controller_num and loop_num == end_loop_num:
                                qry_func = qry_func.where(TabDevice.addr_num <= end_addr_num)
                            records = await session.execute(qry_func)
                            records = records.scalars().all()
                            device_ids += [record.id for record in records]
                            assign_device_ids += [record.id for record in records if record.is_assign]
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        try:
            # 删除所有需要删除的设备和布点
            async with db.slice_session() as session:
                if device_ids:
                    await session.execute(update(TabDevice).where(TabDevice.id.in_(device_ids)).values(is_delete=1))

                if assign_device_ids:
                    await session.execute(update(TabAssignDevice).where(TabAssignDevice.device_id.in_(assign_device_ids)).values(is_delete=1))
                else:
                    await session.execute(update(TabAssignDevice).where(TabAssignDevice.device_id.in_(device_ids)).values(is_delete=1))
        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())


class DevicesFile(BaseHandler):
    """设备文件上传"""

    async def post(self, request):
        get_field = partial(get_forms, request)

        try:
            controller_id = get_field("controller_id", field_type=int)
            controller_num = get_field("controller_num", field_type=int)
            device_excel = request.files.get("device_excel")

            if not all([controller_id, controller_num, device_excel]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            name_uuid = str(uuid.uuid1()).replace('-', '')
            file_format = device_excel.name.split('.')[-1].lower()
            if file_format not in ["xlsx", "xls", "csv"]:
                msg = f"文件类型错误，仅支持xlsx，xls，csv格式文件！"
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, msg=msg, status=400))

            path = f'{request.app.config.STATIC_ROOT_PATH}/static/other/device_{name_uuid}.{file_format}'
            with open(f'{path}', 'wb+') as f:
                f.write(device_excel.body)
        except Exception as e:
            msg = f'保存excel出错！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, msg=msg, status=500))

        try:
            table_data = read_excel(path)
        except Exception as e:
            msg = f'excel解析错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, msg=msg, status=500))

        try:
            if table_data:
                async with db.slice_session() as session:
                    # 查询设备信息
                    qry_func = select(TabDevice).where(TabDevice.is_delete == 0, TabDevice.controller_num == controller_num)
                    devices = await session.execute(qry_func)
                    devices = devices.scalars().all()

                    devices_current = {f'{device.controller_num}-{device.loop_num}-{device.addr_num}': 1 for device in
                                       devices} if devices else {}

                    # 查询设备类型
                    device_types = await async_load_device_type(page=0, redis=self.redis, fast_to_dict=True)
                    # 查询设备图标
                    device_icons = await async_load_device_icon(page=0, redis=self.redis, fast_to_dict=True)

                    for raw_data in table_data:
                        if devices_current.get(f"{controller_num}-{raw_data.get('loop')}-{raw_data.get('position')}"):
                            continue

                        # 若psn存在且长度>=4且合法，则设备类型取psn中获取的内部编码，否则用国标码进行转化
                        if raw_data.get('psn') and len(raw_data.get('psn')) >= 4 and device_icons.get(
                                int(raw_data.get('psn')[:4], 16)):
                            device_type_id = int(raw_data.get('psn')[:4], 16)
                        else:
                            device_type_id = int(raw_data.get('type'))

                        device_type = device_types.get(device_type_id, {})
                        device_icon = device_icons.get(device_type_id, {})

                        # 解析描述 拆分出地址信息
                        address = None
                        area, build, unit, floor, district, room = None, None, None, None, None, None
                        # 单个分区情况
                        if '_' in raw_data.get('description') and len(raw_data.get('description').split('-')) == 7:
                            address = raw_data.get('description').split('-')
                            area = address[0] if address[0] != '_' else "小区"
                            build = address[1] if address[1] != '_' else "楼宇"
                            unit = address[2] if address[2] != '_' else "单元"
                            floor = address[3] if address[3] != '_' else "楼层"
                            district = address[4] if address[4] != '_' else "防火分区"

                        # 双层分区情况
                        elif '_' in raw_data.get('description') and len(raw_data.get('description').split('-')) == 8:
                            address = raw_data.get('description').split('-')
                            area = address[0] if address[0] != '_' else "小区"
                            build = address[1] if address[1] != '_' else "楼宇"
                            unit = address[2] if address[2] != '_' else "单元"
                            floor = address[3] if address[3] != '_' else "楼层"
                            district = address[4] if address[4] != '_' else "防火分区"
                            room = address[5] if address[5] != '_' else "防烟分区"

                        device = {
                            "controller_id": controller_id,
                            "controller_num": controller_num,
                            "loop_num": raw_data.get('loop'),
                            "addr_num": raw_data.get('position'),
                            "psn": raw_data.get('psn'),
                            "manufacturer": raw_data.get('manufacturer'),
                            "device_model": device_type.get('name'),
                            "maintain_cycle": raw_data.get('maintain_cycle') or None,
                            "expiration_date": raw_data.get('expiration_date') or None,
                            "description": raw_data.get('description'),
                            "path": device_icon.get('path'),
                            "device_type_id": device_type_id,
                            "device_type_name": device_type.get('name')
                        }

                        if raw_data.get('date'):
                            device["setup_date"] = raw_data.get('date')

                        address_info = {}
                        if address:
                            address_info = {
                                'area': area,
                                'build': build,
                                'unit': unit,
                                'floor': floor,
                                'district': district,
                                'room': room
                            }

                        session.add(TabDevice(**device, **address_info))
                    await session.flush()
        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())


class AddressRelationship(BaseHandler):

    async def get(self, request):

        get_field = partial(get_args, request)

        try:
            project_id = get_field("project_id", field_type=int)

            if not project_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                controller_qry_func = select(TabController).where(TabController.is_delete == 0, TabController.project_id == project_id)
                controllers = await session.execute(controller_qry_func)
                controllers = controllers.scalars().all()

                controller_ids = [controller.id for controller in controllers]

                addresses_qry_func = select(text("area"), text("build"), text("unit"), text("floor"), text("district"), text("room"))
                addresses_qry_func = addresses_qry_func.where(TabDevice.is_delete == 0, TabDevice.controller_id.in_(controller_ids), TabDevice.area != None, TabDevice.build != None, TabDevice.floor != None)
                addresses_qry_func = addresses_qry_func.group_by(TabDevice.area, TabDevice.build, TabDevice.unit, TabDevice.floor, TabDevice.district, TabDevice.room)
                addresses = await session.execute(addresses_qry_func)
                addresses = addresses.all()

                num_qry_func = select(text("area"), text("build"), text("unit"), text("floor"), text("district"), text("room"), func.count(id))
                num_qry_func = num_qry_func.where(TabDevice.is_delete == 0, TabDevice.controller_id.in_(controller_ids), TabDevice.is_assign == 0, TabDevice.area != None, TabDevice.build != None, TabDevice.floor != None)
                num_qry_func = num_qry_func.group_by(TabDevice.area, TabDevice.build, TabDevice.unit, TabDevice.floor, TabDevice.district, TabDevice.room)
                nums = await session.execute(num_qry_func)
                nums = nums.all()

                nums = {(area, build, unit, floor, district, room): num for area, build, unit, floor, district, room, num in nums}
                addresses = [(area, build, unit, floor, district, room, nums.get((area, build, unit, floor, district, room), 0)) for area, build, unit, floor, district, room in addresses]

                address_relationship = {}
                for address in addresses:
                    area, build, unit, floor, district, room, num = address
                    if not address_relationship.get(area):
                        address_relationship[area] = {}
                    if not address_relationship[area].get(build):
                        address_relationship[area][build] = {}
                    if not address_relationship[area][build].get(unit):
                        address_relationship[area][build][unit] = {}
                    if not address_relationship[area][build][unit].get(floor):
                        address_relationship[area][build][unit][floor] = {}
                    if not address_relationship[area][build][unit][floor].get(district):
                        address_relationship[area][build][unit][floor][district] = {}
                    address_relationship[area][build][unit][floor][district][room] = num

                data = []
                for area_name, area_info in address_relationship.items():
                    area = {
                            "label": area_name,
                            "level": "area",
                            "children": [],
                        }
                    area_num = 0
                    for build_name, build_info in area_info.items():
                        build = {
                            "label": build_name,
                            "level": "build",
                            "children": [],
                        }
                        build_num = 0
                        for unit_name, unit_info in build_info.items():
                            if unit:
                                unit = {
                                    "label": unit_name,
                                    "level": "unit",
                                    "children": [],
                                }
                                unit_num = 0
                                for floor_name, floor_info in unit_info.items():
                                    floor = {
                                        "label": floor_name,
                                        "level": "floor",
                                        "children": [],
                                    }
                                    floor_num = 0

                                    for district_name, room_info in floor_info.items():
                                        district = {
                                            "label": district_name,
                                            "level": "district",
                                            "children": [],
                                        }
                                        district_num = 0

                                        for room_name, num in room_info.items():
                                            if room_name:
                                                district["children"].append(
                                                    {
                                                        "label": f'{room_name}--{num}',
                                                        "level": "room",
                                                    }
                                                )
                                            district_num += num
                                        district["label"] = f"{district['label']}--{district_num}"

                                        if not district["children"]:
                                            del district["children"]

                                        floor_num += district_num
                                        floor["children"].append(district)

                                    if not floor["children"]:
                                        del floor["children"]

                                    floor["label"] = f"{floor['label']}--{floor_num}"
                                    unit["children"].append(floor)

                                    unit_num += floor_num

                                unit["label"] = f"{unit['label']}--{unit_num}"
                                build["children"].append(unit)

                                build_num += unit_num

                            else:
                                for floor_name, floor_info in unit_info.items():
                                    floor = {
                                        "label": floor_name,
                                        "level": "floor",
                                        "children": [],
                                    }
                                    floor_num = 0

                                    for district_name, room_info in floor_info.items():
                                        district = {
                                            "label": district_name,
                                            "level": "district",
                                            "children": [],
                                        }
                                        district_num = 0

                                        for room_name, num in room_info.items():
                                            if room_name:
                                                district["children"].append(
                                                    {
                                                        "label": f'{room_name}--{num}',
                                                        "level": "room",
                                                    }
                                                )
                                            district_num += num
                                        district["label"] = f"{district['label']}--{district_num}"
                                        if not district["children"]:
                                            del district["children"]

                                        floor_num += district_num
                                        floor["children"].append(district)

                                    if not floor["children"]:
                                        del floor["children"]

                                    build["children"].append(floor)

                                    build_num += floor_num

                        build["label"] = f"{build['label']}--{build_num}"
                        area["children"].append(build)

                        area_num += build_num

                    area["label"] = f"{area['label']}--{area_num}"
                    data.append(area)

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse(data=data))


class CurrentRelationship(BaseHandler):

    async def get(self, request):

        get_field = partial(get_args, request)

        try:
            project_id = get_field("project_id", field_type=int)

            if not project_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                controller_qry_func = select(TabController).where(TabController.is_delete == 0)
                controller_qry_func = controller_qry_func.where(TabController.project_id == project_id)
                controllers = await session.execute(controller_qry_func)
                controllers = controllers.scalars().all()

                controller_ids = [controller.id for controller in controllers]

                loops_qry_func = select(text("controller_num"), text("loop_num")).where(TabDevice.is_delete == 0)
                loops_qry_func = loops_qry_func.where(TabDevice.controller_id.in_(controller_ids))
                loops_qry_func = loops_qry_func.group_by(TabDevice.controller_num, TabDevice.loop_num)
                loops = await session.execute(loops_qry_func)
                loops = loops.all()

                num_qry_func = select(text("controller_num"), text("loop_num"), func.count(id)).where(TabDevice.is_delete == 0)
                num_qry_func = num_qry_func.where(TabDevice.controller_id.in_(controller_ids), TabDevice.is_assign == 0)
                num_qry_func = num_qry_func.group_by(TabDevice.controller_num, TabDevice.loop_num)
                nums = await session.execute(num_qry_func)
                nums = nums.all()

                nums = {(controller_num, loop_num): num or 0 for controller_num, loop_num, num in nums}
                loops = [(controller_num, loop_num, nums.get((controller_num, loop_num), 0)) for controller_num, loop_num in loops]

                controller_loop = {}
                controllers_num = {}
                for controller_num, loop_num, num in loops:
                    if controller_num not in controller_loop:
                        controller_loop[controller_num] = {}
                        controllers_num[controller_num] = 0
                    controllers_num[controller_num] += num
                    controller_loop[controller_num][loop_num] = num

                data = []
                for controller in controllers:
                    controller_info = {"label": f'{controller.name}--{controllers_num.get(controller.code, 0)}', "id": controller.code, "children": []}
                    if controller_loop.get(controller.code):
                        for loop_num, num in controller_loop.get(controller.code).items():
                            controller_info["children"].append(
                                {
                                    "label": f'回路{loop_num}--{num or 0}',
                                    "id": loop_num
                                }
                            )

                    data.append(controller_info)

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse(data=data))


class AssignDevice(BaseHandler):
    """布点"""

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            floor_id = get_field("floor_id", field_type=int)

            if not floor_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                qry_func = select(TabAssignDevice).where(TabAssignDevice.is_delete == 0)
                qry_func = qry_func.where(TabAssignDevice.floor_id == floor_id)
                assign_devices = await session.execute(qry_func)
                assign_devices = assign_devices.scalars().all()

                assign_devices = [assign_device.to_dict() for assign_device in assign_devices]
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        for assign_device in assign_devices:
            controller_num = assign_device.get('controller_num')
            loop_num = assign_device.get('loop_num')
            addr_num = assign_device.get('addr_num')
            assign_device['device_address'] = f"{controller_num}-{loop_num}-{addr_num}"

        attrs = {'id', 'coordinate_X', 'coordinate_Y', 'rate', 'angle', 'width', 'height', 'device_type_id',
                 'device_type_name', 'path', 'description', 'device_status', 'device_id', 'psn',
                 'device_address', 'floor_id'}
        data = [{k: assign_device[k] for k in attrs if k in assign_device} for assign_device in assign_devices]

        return await self.write_json(CfResponse(data=data))

    async def post(self, request):
        get_field = partial(get_jsons, request)

        try:
            assign_info = get_field("assign_info")
            floor_id = get_field("floor_id", field_type=int)
            inheritance_template = get_field("inheritance_template", field_type=int)

            if not assign_info:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

            if inheritance_template is not None and inheritance_template not in [0, 1]:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 检查楼层是否存在
                qry_func = select(TabFloor).where(TabFloor.is_delete == 0, TabFloor.id == floor_id)
                floor = await session.execute(qry_func)
                floor = floor.scalars().first()
                if not floor:
                    msg = f'floor_id: {floor_id} 楼层不存在！'
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, msg=msg))

                if inheritance_template is not None:
                    floor.inheritance_template = inheritance_template

                qry_func = select(TabAssignDevice).where(TabAssignDevice.is_delete == 0)
                qry_func = qry_func.where(TabAssignDevice.floor_id == floor_id)
                assign_devices = await session.execute(qry_func)
                assign_devices = assign_devices.scalars().all()

                assign_devices = {assign_device.device_id: assign_device for assign_device in assign_devices}

                for assign in assign_info:
                    if assign.get('device_id') in assign_devices:
                        # 修改
                        assign_device = assign_devices.get(assign.get('device_id'))
                        assign_device.coordinate_X = assign.get('coordinate_X')
                        assign_device.coordinate_Y = assign.get('coordinate_Y')
                        assign_device.rate = assign.get('rate')
                        assign_device.angle = assign.get('angle')
                        assign_device.width = assign.get('width')
                        assign_device.height = assign.get('height')
                    else:
                        # 新增
                        device_qry_func = select(TabDevice).where(TabDevice.is_delete == 0, TabDevice.is_assign == 0)
                        device_qry_func = device_qry_func.where(TabDevice.id == assign.get('device_id'))
                        device = await session.execute(device_qry_func)
                        device = device.scalars().first()
                        if not device:
                            self.logger.info(f"device_id: {assign.get('device_id')} 无此设备或设备已部署到其他图纸！")
                            continue
                        device.is_assign = 1
                        device.assign_floor_id = floor_id

                        assign_device = {
                            "coordinate_X": assign.get('coordinate_X'),
                            "coordinate_Y": assign.get('coordinate_Y'),
                            "rate": assign.get('rate'),
                            "angle": assign.get('angle'),
                            "width": assign.get('width'),
                            "height": assign.get('height'),
                            "device_type_id": device.device_type_id,
                            "device_type_name": device.device_type_name,
                            "path": device.path,
                            "description": device.description,
                            "device_status": 1 if device.alarm else 0,
                            "device_id": assign.get('device_id'),
                            "psn": device.psn,
                            "controller_num": device.controller_num,
                            "loop_num": device.loop_num,
                            "addr_num": device.addr_num,
                            "equipment_num": device.equipment_num,
                            "module_num": device.module_num,
                            "floor_id": floor_id,
                        }
                        session.add(TabAssignDevice(**assign_device))

                    await session.flush()

                # 清除缓存
                await delete_cache(self.redis, "tab_device")
                await delete_cache(self.redis, "tab_assign_device")

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def delete(self, request):
        get_field = partial(get_args, request)

        try:
            assign_id = get_field("assign_id", field_type=int)
            device_id = get_field("device_id", field_type=int)

            if not assign_id and not device_id:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                if not assign_id:
                    # 查询布点id
                    qry_func = select(TabAssignDevice).where(TabAssignDevice.is_delete == 0, TabAssignDevice.device_id == device_id)
                    assign_device = await session.execute(qry_func)
                    assign_device = assign_device.scalars().first()
                    if not assign_device:
                        msg = f"此设备不存在或此设备未布点！"
                        return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))
                else:
                    # 查询布点是否存在
                    qry_func = select(TabAssignDevice).where(TabAssignDevice.is_delete == 0, TabAssignDevice.id == assign_id)
                    assign_device = await session.execute(qry_func)
                    assign_device = assign_device.scalars().first()

                    if not assign_device:
                        msg = f"布点不存在！"
                        return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 查询设备是否存在
                device_qry_func = select(TabDevice).where(TabDevice.is_delete == 0, TabDevice.id == assign_device.device_id)
                device = await session.execute(device_qry_func)
                device = device.scalars().first()

                if not device:
                    msg = f"设备不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 修改设备布点信息
                device.is_assign = 0
                device.assign_floor_id = None

                # 删除布点
                assign_device.is_delete = 1

                await session.flush()

        except Exception as e:
            msg = f'数据库操作错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())


class AssignInheritance(BaseHandler):

    async def post(self, request):
        get_field = partial(get_jsons, request)

        try:
            father_floor_id = get_field("father_floor_id", field_type=int)
            son_floor_id = get_field("son_floor_id", field_type=int)

            start_controller_num = get_field("start_controller_num", field_type=int)
            start_loop_num = get_field("start_loop_num", field_type=int)
            start_addr_num = get_field("start_addr_num", field_type=int)
            end_controller_num = get_field("end_controller_num", field_type=int)
            end_loop_num = get_field("end_loop_num", field_type=int)
            end_addr_num = get_field("end_addr_num", field_type=int)
        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            devices_by_id = {}
            async with db.slice_session() as session:
                # 检查子布点图是否已布点 如果已布点就不能进行继承操作
                qry_func = select(TabAssignDevice).where(TabAssignDevice.is_delete == 0)
                qry_func = qry_func.where(TabAssignDevice.floor_id == son_floor_id)
                assign_devices = await session.execute(qry_func)
                assign_devices = assign_devices.scalars().all()
                if assign_devices:
                    msg = "子布点图已布点，如需进行布点操作，请删除子布点图的所有布点信息！"
                    return await self.write_json(
                        CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 获取输入的所有设备
                for controller_num in range(start_controller_num, end_controller_num + 1):
                    for loop_num in range(start_loop_num, end_loop_num + 1):
                        qry_func = select(TabDevice).where(TabDevice.is_delete == 0, TabDevice.is_assign == 0)
                        qry_func = qry_func.where(TabDevice.controller_num == controller_num)
                        qry_func = qry_func.where(TabDevice.loop_num == loop_num)
                        if controller_num == start_controller_num and loop_num == start_loop_num:
                            qry_func = qry_func.where(TabDevice.addr_num >= start_addr_num)
                        if controller_num == end_controller_num and loop_num == end_loop_num:
                            qry_func = qry_func.where(TabDevice.addr_num <= end_addr_num)

                        records = await session.execute(qry_func)
                        records = records.scalars().all()
                        devices_by_id.update({record.id: record for record in records})

                # 获取所有输入设备
                devices = [device.to_dict() for device in devices_by_id.values()]

                # 获取父级布点点位数据
                qry_func = select(TabAssignDevice).where(TabAssignDevice.is_delete == 0)
                qry_func = qry_func.where(TabAssignDevice.floor_id == father_floor_id)
                assign_devices = await session.execute(qry_func)
                assign_devices = assign_devices.scalars().all()
                assign_devices = [assign_device.to_dict() for assign_device in assign_devices]

                if len(devices) > len(assign_devices):
                    msg = "输入的设备数量不能超过父级图纸的点位数量！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 生成新的布点信息
                data = []
                for i in range(len(devices)):
                    assign_device = assign_devices[i]
                    device = devices[i]
                    assign_device['device_type_id'] = device.device_type_id
                    assign_device['device_type_name'] = device.device_type_name
                    assign_device['path'] = device.path
                    assign_device['device_status'] = 1 if device.alarm else 0
                    assign_device['description'] = device.description
                    assign_device['device_id'] = device.id
                    assign_device['psn'] = device.psn
                    assign_device['controller_num'] = device.controller_num
                    assign_device['loop_num'] = device.loop_num
                    assign_device['addr_num'] = device.addr_num
                    assign_device['equipment_num'] = device.equipment_num
                    assign_device['module_num'] = device.module_num
                    assign_device['floor_id'] = son_floor_id
                    data.append(assign_device)

                attrs = {'coordinate_X', 'coordinate_Y', 'rate', 'angle', 'width', 'height', 'device_type_id',
                         'device_type_name', 'path', 'description', 'device_status', 'device_id', 'psn',
                         'controller_num', 'loop_num', 'addr_num', 'equipment_num', 'module_num', 'floor_id'}
                data = [{k: assign_device[k] for k in attrs if k in assign_device} for assign_device in data]

                # 获取父级布点图信息
                qry_func = select(TabFloor).where(TabFloor.is_delete == 0, TabFloor.id == son_floor_id)
                son_floor = await session.execute(qry_func)
                son_floor = son_floor.scalars().first()
                son_floor.inheritance = father_floor_id

                _assign_device = None
                for assign in data:
                    assign_device = {
                        "coordinate_X": assign.get('coordinate_X'),
                        "coordinate_Y": assign.get('coordinate_Y'),
                        "rate": assign.get('rate'),
                        "angle": assign.get('angle'),
                        "width": assign.get('width'),
                        "height": assign.get('height'),
                        "device_type_id": assign.get('device_type_id'),
                        "device_type_name": assign.get('device_type_name'),
                        "path": assign.get('path'),
                        "description": assign.get('description'),
                        "device_status": assign.get('device_status'),
                        "device_id": assign.get('device_id'),
                        "psn": assign.get('psn'),
                        "controller_num": assign.get('controller_num'),
                        "loop_num": assign.get('loop_num'),
                        "addr_num": assign.get('addr_num'),
                        "equipment_num": assign.get('equipment_num'),
                        "module_num": assign.get('module_num'),
                        "floor_id": assign.get('floor_id'),
                    }
                    _assign_device = TabAssignDevice(**assign_device)
                    session.add(_assign_device)

                    device = devices_by_id.get(assign.get('device_id'))
                    device.is_assign = 1
                    device.assign_floor_id = assign.get('floor_id')
                    await session.flush()

                    assign['id'] = _assign_device.id

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        for assign_device in data:
            controller_num = assign_device.get('controller_num')
            loop_num = assign_device.get('loop_num')
            addr_num = assign_device.get('addr_num')
            assign_device['device_address'] = f"{controller_num}-{loop_num}-{addr_num}"

        attrs = {'id', 'coordinate_X', 'coordinate_Y', 'rate', 'angle', 'width', 'height', 'device_type_id',
                 'device_type_name', 'path', 'description', 'device_status', 'device_id', 'psn',
                 'device_address', 'floor_id'}
        data = [{k: assign_device[k] for k in attrs if k in assign_device} for assign_device in data]

        return await self.write_json(CfResponse(data=data))


class QuickSvg(BaseHandler):
    async def post(self, request):
        get_field = partial(get_jsons, request)

        try:
            floor_id = get_field("floor_id", field_type=int)
        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 检查子布点图是否已布点 如果已布点就不能进行继承操作
                qry_func = select(TabFloor).where(TabFloor.is_delete == 0, TabFloor.id == floor_id)
                floor = await session.execute(qry_func)
                floor = floor.scalars().first()
                if not floor:
                    msg = "布点图不存在！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                qry_func = select(TabAssignDevice).where(TabAssignDevice.is_delete == 0)
                qry_func = qry_func.where(TabAssignDevice.floor_id == floor_id)
                assign_devices = await session.execute(qry_func)
                assign_devices = assign_devices.scalars().all()
                if not assign_devices:
                    msg = "此布点图无布点信息，请先进行布点！"
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 获取静态文件地址
                static_root_path = request.app.config.STATIC_ROOT_PATH
                # 获取布点图地址
                floor_path = floor.path

                # 如果快速svg已存在，删除快速svg
                if floor.quick_svg_path:
                    pass

                quick_svg_path = f'{floor_path[:-4]}_quick_svg.svg'

                # 读取布点图数据
                try:
                    with open(file=f'{static_root_path}{floor_path}', mode='r') as f:
                        lines = f.readlines()

                    if not lines:
                        msg = "布点图无信息，请联系管理员检查布点图！"
                        return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                    lines.pop()
                except Exception as e:
                    msg = f'读取布点图信息错误！'
                    self.logger.error(msg)
                    self.logger.exception(e)
                    return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

                for assign_device in assign_devices:
                    img = Image.open(f'{static_root_path}{assign_device.path}')
                    # width = img.width
                    # height = img.height
                    # 旋转图片
                    if assign_device.angle:
                        img = img.rotate(assign_device.angle)
                    # 缩放图片
                    # if assign_device.rate:
                    #     width *= assign_device.rate
                    #     height *= assign_device.rate

                    # 创建data_uri
                    img_byte_arr = io.BytesIO()  # 用于存放图标图片的临时byte数据流
                    img.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()  # 获取图标图片的byte数据流
                    encoded_data = b64encode(img_byte_arr).decode("utf-8").strip()  # 将图片转为base64

                    # 拼接图片信息
                    href = f'data:image/png;base64,{encoded_data}'
                    info = f'<image width="{assign_device.width}" height="{assign_device.height}" x="{assign_device.coordinate_X}" y="{assign_device.coordinate_Y}" href="{href}"></image>\n'
                    lines.append(info)

                lines.append("</svg>")

                # 写入新的信息
                with open(file=f'{static_root_path}{quick_svg_path}', mode='w') as f:
                    f.write(''.join(lines))

                # 报错快速svg文件路径
                floor.quick_svg_path = quick_svg_path

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())


class Loops(BaseHandler):

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            controller_num = get_field("controller_num", field_type=int)

            if controller_num is None:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                qry_func = select(text("loop_num")).where(TabDevice.is_delete == 0)
                qry_func = qry_func.where(TabDevice.controller_num == controller_num)
                qry_func = qry_func.group_by(TabDevice.loop_num)
                loops = await session.execute(qry_func)
                loops = loops.scalars().all()

                data = {
                    'loops': loops
                }

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse(data=data))
