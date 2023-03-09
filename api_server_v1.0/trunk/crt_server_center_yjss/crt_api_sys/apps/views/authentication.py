import os
import json
import platform

from attrdict import AttrDict
from functools import partial
from sqlalchemy import select
from datetime import timedelta, datetime

from . import BaseHandler, CfResponse, get_args, get_jsons, ErrorCode, redis_factory, db
from ..util.authentication import create_access_token
from ..util.async_func import md5_encryption, hash_func_params
from ..util.db_module.models import TabUser, TabSystemLog, TabShiftRecord, TabRole
from ..util.async_db_api import async_load_users, async_load_user_by_user_name, async_load_user_by_user_id, \
    async_load_role_by_role_id


class Login(BaseHandler):
    async def post(self, request):
        get_field = partial(get_jsons, request)

        try:
            user_name = get_field("user_name")
            password = get_field("password")

            if not all([user_name, password]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            if user_name == request.app.config.SUPER_USERNAME:
                # 校验超管密码 超级管理员密码规则为superpassword_<year>-<month>（如superpassword_2022-8） md5加密后 取第6位到第11位（共6位）
                now = datetime.now()
                super_password = md5_encryption(f'{request.app.config.SUPER_PASSWORD}_{now.year}-{now.month}')
                if md5_encryption(super_password[5:11]) != password:
                    msg = f'超级管理员密码错误！'
                    self.logger.info(msg)
                    return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_ACCOUNT, msg=msg, status=403))

                user = AttrDict({'id': 0, 'user_name': user_name, 'role_id': 0, 'role_name': '超级管理员'})

            else:
                # 校验账号和密码
                user = await async_load_user_by_user_name(user_name=user_name, redis=self.redis)
                # 无此用户
                if not user:
                    msg = f'登录账号不存在！'
                    self.logger.info(msg)
                    return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_ACCOUNT, msg=msg, status=403))

                # 校验密码
                secret = request.app.config.SECRET  # 加密秘钥
                password = md5_encryption(password, secret)

                # 密码错误
                if password != user.password:
                    msg = f'登录密码错误！'
                    self.logger.info(msg)
                    return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_ACCOUNT, msg=msg, status=403))

        except Exception as e:
            msg = f'校验账号密码错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        # 创建token
        token_data = {"user_id": user.id}  # token data
        expires_delta = timedelta(minutes=request.app.config.REDIS_TOKEN_EXPIRE)  # 过期时间
        token = create_access_token(data=token_data, expires_delta=expires_delta, secret=request.app.config.SECRET)

        k = f'login:{user.id}'
        await redis_factory.set_string_cache(k, token, ex=request.app.config.REDIS_TOKEN_EXPIRE, redis=self.redis)

        data = {
            "id": user.id,
            "user_name": user_name,
            "role_id": user.role_id,
            "role_name": user.role_name,
            "token": token
        }

        # 创建登录记录
        try:
            async with db.slice_session() as session:
                system_log = {
                    "description": "登录",
                    "user_id": user.id,
                    "user_name": user.user_name
                }
                session.add(TabSystemLog(**system_log))
                await session.flush()

            # 删除缓存
            system_log_name = f'tab_system_log-records:*'
            system_log_keys = await self.redis.keys(system_log_name)
            if system_log_keys:
                # 清除全部缓存键
                await self.redis.delete(*system_log_keys)
        except Exception as e:
            msg = f'新增登录记录错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse(data=data))


class Logout(BaseHandler):
    async def post(self, request):
        get_field = partial(get_jsons, request)

        try:
            password = get_field("password")

            # 校验密码
            now = datetime.now()
            super_password = md5_encryption(f'{request.app.config.SUPER_PASSWORD}_{now.year}-{now.month}')
            if md5_encryption(super_password[5:11]) != password:
                msg = f'超级管理员密码错误！'
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_ACCOUNT, msg=msg, status=403))

            login_user_id = request.ctx.user_id

            # 清除值班账号的登录信息
            k = f'login:{login_user_id}'
            await redis_factory.del_key(k, redis=self.redis)

            # 创建退出记录
            user = await async_load_user_by_user_id(user_id=login_user_id, redis=self.redis)
            async with db.slice_session() as session:
                system_log = {
                    "description": "关机",
                    "user_id": user.id,
                    "user_name": user.user_name
                }
                session.add(TabSystemLog(**system_log))
                await session.flush()

                # 删除缓存
                system_log_name = f'tab_system_log-records:*'
                system_log_keys = await self.redis.keys(system_log_name)
                if system_log_keys:
                    # 清除全部缓存键
                    await self.redis.delete(*system_log_keys)
        except Exception as e:
            msg = f'新增退出记录错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        if platform.system() == 'Linux' and request.ip in ['127.0.0.1', 'localhost']:
            os.system('shutdown -h now')
        return await self.write_json(CfResponse())


class ShiftDuty(BaseHandler):
    async def post(self, request):
        get_field = partial(get_jsons, request)

        try:
            user_name = get_field("user_name")
            password = get_field("password")

            if not all([user_name, password]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK))
        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            old_duty = await async_load_user_by_user_id(user_id=request.ctx.user_id, redis=self.redis)  # 值班用户信息

            if user_name == old_duty.user_name:
                msg = f'换班账号和值班账号相同！'
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_ACCOUNT, msg=msg, status=403))

            # 校验换班用户密码
            if user_name == request.app.config.SUPER_USERNAME:
                # 校验超管密码 超级管理员密码规则为superpassword_<year>-<month>（如superpassword_2022-8） md5加密后 取第6位到第11位（共6位）
                now = datetime.now()
                super_password = md5_encryption(f'{request.app.config.SUPER_PASSWORD}_{now.year}-{now.month}')
                if md5_encryption(super_password[5:11]) != password:
                    msg = f'超级管理员密码错误！'
                    self.logger.info(msg)
                    return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_ACCOUNT, msg=msg, status=403))

                new_duty = AttrDict({'id': 0, 'user_name': user_name, 'role_id': 0, 'role_name': '超级管理员'})

            else:
                # 校验账号和密码
                new_duty = await async_load_user_by_user_name(user_name=user_name, redis=self.redis)
                # 无此用户
                if not new_duty:
                    msg = f'换班账号不存在！'
                    self.logger.info(msg)
                    return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_ACCOUNT, msg=msg, status=403))

                # 校验密码
                secret = request.app.config.SECRET  # 加密秘钥
                password = md5_encryption(password, secret)

                # 密码错误
                if password != new_duty.password:
                    msg = f'换班用户密码错误！'
                    self.logger.info(msg)
                    return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_ACCOUNT, msg=msg, status=403))

            # 清除值班账号的登录信息
            k = f'login:{old_duty.id}'
            await redis_factory.del_key(k, redis=self.redis)

            # 创建换班账号token
            secret = request.app.config.SECRET  # 加密秘钥
            token_data = {"user_id": new_duty.id}  # token data
            expires_delta = timedelta(minutes=request.app.config.REDIS_TOKEN_EXPIRE)  # 过期时间
            token = create_access_token(data=token_data, expires_delta=expires_delta, secret=secret)

            k = f'login:{new_duty.id}'
            await redis_factory.set_string_cache(k, token, ex=request.app.config.REDIS_TOKEN_EXPIRE, redis=self.redis)

        except Exception as e:
            msg = f'换班错误！'
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg, status=500))

        # 创建换班记录
        try:
            async with db.slice_session() as session:
                shift_record = {
                    "watch_user_id": old_duty.id,
                    "watch_user_name": old_duty.user_name,
                    "change_user_id": new_duty.id,
                    "change_user_name": new_duty.user_name
                }
                session.add(TabShiftRecord(**shift_record))
                await session.flush()
        except Exception as e:
            msg = f'新增换班记录错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        data = {
            "id": new_duty.id,
            "user_name": new_duty.user_name,
            "role_id": new_duty.role_id,
            "role_name": new_duty.role_name,
            "token": token
        }

        return await self.write_json(CfResponse(data=data))


class User(BaseHandler):

    async def get(self, request):
        get_field = partial(get_args, request)

        try:
            page = get_field("page", 1, field_type=int)
            per_page = get_field("per_page", 10, field_type=int)

            if per_page == 0:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=400))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            records = await async_load_users(page=page, per_page=per_page, redis=self.redis)
        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        attrs = {'id', 'user_name', 'role_id', 'role_name'}
        records['items'] = [{k: record[k] for k in attrs if k in record} for record in records.get('items')]

        return await self.write_json(CfResponse(data=records))


class UpdateUser(BaseHandler):

    async def post(self, request):
        get_field = partial(get_jsons, request)

        try:
            user_name = get_field("user_name")
            password = get_field("password")
            role_id = get_field("role_id", field_type=int)

            if not all([user_name, password, role_id]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK))

            # 校验密码格式
            if len(password) != 32:
                msg = '新增用户，密码格式错误！'
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询当前登陆用户权限
                logger = await async_load_user_by_user_id(user_id=request.ctx.user_id, redis=self.redis)
                temporary_permissions = await self.redis.get(f'temporary_permissions:{logger.id}')
                if logger.role_id not in [0, 1, 2] and not temporary_permissions:
                    msg = '当前登陆用户无此权限！'
                    self.logger.info(msg)
                    return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg))

                # 查询用户名是否存在
                check_user = await async_load_user_by_user_name(user_name=user_name, redis=self.redis)

                if check_user:
                    msg = '用户名已存在，请更换用户名！'
                    self.logger.info(msg)
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 查询角色
                role = await async_load_role_by_role_id(role_id=role_id, redis=self.redis)

                if not role:
                    msg = '角色不存在，请检查角色！'
                    self.logger.info(msg)
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 新增用户
                secret = request.app.config.SECRET  # 加密秘钥
                password = md5_encryption(password, secret)  # md5加密
                new_user = {
                    "user_name": user_name,
                    "password": password,
                    "role_id": role.id,
                    "role_name": role.name
                }
                session.add(TabUser(**new_user))
                await session.flush()

            try:
                # 删除缓存
                await self.redis.delete('tab_user-records:')
            except Exception as e:
                msg = '删除缓存错误！'
                self.logger.info(msg)
                self.logger.exception(e)
                return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM))

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        try:
            # 新增系统日志
            system_log = {
                "description": f"新增用户 {user_name}",
                "user_id": logger.id,
                "user_name": logger.user_name
            }
            session.add(TabSystemLog(**system_log))
            await session.flush()

            # 删除缓存
            system_log_name = f'tab_system_log-records:*'
            system_log_keys = await self.redis.keys(system_log_name)
            if system_log_keys:
                # 清除全部缓存键
                await self.redis.delete(*system_log_keys)
        except Exception as e:
            msg = f'新增用户写入系统日志记录错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def put(self, request):
        get_field = partial(get_jsons, request)

        try:
            user_id = get_field("user_id", field_type=int)
            password = get_field("password")
            role_id = get_field("role_id", field_type=int)

            if not all([user_id]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK))

            # 校验密码格式
            if password and len(password) != 32:
                msg = '修改用户，密码格式错误！'
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询当前登陆用户权限
                logger = await async_load_user_by_user_id(user_id=request.ctx.user_id, redis=self.redis)
                temporary_permissions = await self.redis.get(f'temporary_permissions:{logger.id}')
                if logger.role_id not in [0, 1, 2] and not temporary_permissions:
                    msg = '当前登陆用户无此权限！'
                    self.logger.info(msg)
                    return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_RESOURCE, msg=msg))

                # 查询用户是否存在
                update_user_qry_func = select(TabUser).where(TabUser.is_delete == 0, TabUser.id == user_id)
                update_user = await session.execute(update_user_qry_func)
                update_user = update_user.scalars().first()

                if not update_user:
                    msg = '用户不存在！'
                    self.logger.info(msg)
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 查询角色
                if role_id:
                    role_qry_func = select(TabRole).where(TabRole.is_delete == 0, TabRole.id == role_id)
                    role = await session.execute(role_qry_func)
                    role = role.scalars().first()

                    if not role:
                        msg = '角色不存在，请检查角色！'
                        self.logger.info(msg)
                        return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                    update_user.role_id = role.id
                    update_user.role_name = role.name

                # 修改用户
                if password:
                    secret = request.app.config.SECRET  # 加密秘钥
                    password = md5_encryption(password, secret)  # md5加密

                    if password == update_user.password:
                        msg = '新旧密码相同！'
                        self.logger.info(msg)
                        return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                    update_user.password = password

                if update_user in session.dirty:
                    await session.flush()

                try:
                    # 更新缓存
                    await self.redis.hset('tab_user-records:', user_id, json.dumps(update_user.to_dict()))
                    await self.redis.delete(f'tab_user-record:{hash_func_params(user_name=update_user.user_name)}')
                except Exception as e:
                    msg = '更新缓存错误！'
                    self.logger.info(msg)
                    self.logger.exception(e)
                    return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM))

                # 新增系统日志
                system_log = {
                    "description": f"更新用户 {update_user.user_name}",
                    "user_id": logger.id,
                    "user_name": logger.user_name
                }
                session.add(TabSystemLog(**system_log))
                await session.flush()

                # 删除缓存
                system_log_name = f'tab_system_log-records:*'
                system_log_keys = await self.redis.keys(system_log_name)
                if system_log_keys:
                    # 清除全部缓存键
                    await self.redis.delete(*system_log_keys)

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())

    async def delete(self, request):
        get_field = partial(get_args, request)

        try:
            user_id = get_field("user_id", field_type=int)

            if not all([user_id]):
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            async with db.slice_session() as session:
                # 查询当前登陆用户权限
                logger = await async_load_user_by_user_id(user_id=request.ctx.user_id, redis=self.redis)
                temporary_permissions = await self.redis.get(f'temporary_permissions:{logger.id}')
                if logger.role_id not in [0, 1, 2] and not temporary_permissions:
                    msg = '当前用户无此权限！'
                    self.logger.info(msg)
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 查询用户是否存在
                del_user_qry_func = select(TabUser).where(TabUser.is_delete == 0, TabUser.id == user_id)
                del_user = await session.execute(del_user_qry_func)
                del_user = del_user.scalars().first()

                if not del_user:
                    msg = '用户不存在！'
                    self.logger.info(msg)
                    return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, msg=msg))

                # 删除用户
                del_user.is_delete = 1

                if del_user in session.dirty:
                    await session.flush()

                # 删除缓存
                try:
                    params_md5 = hash_func_params(user_name=del_user.user_name)
                    record_keys = await self.redis.keys(f'tab_user-record:{user_id}')
                    records_keys = await self.redis.keys(f'tab_user-record:{params_md5}')
                    del_keys = [] + [r.decode() for r in record_keys] + [r.decode() for r in records_keys]
                    if del_keys:
                        # 清除全部缓存键
                        await self.redis.delete(*del_keys)
                    await self.redis.delete('tab_user-records:')
                except Exception as e:
                    msg = '删除缓存错误！'
                    self.logger.info(msg)
                    self.logger.exception(e)
                    return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM))

                # 新增系统日志
                system_log = {
                    "description": f"删除用户 {del_user.user_name}",
                    "user_id": logger.id,
                    "user_name": logger.user_name
                }
                session.add(TabSystemLog(**system_log))
                await session.flush()

                # 删除缓存
                system_log_name = f'tab_system_log-records:*'
                system_log_keys = await self.redis.keys(system_log_name)
                if system_log_keys:
                    # 清除全部缓存键
                    await self.redis.delete(*system_log_keys)

        except Exception as e:
            msg = f'数据库查询错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        return await self.write_json(CfResponse())


class CheckSuperPassword(BaseHandler):
    async def post(self, request):
        get_field = partial(get_jsons, request)

        try:
            password = get_field("password")

            if not password:
                return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK))

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            # 校验超管密码 超级管理员密码规则为superpassword_<year>-<month>（如superpassword_2022-8） md5加密后 取第6位到第11位（共6位）
            now = datetime.now()
            super_password = md5_encryption(f'{request.app.config.SUPER_PASSWORD}_{now.year}-{now.month}')
            if md5_encryption(super_password[5:11]) != password:
                msg = f'超级密码错误！'
                self.logger.info(msg)
                return await self.write_json(CfResponse(err=ErrorCode.AUTH_ERR_ACCOUNT, msg=msg, status=403))

        except Exception as e:
            msg = f'校验超级密码错误！'
            self.logger.error(msg)
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.DB_ERR_UNCONNECTED, msg=msg, status=500))

        logger = await async_load_user_by_user_id(user_id=request.ctx.user_id, redis=self.redis)

        # 设置临时超级权限
        await self.redis.set(f'temporary_permissions:{logger.id}', 1, ex=request.app.config.REDIS_MEDIUM_EXPIRE)

        try:
            async with db.slice_session() as session:
                # 新增系统日志
                system_log = {
                    "description": f"请求超级用户权限",
                    "user_id": logger.id,
                    "user_name": logger.user_name
                }
                session.add(TabSystemLog(**system_log))
                await session.flush()

                # 删除缓存
                system_log_name = f'tab_system_log-records:*'
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
