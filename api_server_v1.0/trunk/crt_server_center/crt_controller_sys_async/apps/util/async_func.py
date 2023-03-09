import hashlib

default_origin = 'redis'


def md5_encryption(word, salt):
    from hashlib import md5
    md5_obj = md5()
    md5_obj.update(f'{word}_{salt}'.encode())
    return md5_obj.hexdigest()


def hash_func_params(*args, **kwargs):
    """
        格式化位置参数和关键字参数
            eg.
                a|b|c|?k=v&k=v
    """

    args_list = [str(_it) for _it in args]
    args_list.sort()

    kwargs_keys_list = list(kwargs.keys())
    kwargs_keys_list.sort()
    kwargs_list = [f'{_it}={kwargs[_it]}' for _it in kwargs_keys_list]

    params_msg = f'{"|".join(args_list)}?{"&".join(kwargs_list)}'
    md5_obj = hashlib.md5(params_msg.encode())
    return md5_obj.hexdigest()


async def default_handle_sql(redis, table_name, op_type, record_id=None):
    """
        默认实现, 统一处理
        两条规则:
            1 根据 user_id, 清理 table_name 关联的记录
            2 根据 user_id, 清理 table_name 列表关联的记录
    :param redis:  redis对象
    :param table_name:  表名
    :param op_type:  数据库操作方式
    :param record_id:  记录id
    :return:
    """
    if op_type in ('insert', 'update', 'delete'):

        record_key = f'{table_name}-record:{record_id}'
        records_key = f'*{table_name}*-records:*'

        try:
            record_keys = redis.keys(record_key)
            records_keys = redis.keys(records_key)

            del_keys = [] + [r.decode() for r in record_keys] + [r.decode() for r in records_keys]

            if del_keys:
                # 清除全部缓存键
                result = redis.delete(*del_keys)
                return True, result

        except Exception as e:
            return False, e

    return True, 0
