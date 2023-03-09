import json

from sanic.log import logger
from sqlalchemy import select, func
from attrdict import AttrDict

from crt_api_sys.apps.util.db_module.models import *
from crt_api_sys.apps.util.async_func import hash_func_params, default_origin, data_pag
from crt_api_sys.apps.util.redis_module import redis_factory
from crt_api_sys.apps.util.db_module.sqlalchemy_factory import db_factory as db


async def async_load_users(page=1, per_page=10, redis=None, origin=default_origin, fast_to_dict=False):
    """
    查询用户列表
    :param page:
    :param per_page:
    :param redis:
    :param origin:
    :param fast_to_dict:
    :return:
    """
    records = []
    k = f'tab_user-records:'
    if origin == 'redis':
        records = await redis_factory.get_hash_cache(k, redis=redis)
        logger.debug(f'load from redis: {records}')

    if not records:
        async with db.slice_session() as session:
            qry_func = select(TabUser).where(TabUser.is_delete == 0)
            records = await session.execute(qry_func)
            records = records.scalars().all()
        logger.debug(f'load from db: {records}')

        if origin == 'redis' and records:
            records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
            await redis.hset(k, mapping=records)

    if fast_to_dict:
        return {int(user_id): json.loads(record) for user_id, record in records.items()}

    if records:
        result = data_pag(records=records, page=page, per_page=per_page)
    else:
        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

    logger.debug(f'data: {result}')

    return result


async def async_load_user_by_user_name(user_name, redis=None, origin=default_origin):
    if user_name == "super":
        return AttrDict({'id': 0, 'user_name': "super", 'role_id': 0, 'role_name': '超级管理员'})

    record = None
    params_md5 = hash_func_params(user_name=user_name)
    k = f'tab_user-record:{params_md5}'
    if origin == 'redis':
        record = await redis_factory.get_string_cache(k, to_json=True, redis=redis)
        logger.debug(f'load from redis: {record}')

    if not record:

        async with db.slice_session() as session:
            qry_func = select(TabUser).where(TabUser.is_delete == 0, TabUser.user_name == user_name)
            record = await session.execute(qry_func)
            record = record.scalars().first()
            record = record.to_dict() if record else None

        logger.debug(f'load from db: {record}')

        if origin == 'redis' and record:
            await redis_factory.set_string_cache(k, record, redis=redis)

    return record


async def async_load_user_by_user_id(user_id, redis=None, origin=default_origin):
    if user_id == 0:
        return AttrDict({'id': 0, 'user_name': "super", 'role_id': 0, 'role_name': '超级管理员'})

    record = None
    k = f'tab_user-records:'
    if origin == 'redis':
        record = await redis_factory.get_hash_item_cache(k, user_id, redis=redis)
        logger.debug(f'load from redis: {record}')

    if not record:
        async with db.slice_session() as session:
            qry_func = select(TabUser).where(TabUser.is_delete == 0)
            records = await session.execute(qry_func)
            records = records.scalars().all()
        logger.debug(f'load from db: {records}')

        if origin == 'redis' and records:
            records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
            await redis.hset(k, mapping=records)
            record = records.get(user_id)

    if isinstance(record, str):
        record = AttrDict(json.loads(record))

    return record


async def async_load_roles(page=1, per_page=10, redis=None, origin=default_origin, fast_to_dict=False):
    """
    查询角色列表
    :param page: 页码
    :param per_page: 每页数量
    :param redis: redis对象
    :param origin: 获取数据方式 db 从mysql中取  redis 从缓存中取
    :param fast_to_dict: 是否转换为dict
    :return:
    """
    records = []
    k = f'tab_role-records:'
    if origin == 'redis':
        records = await redis_factory.get_hash_cache(k, redis=redis)
        logger.debug(f'load from redis: {records}')

    if not records:
        async with db.slice_session() as session:
            qry_func = select(TabRole).where(TabRole.is_delete == 0)
            records = await session.execute(qry_func)
            records = records.scalars().all()
        logger.debug(f'load from db: {records}')

        if origin == 'redis' and records:
            records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
            await redis.hset(k, mapping=records)

    if fast_to_dict:
        return {int(id): json.loads(record) for id, record in records.items()}

    if records:
        result = data_pag(records=records, page=page, per_page=per_page)
    else:
        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

    logger.debug(f'data: {result}')

    return result


async def async_load_role_by_role_id(role_id, redis=None, origin=default_origin):
    record = None
    k = f'tab_role-records:'
    if origin == 'redis':
        record = await redis_factory.get_hash_item_cache(k, role_id, redis=redis)
        logger.debug(f'load from redis: {record}')

    if not record:
        async with db.slice_session() as session:
            qry_func = select(TabRole).where(TabRole.is_delete == 0)
            records = await session.execute(qry_func)
            records = records.scalars().all()
        logger.debug(f'load from db: {records}')

        if origin == 'redis' and records:
            records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
            await redis.hset(k, mapping=records)
            record = records.get(role_id)

    if isinstance(record, str):
        record = AttrDict(json.loads(record))

    logger.debug(f'data: {record}')

    return record


async def async_load_device_type(page=1, per_page=10, redis=None, origin=default_origin, fast_to_dict=False):
    """
    查询设备类型
    :param page: 页码
    :param per_page: 每页数量
    :param redis: redis对象
    :param origin: 获取数据方式 db 从mysql中取  redis 从缓存中取
    :param fast_to_dict: 是否转换为dict
    :return:
    """
    records = []
    k = f'tab_device_type-records:'
    if origin == 'redis':
        records = await redis_factory.get_hash_cache(k, redis=redis)
        logger.debug(f'load from redis: {records}')

    if not records:
        async with db.slice_session() as session:
            qry_func = select(TabDeviceType).where(TabDeviceType.is_delete == 0)
            qry_func = qry_func.order_by(TabDeviceType.priority, TabDeviceType.id)
            records = await session.execute(qry_func)
            records = records.scalars().all()
            records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
        logger.debug(f'load from db: {records}')

        if origin == 'redis' and records:
            await redis.hset(k, mapping=records)

    if fast_to_dict:
        return {int(id): json.loads(record) for id, record in records.items()}

    if records:
        result = data_pag(records=records, page=page, per_page=per_page)
    else:
        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

    logger.debug(f'data: {result}')

    return result


async def async_load_device_type_by_id(device_type_id, redis=None, origin=default_origin):
    """
    查询设备类型
    :param device_type_id: 设备类型id（国标码）
    :param redis: redis对象
    :param origin: 获取数据方式 db 从mysql中取  redis 从缓存中取
    :return:
    """
    record = None
    k = f'tab_device_type-records:'
    if origin == 'redis':
        record = await redis_factory.get_hash_item_cache(k, device_type_id, redis=redis)
        logger.debug(f'load from redis: {record}')

    if not record:
        async with db.slice_session() as session:
            qry_func = select(TabDeviceType).where(TabDeviceType.is_delete == 0)
            records = await session.execute(qry_func)
            records = records.scalars().all()
        logger.debug(f'load from db: {records}')

        if origin == 'redis' and records:
            records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
            await redis.hset(k, mapping=records)
            record = records.get(device_type_id)

    if isinstance(record, str):
        record = AttrDict(json.loads(record))

    logger.debug(f'data: {record}')

    return record


async def async_load_picture_type(page=1, per_page=10, redis=None, origin=default_origin, fast_to_dict=False):
    """
    查询图片类型
    :param page: 页码
    :param per_page: 每页数量
    :param redis: redis对象
    :param origin: 获取数据方式 db 从mysql中取  redis 从缓存中取
    :param fast_to_dict: 是否转换为dict
    :return:
    """
    records = []
    k = f'tab_picture_type-records:'
    if origin == 'redis':
        records = await redis_factory.get_hash_cache(k, redis=redis)
        logger.debug(f'load from redis: {records}')

    if not records:
        async with db.slice_session() as session:
            qry_func = select(TabPictureType).where(TabPictureType.is_delete == 0)
            records = await session.execute(qry_func)
            records = records.scalars().all()
        logger.debug(f'load from db: {records}')

        if origin == 'redis' and records:
            records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
            await redis.hset(k, mapping=records)

    if fast_to_dict:
        return {int(id): json.loads(record) for id, record in records.items()}

    if records:
        result = data_pag(records=records, page=page, per_page=per_page)
    else:
        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

    logger.debug(f'data: {result}')

    return result


async def async_load_picture_type_by_id(picture_type_id, redis=None, origin=default_origin):
    """
    查询图片类型
    :param picture_type_id: 图片类型id
    :param redis: redis对象
    :param origin: 获取数据方式 db 从mysql中取  redis 从缓存中取
    :return:
    """
    record = None
    k = f'tab_picture_type-records:'
    if origin == 'redis':
        record = await redis_factory.get_hash_item_cache(k, picture_type_id, redis=redis)
        logger.debug(f'load from redis: {record}')

    if not record:
        async with db.slice_session() as session:
            qry_func = select(TabPictureType).where(TabPictureType.is_delete == 0)
            records = await session.execute(qry_func)
            records = records.scalars().all()
        logger.debug(f'load from db: {records}')

        if origin == 'redis' and records:
            records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
            await redis.hset(k, mapping=records)
            record = records.get(picture_type_id)

    if isinstance(record, str):
        record = AttrDict(json.loads(record))

    logger.debug(f'data: {record}')

    return record


async def async_load_alarm_type(page=1, per_page=10, redis=None, origin=default_origin, fast_to_dict=False):
    """
    查询报警类型
    :param page: 页码
    :param per_page: 每页数量
    :param redis: redis对象
    :param origin: 获取数据方式 db 从mysql中取  redis 从缓存中取
    :param fast_to_dict: 是否转换为dict
    :return:
    """
    records = []
    k = f'tab_alarm_type-records:'
    if origin == 'redis':
        records = await redis_factory.get_hash_cache(k, redis=redis)
        logger.debug(f'load from redis: {records}')

    if not records:
        async with db.slice_session() as session:
            qry_func = select(TabAlarmType).where(TabAlarmType.is_delete == 0)
            records = await session.execute(qry_func)
            records = records.scalars().all()
        logger.debug(f'load from db: {records}')

        if origin == 'redis' and records:
            records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
            await redis.hset(k, mapping=records)

    if fast_to_dict:
        return {int(id): json.loads(record) for id, record in records.items()}

    if records:
        result = data_pag(records=records, page=page, per_page=per_page)
    else:
        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

    logger.debug(f'data: {result}')

    return result


async def async_load_gb_evt_type(page=1, per_page=10, redis=None, origin=default_origin, fast_to_dict=False):
    """
    查询国标设备类型
    :param page: 页码
    :param per_page: 每页数量
    :param redis: redis对象
    :param origin: 获取数据方式 db 从mysql中取  redis 从缓存中取
    :param fast_to_dict: 是否转换为dict
    :return:
    """
    records = []
    k = f'tab_gb_evt_type-records:'
    if origin == 'redis':
        records = await redis_factory.get_hash_cache(k, redis=redis)
        logger.debug(f'load from redis: {records}')

    if not records:
        async with db.slice_session() as session:
            qry_func = select(TabGbEvtType).where(TabGbEvtType.is_delete == 0)
            records = await session.execute(qry_func)
            records = records.scalars().all()
        logger.debug(f'load from db: {records}')

        if origin == 'redis' and records:
            records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
            await redis.hset(k, mapping=records)

    if fast_to_dict:
        return {int(id): json.loads(record) for id, record in records.items()}

    if records:
        result = data_pag(records=records, page=page, per_page=per_page)
    else:
        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

    logger.debug(f'data: {result}')

    return result


async def async_load_gb_evt_type_by_id(gb_evt_type_id, redis=None, origin=default_origin):
    """
    查询国标设备类型
    :param gb_evt_type_id: 国标设备类型id
    :param redis: redis对象
    :param origin: 获取数据方式 db 从mysql中取  redis 从缓存中取
    :return:
    """
    record = None
    k = f'tab_gb_evt_type-records:'
    if origin == 'redis':
        record = await redis_factory.get_hash_item_cache(k, gb_evt_type_id, redis=redis)
        logger.debug(f'load from redis: {record}')

    if not record:
        async with db.slice_session() as session:
            qry_func = select(TabGbEvtType).where(TabGbEvtType.is_delete == 0)
            records = await session.execute(qry_func)
            records = records.scalars().all()
        logger.debug(f'load from db: {records}')

        if origin == 'redis' and records:
            records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
            await redis.hset(k, mapping=records)
            record = records.get(gb_evt_type_id)

    if isinstance(record, str):
        record = AttrDict(json.loads(record))

    logger.debug(f'data: {record}')

    return record


async def async_load_device_icon(page=1, per_page=10, redis=None, origin=default_origin, fast_to_dict=False):
    """
    查询设备图标
    :param page: 页码
    :param per_page: 每页数量
    :param redis: redis对象
    :param origin: 获取数据方式 db 从mysql中取  redis 从缓存中取
    :param fast_to_dict: 是否转换为dict
    :return:
    """
    records = []
    k = f'tab_device_icon-records:'
    if origin == 'redis':
        records = await redis_factory.get_hash_cache(k, redis=redis)
        logger.debug(f'load from redis: {records}')

    if not records:
        async with db.slice_session() as session:
            qry_func = select(TabIcon).where(TabIcon.is_delete == 0)
            records = await session.execute(qry_func)
            records = records.scalars().all()
        logger.debug(f'load from db: {records}')

        records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}

        if origin == 'redis' and records:
            await redis.hset(k, mapping=records)

    if fast_to_dict:
        return {int(id): json.loads(record) for id, record in records.items()}

    if records:
        result = data_pag(records=records, page=page, per_page=per_page)
    else:
        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

    logger.debug(f'data: {result}')

    return result


async def async_load_device_icon_by_id(icon_id, redis=None, origin=default_origin):
    """
    查询设备图标
    :param icon_id: device_type_id 和 icon_id 在 tab_device_icon 表相同
    :param redis: redis对象
    :param origin: 获取数据方式 db 从mysql中取  redis 从缓存中取
    :return:
    """
    record = None
    k = f'tab_device_icon-records:'
    if origin == 'redis':
        record = await redis_factory.get_hash_item_cache(k, icon_id, redis=redis)
        logger.debug(f'load from redis: {record}')

    if not record:
        async with db.slice_session() as session:
            qry_func = select(TabIcon).where(TabIcon.is_delete == 0)
            records = await session.execute(qry_func)
            records = records.scalars().all()
        logger.debug(f'load from db: {records}')

        if origin == 'redis' and records:
            records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
            await redis.hset(k, mapping=records)
            record = records.get(icon_id)

    if isinstance(record, str):
        record = AttrDict(json.loads(record))

    logger.debug(f'data: {record}')

    return record


async def async_load_controller_by_num(controller_num, redis=None, origin=default_origin):
    record = None
    k = f'tab_controller-record:{controller_num}'
    if origin == 'redis':
        record = await redis_factory.get_string_cache(k, to_json=True, redis=redis)
        logger.debug(f'load from redis: {record}')

    if not record:
        async with db.slice_session() as session:
            qry_func = select(TabController).where(TabController.is_delete == 0, TabController.code == controller_num)
            record = await session.execute(qry_func)
            record = record.scalars().first()
            record = record.to_dict() if record else None

        logger.debug(f'load from db: {record}')

        if origin == 'redis' and record:
            await redis_factory.set_string_cache(k, record, redis=redis)

    logger.debug(f'data: {record}')

    return record


async def async_load_devices(page=1, per_page=10, redis=None, origin=default_origin, fast_to_dict=False):
    records = []
    k = f'tab_device-records:'
    if origin == 'redis':
        records = await redis_factory.get_hash_cache(k, redis=redis)
        logger.debug(f'load from redis: {records}')

    if not records:
        async with db.slice_session() as session:
            qry_func = select(TabDevice).where(TabDevice.is_delete == 0)
            records = await session.execute(qry_func)
            records = records.scalars().all()

        if origin == 'redis' and records:
            records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
            await redis.hset(k, mapping=records)

        logger.debug(f'load from db: {records}')

    if fast_to_dict:
        return {int(id): json.loads(record) for id, record in records.items()}

    if records:
        result = data_pag(records=records, page=page, per_page=per_page)
    else:
        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

    logger.debug(f'data: {result}')

    return result


async def async_load_device_by_location(controller_num, loop_num, addr_num, redis=None, origin=default_origin):
    record = None
    params_md5 = hash_func_params(controller_num=controller_num, loop_num=loop_num, addr_num=addr_num)
    k = f'tab_device-record:{params_md5}'
    if origin == 'redis':
        record = await redis_factory.get_string_cache(k, to_json=True, redis=redis)
        logger.debug(f'load from redis: {record}')

    if not record:

        async with db.slice_session() as session:
            qry_func = select(TabDevice).where(TabDevice.is_delete == 0, TabDevice.controller_num == controller_num,
                                               TabDevice.loop_num == loop_num, TabDevice.addr_num == addr_num)
            record = await session.execute(qry_func)
            record = record.scalars().first()
            record = record.to_dict() if record else None

        logger.debug(f'load from db: {record}')

        if origin == 'redis' and record:
            await redis_factory.set_string_cache(k, record, redis=redis)

    logger.debug(f'data: {record}')

    return record


async def async_load_alarm_logs_by_params(redis=None, origin='db', **kwargs):
    result = {}
    params_md5 = hash_func_params(**kwargs)
    k = f'tab_alarm_log-records:{params_md5}'
    if origin == 'redis':
        result = await redis_factory.get_string_cache(k, to_json=True, redis=redis)
        logger.debug(f'load from redis: {result}')

    if not result:
        is_all = kwargs.get('is_all', 0)
        page = kwargs.get('page')
        per_page = kwargs.get('per_page')

        is_clear = kwargs.get('is_clear')

        st = kwargs.get('st')
        et = kwargs.get('et')
        description = kwargs.get('description')
        area_id = kwargs.get('area_id')
        build_id = kwargs.get('build_id')
        floor_id = kwargs.get('floor_id')
        controller_num = kwargs.get('controller_num')
        loop_num = kwargs.get('loop_num')
        addr_num = kwargs.get('addr_num')
        equipment_num = kwargs.get('equipment_num')
        module_num = kwargs.get('module_num')
        alarm_type_id = kwargs.get('alarm_type_id')
        alarm_status = kwargs.get('alarm_status')
        alarm_type = kwargs.get('alarm_type')
        device_id = kwargs.get('device_id')
        device_type_ids = kwargs.get('device_type_ids')

        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

        async with db.slice_session() as session:
            count_qry_func = select(func.count(TabAlarmLog.id)).where(TabAlarmLog.is_delete == 0)
            qry_func = select(TabAlarmLog).where(TabAlarmLog.is_delete == 0)

            if is_clear is not None:
                count_qry_func = count_qry_func.filter(TabAlarmLog.is_clear == is_clear)
                qry_func = qry_func.filter(TabAlarmLog.is_clear == is_clear)

            if description:
                count_qry_func = count_qry_func.filter(TabAlarmLog.description.like(f'%{description}%'))
                qry_func = qry_func.filter(TabAlarmLog.description.like(f'%{description}%'))

            if st and et:
                st = f'{st} 00:00:00'
                et = f'{et} 23:59:59'
                count_qry_func = count_qry_func.filter(TabAlarmLog.create_time.between(st, et))
                qry_func = qry_func.filter(TabAlarmLog.create_time.between(st, et))

            if area_id:
                count_qry_func = count_qry_func.filter(TabAlarmLog.area_id == area_id)
                qry_func = qry_func.filter(TabAlarmLog.area_id == area_id)

            if build_id:
                count_qry_func = count_qry_func.filter(TabAlarmLog.build_id == build_id)
                qry_func = qry_func.filter(TabAlarmLog.build_id == build_id)

            if floor_id:
                count_qry_func = count_qry_func.filter(TabAlarmLog.floor_id == floor_id)
                qry_func = qry_func.filter(TabAlarmLog.floor_id == floor_id)

            if controller_num is not None:
                count_qry_func = count_qry_func.filter(TabAlarmLog.controller_num == controller_num)
                qry_func = qry_func.filter(TabAlarmLog.controller_num == controller_num)

            if loop_num:
                count_qry_func = count_qry_func.filter(TabAlarmLog.loop_num == loop_num)
                qry_func = qry_func.filter(TabAlarmLog.loop_num == loop_num)

            if addr_num:
                count_qry_func = count_qry_func.filter(TabAlarmLog.addr_num == addr_num)
                qry_func = qry_func.filter(TabAlarmLog.addr_num == addr_num)

            if equipment_num:
                count_qry_func = count_qry_func.filter(TabAlarmLog.equipment_num == equipment_num)
                qry_func = qry_func.filter(TabAlarmLog.equipment_num == equipment_num)

            if module_num:
                count_qry_func = count_qry_func.filter(TabAlarmLog.module_num == module_num)
                qry_func = qry_func.filter(TabAlarmLog.module_num == module_num)

            if alarm_type_id:
                count_qry_func = count_qry_func.filter(TabAlarmLog.alarm_type_id == alarm_type_id)
                qry_func = qry_func.filter(TabAlarmLog.alarm_type_id == alarm_type_id)

            if device_type_ids:
                count_qry_func = count_qry_func.filter(TabAlarmLog.device_type_id.in_(device_type_ids))
                qry_func = qry_func.filter(TabAlarmLog.device_type_id.in_(device_type_ids))

            if alarm_status is not None:
                count_qry_func = count_qry_func.filter(TabAlarmLog.alarm_status == alarm_status)
                qry_func = qry_func.filter(TabAlarmLog.alarm_status == alarm_status)

            if alarm_type is not None:
                count_qry_func = count_qry_func.filter(TabAlarmLog.alarm_type == alarm_type)
                qry_func = qry_func.filter(TabAlarmLog.alarm_type == alarm_type)

            if device_id:
                count_qry_func = count_qry_func.filter(TabAlarmLog.device_id == device_id)
                qry_func = qry_func.filter(TabAlarmLog.device_id == device_id)

            qry_func = qry_func.order_by(TabAlarmLog.create_time.desc())

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
                if page == 0 and is_all:
                    result['record_size'] = total
                else:
                    result['record_size'] = total
                    qry_func = qry_func.limit(200)

            records = await session.execute(qry_func)
            records = records.scalars().all()
            result['items'] = [record.to_dict() for record in records]

        logger.debug(f'load from db: {result}')

        if origin == 'redis' and result['items']:
            await redis_factory.set_string_cache(k, result, redis=redis)

    return result


async def async_load_alarm_log_by_id(alarm_log_id, redis=None, origin=default_origin):
    """
    查询单条报警记录
    :param alarm_log_id: 报警记录id
    :param redis:
    :param origin:
    :return:
    """
    record = []
    k = f'tab_alarm_log-record:{alarm_log_id}'
    if origin == 'redis':
        record = await redis_factory.get_string_cache(k, to_json=True, redis=redis)
        logger.debug(f'load from redis: {record}')

    if not record:
        record = await TabAlarmLog.async_fetch_record_by_id(record_id=alarm_log_id)
        logger.debug(f'load from db: {record}')

        if origin == 'redis' and record:
            await redis_factory.set_string_cache(k, record, redis=redis)

    logger.debug(f'data: {record}')

    return record


async def async_load_build_drawings_by_params(redis=None, origin=default_origin, **kwargs):
    result = {}
    params_md5 = hash_func_params(**kwargs)
    k = f'tab_floor-records:{params_md5}'
    if origin == 'redis':
        result = await redis_factory.get_string_cache(k, to_json=True, redis=redis)
        logger.debug(f'load from redis: {result}')

    if not result:
        is_all = kwargs.get('is_all', 0)
        page = kwargs.get('page')
        per_page = kwargs.get('per_page')

        area_id = kwargs.get('area_id')
        build_id = kwargs.get('build_id')
        floor_id = kwargs.get('floor_id')

        is_alarm = kwargs.get('is_alarm')
        state = kwargs.get('state')

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

            if floor_id:
                count_qry_func = count_qry_func.filter(TabFloor.id == floor_id)
                qry_func = qry_func.filter(TabFloor.id == floor_id)

            if is_alarm == 0:
                count_qry_func = count_qry_func.filter(TabFloor.alarm == 0)
                qry_func = qry_func.filter(TabFloor.alarm == 0)
            elif is_alarm == 1:
                count_qry_func = count_qry_func.filter(TabFloor.alarm > 0)
                qry_func = qry_func.filter(TabFloor.alarm > 0)

            if state:
                if state == 1:  # 火警
                    count_qry_func = count_qry_func.filter(TabFloor.fire > 0)
                    qry_func = qry_func.filter(TabFloor.fire > 0)
                elif state == 2:  # 联动
                    count_qry_func = count_qry_func.filter(TabFloor.linkage > 0)
                    qry_func = qry_func.filter(TabFloor.linkage > 0)
                elif state == 3:  # 反馈
                    count_qry_func = count_qry_func.filter(TabFloor.feedback > 0)
                    qry_func = qry_func.filter(TabFloor.feedback > 0)
                elif state == 4:  # 故障
                    count_qry_func = count_qry_func.filter(TabFloor.malfunction > 0)
                    qry_func = qry_func.filter(TabFloor.malfunction > 0)
                elif state == 5:  # 屏蔽
                    count_qry_func = count_qry_func.filter(TabFloor.shielding > 0)
                    qry_func = qry_func.filter(TabFloor.shielding > 0)
                elif state == 6:  # 监管
                    count_qry_func = count_qry_func.filter(TabFloor.supervise > 0)
                    qry_func = qry_func.filter(TabFloor.supervise > 0)
                elif state == 7:  # 声光故障
                    count_qry_func = count_qry_func.filter(TabFloor.vl_malfunction > 0)
                    qry_func = qry_func.filter(TabFloor.vl_malfunction > 0)
                elif state == 8:  # 声光屏蔽
                    count_qry_func = count_qry_func.filter(TabFloor.vl_shielding > 0)
                    qry_func = qry_func.filter(TabFloor.vl_shielding > 0)

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
                if page == 0 and is_all:
                    result['record_size'] = total
                else:
                    result['record_size'] = total
                    qry_func = qry_func.limit(200)

            records = await session.execute(qry_func)
            records = records.scalars().all()
            result['items'] = [record.to_dict() for record in records]

        logger.debug(f'load from db: {result}')

        if origin == 'redis' and result['items']:
            await redis_factory.set_string_cache(k, result, redis=redis)

    return result


async def async_load_assign_devices_by_params(page=1, per_page=10, redis=None, origin=default_origin, refresh_redis=False, **kwargs):
    records = {}
    params_md5 = hash_func_params(**kwargs)
    k = f'tab_assign_device-records:{params_md5}'
    if origin == 'redis' and refresh_redis is False:
        records = await redis_factory.get_hash_cache(k, redis=redis)
        logger.debug(f'load from redis: {records}')

    if not records or refresh_redis:
        floor_id = kwargs.get('floor_id')
        device_status = kwargs.get('device_status')

        async with db.slice_session() as session:
            qry_func = select(TabAssignDevice).where(TabAssignDevice.is_delete == 0)

            if floor_id:
                qry_func = qry_func.filter(TabAssignDevice.floor_id == floor_id)

            if device_status == 0:
                qry_func = qry_func.filter(TabAssignDevice.device_status == 0)
            elif device_status == 1:
                qry_func = qry_func.filter(TabAssignDevice.device_status > 0)

            records = await session.execute(qry_func)
            records = records.scalars().all()

            if origin == 'redis' and records:
                records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
                await redis.hset(k, mapping=records)
            else:
                records = [json.dumps(record.to_dict(is_attr_dict=False)) for record in records]

    if records:
        result = data_pag(records=records, page=page, per_page=per_page)
    else:
        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

    logger.debug(f'load from db: {result}')

    return result


async def async_load_controller_op_logs_by_params(redis=None, origin=default_origin, **kwargs):
    result = {}
    params_md5 = hash_func_params(**kwargs)
    k = f'tab_controller_op_log-records:{params_md5}'
    if origin == 'redis':
        result = await redis_factory.get_string_cache(k, to_json=True, redis=redis)
        logger.debug(f'load from redis: {result}')

    if not result:
        is_all = kwargs.get('is_all', 0)
        page = kwargs.get('page')
        per_page = kwargs.get('per_page')

        st = kwargs.get('st')
        et = kwargs.get('et')
        controller_id = kwargs.get('controller_id')
        controller_num = kwargs.get('controller_num')
        controller_name = kwargs.get('controller_name')
        gb_evt_type_id = kwargs.get('gb_evt_type_id')
        gb_evt_type_ids = kwargs.get('gb_evt_type_ids')
        description = kwargs.get('description')

        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

        async with db.slice_session() as session:
            count_qry_func = select(func.count(TabControllerOpLog.id)).where(TabControllerOpLog.is_delete == 0)
            qry_func = select(TabControllerOpLog).where(TabControllerOpLog.is_delete == 0)

            if st and et:
                st = f'{st} 00:00:00'
                et = f'{et} 23:59:59'
                count_qry_func = count_qry_func.filter(TabControllerOpLog.create_time.between(st, et))
                qry_func = qry_func.filter(TabControllerOpLog.create_time.between(st, et))

            if controller_id:
                count_qry_func = count_qry_func.filter(TabControllerOpLog.controller_id == controller_id)
                qry_func = qry_func.filter(TabControllerOpLog.controller_id == controller_id)

            if controller_num is not None:
                count_qry_func = count_qry_func.filter(TabControllerOpLog.controller_num == controller_num)
                qry_func = qry_func.filter(TabControllerOpLog.controller_num == controller_num)

            if controller_name:
                count_qry_func = count_qry_func.filter(TabControllerOpLog.controller_name.like(f'%{controller_name}%'))
                qry_func = qry_func.filter(TabControllerOpLog.controller_name.like(f'%{controller_name}%'))

            if gb_evt_type_id:
                count_qry_func = count_qry_func.filter(TabControllerOpLog.gb_evt_type_id == gb_evt_type_id)
                qry_func = qry_func.filter(TabControllerOpLog.gb_evt_type_id == gb_evt_type_id)

            if gb_evt_type_ids:
                count_qry_func = count_qry_func.filter(TabControllerOpLog.gb_evt_type_id.in_(gb_evt_type_ids))
                qry_func = qry_func.filter(TabControllerOpLog.gb_evt_type_id.in_(gb_evt_type_ids))

            if description:
                count_qry_func = count_qry_func.filter(TabControllerOpLog.description.like(f'%{description}%'))
                qry_func = qry_func.filter(TabControllerOpLog.description.like(f'%{description}%'))

            qry_func = qry_func.order_by(TabControllerOpLog.update_time.desc())

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
                if page == 0 and is_all:
                    result['record_size'] = total
                else:
                    result['record_size'] = total
                    qry_func = qry_func.limit(200)

            records = await session.execute(qry_func)
            records = records.scalars().all()
            result['items'] = [record.to_dict() for record in records]

        logger.debug(f'load from db: {result}')

        if origin == 'redis' and result['items']:
            await redis_factory.set_string_cache(k, result, redis=redis)

    return result


async def async_load_maintenance_logs_by_params(redis=None, origin=default_origin, **kwargs):
    result = {}
    params_md5 = hash_func_params(**kwargs)
    k = f'tab_maintenance_log-records:{params_md5}'
    if origin == 'redis':
        result = await redis_factory.get_string_cache(k, to_json=True, redis=redis)
        logger.debug(f'load from redis: {result}')

    if not result:
        is_all = kwargs.get('is_all', 0)
        page = kwargs.get('page')
        per_page = kwargs.get('per_page')

        st = kwargs.get('st')
        et = kwargs.get('et')
        description = kwargs.get('description')
        user_id = kwargs.get('user_id')
        project_id = kwargs.get('project_id')

        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

        async with db.slice_session() as session:
            count_qry_func = select(func.count(TabMaintenanceLog.id)).where(TabMaintenanceLog.is_delete == 0)
            qry_func = select(TabMaintenanceLog).where(TabMaintenanceLog.is_delete == 0)

            if st and et:
                st = f'{st} 00:00:00'
                et = f'{et} 23:59:59'
                count_qry_func = count_qry_func.filter(TabMaintenanceLog.create_time.between(st, et))
                qry_func = qry_func.filter(TabMaintenanceLog.create_time.between(st, et))

            if description:
                count_qry_func = count_qry_func.filter(TabMaintenanceLog.description.like(f'%{description}%'))
                qry_func = qry_func.filter(TabMaintenanceLog.description.like(f'%{description}%'))

            if user_id:
                count_qry_func = count_qry_func.filter(TabMaintenanceLog.user_id == user_id)
                qry_func = qry_func.filter(TabMaintenanceLog.user_id == user_id)

            if project_id:
                count_qry_func = count_qry_func.filter(TabMaintenanceLog.project_id == project_id)
                qry_func = qry_func.filter(TabMaintenanceLog.project_id == project_id)

            qry_func = qry_func.order_by(TabMaintenanceLog.update_time.desc())

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
                if page == 0 and is_all:
                    result['record_size'] = total
                else:
                    result['record_size'] = total
                    qry_func = qry_func.limit(200)

            records = await session.execute(qry_func)
            records = records.scalars().all()
            result['items'] = [record.to_dict() for record in records]

        logger.debug(f'load from db: {result}')

        if origin == 'redis' and result['items']:
            await redis_factory.set_string_cache(k, result, redis=redis)

    return result


async def async_load_shift_records_by_params(redis=None, origin=default_origin, **kwargs):
    result = {}
    params_md5 = hash_func_params(**kwargs)
    k = f'tab_shift_record-records:{params_md5}'
    if origin == 'redis':
        result = await redis_factory.get_string_cache(k, to_json=True, redis=redis)
        logger.debug(f'load from redis: {result}')

    if not result:
        is_all = kwargs.get('is_all', 0)
        page = kwargs.get('page')
        per_page = kwargs.get('per_page')

        st = kwargs.get('st')
        et = kwargs.get('et')
        watch_user_id = kwargs.get('watch_user_id')
        change_user_id = kwargs.get('change_user_id')

        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

        async with db.slice_session() as session:
            count_qry_func = select(func.count(TabShiftRecord.id)).where(TabShiftRecord.is_delete == 0)
            qry_func = select(TabShiftRecord).where(TabShiftRecord.is_delete == 0)

            if st and et:
                st = f'{st} 00:00:00'
                et = f'{et} 23:59:59'
                count_qry_func = count_qry_func.filter(TabShiftRecord.create_time.between(st, et))
                qry_func = qry_func.filter(TabShiftRecord.create_time.between(st, et))

            if watch_user_id:
                count_qry_func = count_qry_func.filter(TabShiftRecord.watch_user_id == watch_user_id)
                qry_func = qry_func.filter(TabShiftRecord.watch_user_id == watch_user_id)

            if change_user_id:
                count_qry_func = count_qry_func.filter(TabShiftRecord.change_user_id == change_user_id)
                qry_func = qry_func.filter(TabShiftRecord.change_user_id == change_user_id)

            qry_func = qry_func.order_by(TabShiftRecord.update_time.desc())

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
                if page == 0 and is_all:
                    result['record_size'] = total
                else:
                    result['record_size'] = total
                    qry_func = qry_func.limit(200)

            records = await session.execute(qry_func)
            records = records.scalars().all()
            result['items'] = [record.to_dict() for record in records]

        logger.debug(f'load from db: {result}')

        if origin == 'redis' and result['items']:
            await redis_factory.set_string_cache(k, result, redis=redis)

    return result


async def async_load_system_logs_by_params(redis=None, origin=default_origin, **kwargs):
    result = {}
    params_md5 = hash_func_params(**kwargs)
    k = f'tab_system_log-records:{params_md5}'
    if origin == 'redis':
        result = await redis_factory.get_string_cache(k, to_json=True, redis=redis)
        logger.debug(f'load from redis: {result}')

    if not result:
        is_all = kwargs.get('is_all', 0)
        page = kwargs.get('page')
        per_page = kwargs.get('per_page')

        st = kwargs.get('st')
        et = kwargs.get('et')
        description = kwargs.get('description')
        user_id = kwargs.get('user_id')

        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

        async with db.slice_session() as session:
            count_qry_func = select(func.count(TabSystemLog.id)).where(TabSystemLog.is_delete == 0)
            qry_func = select(TabSystemLog).where(TabSystemLog.is_delete == 0)

            if st and et:
                st = f'{st} 00:00:00'
                et = f'{et} 23:59:59'
                count_qry_func = count_qry_func.filter(TabSystemLog.create_time.between(st, et))
                qry_func = qry_func.filter(TabSystemLog.create_time.between(st, et))

            if description:
                count_qry_func = count_qry_func.filter(TabSystemLog.description.like(f'%{description}%'))
                qry_func = qry_func.filter(TabSystemLog.description.like(f'%{description}%'))

            if user_id:
                count_qry_func = count_qry_func.filter(TabSystemLog.user_id == user_id)
                qry_func = qry_func.filter(TabSystemLog.user_id == user_id)

            qry_func = qry_func.order_by(TabSystemLog.update_time.desc())

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
                if page == 0 and is_all:
                    result['record_size'] = total
                else:
                    result['record_size'] = total
                    qry_func = qry_func.limit(200)

            records = await session.execute(qry_func)
            records = records.scalars().all()
            result['items'] = [record.to_dict() for record in records]

        logger.debug(f'load from db: {result}')

        if origin == 'redis' and result['items']:
            await redis_factory.set_string_cache(k, result, redis=redis)

    return result


async def async_load_assign_devices_by_floor_id(page=1, per_page=10, redis=None, origin=default_origin, floor_id=None):
    records = {}
    params_md5 = hash_func_params(page=page, per_page=per_page, floor_id=floor_id)
    k = f'tab_assign_device-records:{params_md5}'
    if origin == 'redis':
        records = await redis_factory.get_hash_cache(k, redis=redis)
        logger.debug(f'load from redis: {records}')

    if not records:

        async with db.slice_session() as session:
            qry_func = select(TabAssignDevice).where(TabAssignDevice.is_delete == 0)

            if floor_id:
                qry_func = qry_func.where(TabAssignDevice.floor_id == floor_id)

            records = await session.execute(qry_func)
            records = records.scalars().all()

            if origin == 'redis' and records:
                records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
                await redis.hset(k, mapping=records)
            else:
                records = [json.dumps(record.to_dict(is_attr_dict=False)) for record in records]

    if records:
        result = data_pag(records=records, page=page, per_page=per_page)
    else:
        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

    logger.debug(f'data: {result}')

    return result


async def async_load_devices_by_floor_id(page=1, per_page=10, redis=None, origin=default_origin, floor_id=None, refresh_redis=False):
    records = {}
    params_md5 = hash_func_params(page=page, per_page=per_page, floor_id=floor_id)
    k = f'tab_device-records:{params_md5}'
    if origin == 'redis' and refresh_redis is False:
        records = await redis_factory.get_hash_cache(k, redis=redis)
        logger.debug(f'load from redis: {records}')

    if not records or refresh_redis:
        async with db.slice_session() as session:
            qry_func = select(TabDevice).where(TabDevice.is_delete == 0)

            if floor_id:
                qry_func = qry_func.where(TabDevice.assign_floor_id == floor_id)

            records = await session.execute(qry_func)
            records = records.scalars().all()

            if origin == 'redis' and records:
                records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
                await redis.hset(k, mapping=records)
            else:
                records = [json.dumps(record.to_dict(is_attr_dict=False)) for record in records]

    if records:
        result = data_pag(records=records, page=page, per_page=per_page)
    else:
        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

    logger.debug(f'data: {result}')

    return result


async def async_load_system_param(redis=None, origin=default_origin):
    record = {}
    k = f'tab_system_param-record:'
    if origin == 'redis':
        record = await redis_factory.get_hash_cache(k, redis=redis)
        logger.debug(f'load from redis: {record}')

    if not record:
        async with db.slice_session() as session:
            qry_func = select(TabSystemParam).where(TabSystemParam.is_delete == 0)
            qry_func = qry_func.order_by(TabSystemParam.update_time.desc())
            record = await session.execute(qry_func)
            record = record.scalars().first()
            record = record.to_dict() if record else None

        logger.debug(f'load from db: {record}')

        if origin == 'redis' and record:
            await redis.hset(k, 'carousel_time', record.get('carousel_time') or 0, redis=redis)
            await redis.hset(k, 'crt_sn', record.get('crt_sn') or '', redis=redis)

    return record


async def async_load_center(redis=None, origin=default_origin):
    record = {}
    k = f'tab_center-record:'
    if origin == 'redis':
        record = await redis_factory.get_string_cache(k, to_json=True, redis=redis)
        logger.debug(f'load from redis: {record}')

    if not record:
        async with db.slice_session() as session:
            qry_func = select(TabCenter).where(TabCenter.is_delete == 0).order_by(TabCenter.update_time.desc())
            record = await session.execute(qry_func)
            record = record.scalars().first()
            record = record.to_dict() if record else None

        logger.debug(f'load from db: {record}')

        if origin == 'redis' and record:
            await redis.set(k, json.dumps(record))

    return record


async def async_load_last_version(redis=None, origin=default_origin):
    record = {}
    k = f'tab_version-record:'
    if origin == 'redis':
        record = await redis_factory.get_string_cache(k, to_json=True, redis=redis)
        logger.debug(f'load from redis: {record}')

    if not record:
        async with db.slice_session() as session:
            qry_func = select(TabVersion).where(TabVersion.is_delete == 0)
            qry_func = qry_func.order_by(TabVersion.create_time.desc())
            record = await session.execute(qry_func)
            record = record.scalars().first()
            record = record.to_dict() if record else None

        logger.debug(f'load from db: {record}')

        if origin == 'redis' and record:
            await redis_factory.set_string_cache(k, json.dumps(record), redis=redis)

    logger.debug(f'data: {record}')

    return record


async def async_load_versions(redis=None, origin=default_origin, **kwargs):
    result = {}
    params_md5 = hash_func_params(**kwargs)
    k = f'tab_version-records:{params_md5}'
    if origin == 'redis':
        result = await redis_factory.get_string_cache(k, to_json=True, redis=redis)
        logger.debug(f'load from redis: {result}')

    if not result:
        is_all = kwargs.get('is_all', 0)
        page = kwargs.get('page')
        per_page = kwargs.get('per_page')

        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

        async with db.slice_session() as session:
            count_qry_func = select(func.count(TabVersion.id)).where(TabVersion.is_delete == 0)
            qry_func = select(TabVersion).where(TabVersion.is_delete == 0)

            qry_func = qry_func.order_by(TabVersion.create_time.desc())

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
                if page == 0 and is_all:
                    result['record_size'] = total
                else:
                    result['record_size'] = total
                    qry_func = qry_func.limit(200)

            records = await session.execute(qry_func)
            records = records.scalars().all()
            result['items'] = [record.to_dict() for record in records]

        logger.debug(f'load from db: {result}')

        if origin == 'redis' and result['items']:
            await redis_factory.set_string_cache(k, result, redis=redis)

    logger.debug(f'load from db: {result}')

    return result
