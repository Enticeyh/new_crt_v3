import sys
import json
import redis

from sanic.log import logger
from attrdict import AttrDict
from os.path import dirname, realpath

root_project_dir = dirname(dirname(dirname(dirname(realpath(__file__)))))
if root_project_dir not in sys.path:
    sys.path.append(root_project_dir)


def check_config_params(cfg_class):
    if not hasattr(cfg_class, 'REDIS_URL'):
        raise ValueError('redis_module 模块, 请正确配置 REDIS_URL 配置项')

    if not hasattr(cfg_class, 'REDIS_SHORT_EXPIRE'):
        raise ValueError('redis_module 模块, 请正确配置 REDIS_SHORT_EXPIRE 配置项')

    if not hasattr(cfg_class, 'REDIS_MEDIUM_EXPIRE'):
        raise ValueError('redis_module 模块, 请正确配置 REDIS_MEDIUM_EXPIRE 配置项')

    if not hasattr(cfg_class, 'REDIS_LONG_EXPIRE'):
        raise ValueError('redis_module 模块, 请正确配置 REDIS_LONG_EXPIRE 配置项')

    if not hasattr(cfg_class, 'REDIS_LONG_LONG_EXPIRE'):
        raise ValueError('redis_module 模块, 请正确配置 REDIS_LONG_LONG_EXPIRE 配置项')

    logger.info(f'redis config >>>')
    logger.info(f'REDIS_URL: {cfg_class.REDIS_URL}')
    logger.info(f'REDIS_SHORT_EXPIRE: {cfg_class.REDIS_SHORT_EXPIRE}')
    logger.info(f'REDIS_MEDIUM_EXPIRE: {cfg_class.REDIS_MEDIUM_EXPIRE}')
    logger.info(f'REDIS_LONG_EXPIRE: {cfg_class.REDIS_LONG_EXPIRE}')
    logger.info(f'REDIS_LONG_LONG_EXPIRE: {cfg_class.REDIS_LONG_LONG_EXPIRE}')
    logger.info(f' <<<')


def convert(data: object):
    if isinstance(data, bytes):
        return data.decode('utf-8')
    if isinstance(data, dict):
        return dict(list(map(convert, data.items())))
    if isinstance(data, tuple):
        return list(map(convert, data))
    if isinstance(data, list):
        return [convert(item) for item in data]
    if isinstance(data, set):
        return {convert(item) for item in data}
    return data


class RedisFactory:
    _pool = None
    redis_url = None
    cfg_class = None

    def __init__(self):
        pass

    @classmethod
    def from_config(cls, cfg_class):
        """
            本函数, 系统初始化时, 需被调用执行
        :param cfg_class:
        :return:
        """
        # check config class
        check_config_params(cfg_class)

        cls.cfg_class = cfg_class
        cls.redis_url = cfg_class.REDIS_URL

    @classmethod
    def load_pool(cls):

        if not cls.redis_url:
            raise ValueError('common/redis_module 模块请先调用 from_config 进行初始化')

        # with lock:
        if cls._pool is None:
            cls._pool = redis.ConnectionPool.from_url(cls.redis_url)
        return cls._pool

    @classmethod
    def get_redis(cls):
        return redis.Redis(connection_pool=cls.load_pool())

    @classmethod
    def set_string_cache(cls, k, v, ex=None, conn=None):
        """
            设置 string 类型缓存设置, 并添加过期时间
        :param k:
        :param v:
        :param ex:
        :param conn:
        :return:
        """
        if conn is None:
            conn = cls.get_redis()

        if not isinstance(v, str):
            v = json.dumps(v)

        conn.set(k, v, ex or cls.cfg_class.REDIS_SHORT_EXPIRE)
        conn.close()
        return True

    @classmethod
    def get_string_cache(cls, k, to_json=True, conn=None):
        """
            查询 string 类型缓存数据, 并进行类型转换
        :param k:
        :param to_json:
        :param conn:
        :return:
        """
        if conn is None:
            conn = cls.get_redis()

        result = conn.get(k)
        conn.close()

        if isinstance(result, bytes):
            result = result.decode('utf-8')

        if to_json and result:
            try:
                _result = json.loads(result)
                if isinstance(_result, dict):
                    _items = _result.get('items')
                    if _items and isinstance(_items, list):
                        _result['items'] = [AttrDict(it) for it in _items]
                    return AttrDict(_result)
                elif isinstance(_result, list):
                    if isinstance(_result[0], dict):
                        return [AttrDict(it) for it in _result]
                return _result
            except Exception as e:
                logger.exception(e)
                logger.error('该错误已忽略')
                # 非JSON 格式的数据, 直接返回
                return result
        return result

    @classmethod
    def set_hash_cache(cls, k, mapping, ex=None, conn=None):
        if conn is None:
            conn = cls.get_redis()

        conn.hset(k, mapping=mapping)
        conn.expire(k, ex or cls.cfg_class.REDIS_SHORT_EXPIRE)
        return True

    @classmethod
    def set_hash_item_cache(cls, name, k, v, conn=None):
        if conn is None:
            conn = cls.get_redis()

        conn.hset(name, key=k, value=v)
        return True

    @classmethod
    def get_hash_cache(cls, k, conn=None):
        if conn is None:
            conn = cls.get_redis()

        result = convert(conn.hgetall(k))

        return result

    @classmethod
    def get_hash_item_cache(cls, name, k, conn=None):
        if conn is None:
            conn = cls.get_redis()

        return convert(conn.hget(name, k))

    @classmethod
    def del_hash_item_cache(cls, k, attr_k, conn=None):
        if conn is None:
            conn = cls.get_redis()

        return conn.hdel(k, attr_k)

    @classmethod
    def get_hash_exist(cls, name, field, conn=None):
        if conn is None:
            conn = cls.get_redis()
        return convert(conn.hexists(name, field))

    @classmethod
    def del_key(cls, name, conn=None):
        if conn is None:
            conn = cls.get_redis()
        conn.delete(name)


redis_factory = RedisFactory
