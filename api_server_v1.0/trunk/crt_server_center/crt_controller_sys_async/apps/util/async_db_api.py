import json

from sanic.log import logger
from sqlalchemy import select, func
from attrdict import AttrDict

from apps.util.db_module.models import *
from apps.util.async_func import hash_func_params, default_origin
from apps.util.redis_module import redis_factory
from apps.util.db_module.sqlalchemy_factory import db_factory as db


def data_pag(records, page, per_page):
    if isinstance(records, dict):
        records = list(records.values())

    result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

    result['record_size'] = len(records)

    divisor, remainder = divmod(len(records), per_page)
    result['page_size'] = (divisor + 1 if remainder > 0 else divisor) if page else 0

    records = records[(page - 1) * per_page:page * per_page] if page else records
    result['items'] = [json.loads(record) for record in records]

    return result


async def async_load_user_by_user_name(user_name, redis=None, origin=default_origin):
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
    record = None
    k = f'tab_user-record:{user_id}'
    if origin == 'redis':
        record = await redis_factory.get_string_cache(k, to_json=True, redis=redis)
        logger.debug(f'load from redis: {record}')

    if not record:

        async with db.slice_session() as session:
            qry_func = select(TabUser).where(TabUser.is_delete == 0, TabUser.id == user_id)
            record = await session.execute(qry_func)
            record = record.scalars().first()
            record = record.to_dict() if record else None

        logger.debug(f'load from db: {record}')

        if origin == 'redis' and record:
            await redis_factory.set_string_cache(k, record, redis=redis)

    return record


async def async_load_role_by_role_id(role_id, redis=None, origin=default_origin):
    record = None
    k = f'tab_role-record:{role_id}'
    if origin == 'redis':
        record = await redis_factory.get_string_cache(k, to_json=True, redis=redis)
        logger.debug(f'load from redis: {record}')

    if not record:

        async with db.slice_session() as session:
            qry_func = select(TabRole).where(TabRole.is_delete == 0, TabRole.id == role_id)
            record = await session.execute(qry_func)
            record = record.scalars().first()
            record = record.to_dict() if record else None

        logger.debug(f'load from db: {record}')

        if origin == 'redis' and record:
            await redis_factory.set_string_cache(k, record, redis=redis)

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
            records = await session.execute(qry_func)
            records = records.scalars().all()
        logger.debug(f'load from db: {records}')

        if origin == 'redis' and records:
            records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
            await redis.hset(k, mapping=records)

    if fast_to_dict:
        return {id: json.loads(record) for id, record in records.items()}

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
    record = {}
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

    record = AttrDict(json.loads(record))
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
        return {id: json.loads(record) for id, record in records.items()}

    if records:
        result = data_pag(records=records, page=page, per_page=per_page)
    else:
        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

    logger.debug(f'data: {result}')

    return result


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
        return {id: json.loads(record) for id, record in records.items()}

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
        return {id: json.loads(record) for id, record in records.items()}

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
    record = {}
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

    record = AttrDict(json.loads(record))
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

        if origin == 'redis' and records:
            records = {record.id: json.dumps(record.to_dict(is_attr_dict=False)) for record in records}
            await redis.hset(k, mapping=records)

    if fast_to_dict:
        return {id: json.loads(record) for id, record in records.items()}

    if records:
        result = data_pag(records=records, page=page, per_page=per_page)
    else:
        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

    logger.debug(f'data: {result}')

    return result


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

    return record


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
                                               loop_num == loop_num, addr_num == addr_num)
            record = await session.execute(qry_func)
            record = record.scalars().first()
            record = record.to_dict() if record else None

        logger.debug(f'load from db: {record}')

        if origin == 'redis' and record:
            await redis_factory.set_string_cache(k, record, redis=redis)

    return record


async def async_load_alarm_logs_by_params(redis=None, origin=default_origin, **kwargs):
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

        result = AttrDict(dict(record_size=0, page_size=0, page=page, items=[]))

        async with db.slice_session() as session:
            count_qry_func = select(func.count(TabAlarmLog.id)).where(TabAlarmLog.is_delete == 0)
            qry_func = select(TabAlarmLog).where(TabAlarmLog.is_delete == 0)

            if is_clear == 0:
                count_qry_func = count_qry_func.filter(TabAlarmLog.is_clear == 0)
                qry_func = qry_func.filter(TabAlarmLog.is_clear == 0)

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

            if controller_num:
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

            if alarm_status:
                count_qry_func = count_qry_func.filter(TabAlarmLog.alarm_status == alarm_status)
                qry_func = qry_func.filter(TabAlarmLog.alarm_status == alarm_status)

            if alarm_type:
                count_qry_func = count_qry_func.filter(TabAlarmLog.alarm_type == alarm_type)
                qry_func = qry_func.filter(TabAlarmLog.alarm_type == alarm_type)

            if device_id:
                count_qry_func = count_qry_func.filter(TabAlarmLog.device_id == device_id)
                qry_func = qry_func.filter(TabAlarmLog.device_id == device_id)

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
