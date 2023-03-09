import json
import aioredis

from sanic.log import logger
from attrdict import AttrDict


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
    _redis = None
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
    def connecting(cls):

        if not cls.redis_url:
            raise ValueError('redis_module 模块, 请先调用 from_config 进行初始化')

        # with lock:
        if cls._redis is None:
            cls._redis = aioredis.from_url(cls.redis_url)
        return cls._redis

    # @classmethod
    # async def get_redis(cls, pool=None):
    #     if not pool:
    #         pool = cls.load_pool()
    #     return aioredis.Redis(connection_pool=pool)

    @classmethod
    async def set_string_cache(cls, k, v, ex=None, redis=None):
        """
            设置 string 类型缓存设置, 并添加过期时间
        :param k:
        :param v:
        :param ex:
        :param redis:
        :return:
        """
        if redis is None:
            redis = await cls.connecting()

        if not isinstance(v, str):
            v = json.dumps(v)

        await redis.set(k, v, ex or cls.cfg_class.REDIS_SHORT_EXPIRE)
        return True

    @classmethod
    async def get_string_cache(cls, k, to_json=True, redis=None):
        """
            查询 string 类型缓存数据, 并进行类型转换
        :param k:
        :param to_json:
        :param redis:
        :return:
        """
        if redis is None:
            redis = await cls.connecting()

        result = await redis.get(k)

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
    async def set_hash_cache(cls, k, mapping, ex=None, redis=None):
        if redis is None:
            redis = cls.connecting()

        await redis.hset(k, mapping=mapping)
        await redis.expire(k, ex or cls.cfg_class.REDIS_SHORT_EXPIRE)
        return True

    @classmethod
    async def get_hash_cache(cls, k, redis=None):
        if redis is None:
            redis = await cls.connecting()

        result = convert(await redis.hgetall(k))

        return result

    @classmethod
    async def get_hash_item_cache(cls, name, k, redis=None):
        if redis is None:
            redis = await cls.connecting()

        return convert(await redis.hget(name, k))

    @classmethod
    async def del_hash_item_cache(cls, k, attr_k, redis=None):
        if redis is None:
            redis = await cls.connecting()

        return await redis.hdel(k, attr_k)

    @classmethod
    async def get_hash_exist(cls, name, field, redis=None):
        if redis is None:
            redis = await cls.connecting()
        return convert(await redis.hexists(name, field))

    @classmethod
    async def del_key(cls, name, redis=None):
        if redis is None:
            redis = await cls.connecting()
        await redis.delete(name)


redis_factory = RedisFactory
