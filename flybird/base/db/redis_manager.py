# -*- coding:utf-8 -*-
"""
Module Description: Redis管理类
Date: 2018-1-24
Author: QL Liu
"""
from redis import StrictRedis, ConnectionPool
from json import dumps, loads
from config.server_config import ServerConfig
from util.error_catch import catch_error
from base.log.log_manager import LogManager as Log


class RedisManager(object):

    r = None
    ios_r = None
    android_r = None

    def __init__(self):
        for redis_name in ['RedisServer', 'IosRedis', 'AndroidRedis']:
            ip, port, password, db, auth, max_connections = self.get_redis_config(redis_name)
            Log.logger.info("redis, ip:{}, port:{}, db:{}, "
                            "password:{}, auth:{}, max_connections:{}".format(ip, port,
                                                                              db, password,
                                                                              auth, max_connections))
            if redis_name == 'AndroidRedis':
                RedisManager.android_r = RedisManager.connect_redis(ip, port, db, password, auth)
            elif redis_name == 'IosRedis':
                RedisManager.ios_r = RedisManager.connect_redis(ip, port, db, password, auth)
            else:
                RedisManager.r = RedisManager.connect_redis(ip, port, db, password, auth)

    @staticmethod
    def connect_redis(ip, port, db, password, auth):
        if auth:
            pool = ConnectionPool(host=ip, port=port, db=db, password=password)
        else:
            pool = ConnectionPool(host=ip, port=port, db=db)
        return StrictRedis(connection_pool=pool, decode_responses=True)

    @staticmethod
    def get_redis_config(redis_name):
        """
        获取redis信息
        :return:
        """
        ip = ServerConfig.get_server_info(redis_name, "ip")
        port = ServerConfig.get_server_info(redis_name, "port")
        password = ServerConfig.get_server_info(redis_name, "password")
        db = ServerConfig.get_server_info(redis_name, "db")
        auth = ServerConfig.get_server_info(redis_name, "auth", "boolean")
        max_connections = ServerConfig.get_server_info(redis_name, "max_connections", "int")
        return ip, port, password, db, auth, max_connections

    @classmethod
    def cache_set(cls, key, value, expire=None, r_type='default'):
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        type_map.get(r_type).set(key, dumps(value), ex=expire)

    @classmethod
    def get_cache(cls, key, r_type='default'):
        try:
            type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
            json_value = type_map.get(r_type).get(key)
            value = loads(json_value)
        except Exception as e:
            Log.logger.error("get redis key:{}, error is {}".format(key, e))
            return None
        return value

    @classmethod
    @catch_error
    def delete_keys(cls,  r_type='default', *keys):
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        type_map.get(r_type).delete(*keys)

    @classmethod
    @catch_error
    def delete_key(cls, key, r_type='default'):
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        type_map.get(r_type).delete(key)

    @classmethod
    @catch_error
    def get_keys(cls, pattern, r_type='default'):
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        return type_map.get(r_type).keys(pattern)

    @classmethod
    @catch_error
    def hash_set(cls, name, key, value, r_type='default'):
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        return type_map.get(r_type).hset(name, key, value)

    @classmethod
    @catch_error
    def hash_get(cls, name, key, r_type='default'):
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        return type_map.get(r_type).hget(name, key)

    @classmethod
    @catch_error
    def hash_get_all(cls, name, r_type='default'):
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        return type_map.get(r_type).hgetall(name)

    @classmethod
    @catch_error
    def hash_get_all_value(cls, name, r_type='default'):
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        return type_map.get(r_type).hvals(name)

    @classmethod
    @catch_error
    def hash_delete(cls, name, key, r_type='default'):
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        return type_map.get(r_type).hdel(name, key)

    @classmethod
    @catch_error
    def hash_get_all_key(cls, name, r_type='default'):
        """
        获取hash name下的所有key
        :param name:
        :param r_type:
        :return:
        """
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        return type_map.get(r_type).hkeys(name)

    @classmethod
    @catch_error
    def pipeline(cls, r_type='default'):
        """
        管道
        :return:
        """
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        return type_map.get(r_type).pipeline()

    @classmethod
    def add_to_rank(cls, rank_type, key, score, r_type='default'):
        """
        在榜单中新增一条数据，如果已存在，则覆盖旧的
        :param rank_type:
        :param key:
        :param r_type:
        :param score:
        :return:
        """
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        return type_map.get(r_type).zadd(rank_type, score, key)

    @classmethod
    def increase_rank(cls, rank_type, name, score, r_type='default'):
        """
        增加榜单中对应记录的分数
        :param rank_type:
        :param name:
        :param score:
        :param r_type:
        :return:
        """
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        return type_map.get(r_type).zincrby(rank_type, name, score)

    @classmethod
    def get_range(cls, rank_type, start=0, end=99, with_score=True, score_cast_func=int, r_type='default'):
        """
        获取start-end的排名
        :param rank_type:
        :param start:
        :param end:
        :param with_score:
        :param r_type:
        :param score_cast_func:
        :return:
        """
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        return type_map.get(r_type).zrevrange(rank_type, start, end, withscores=with_score, score_cast_func=score_cast_func)

    @classmethod
    def get_number(cls, rank_type, r_type='default'):
        """
        获取榜单总数量
        :param rank_type:
        :param r_type:
        :return:
        """
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        return type_map.get(r_type).zcard(rank_type)

    @classmethod
    def get_role_rank(cls, rank_type, key, r_type='default'):
        """
        获取玩家排名
        :param rank_type:
        :param key:
        :param r_type:
        :return:
        """
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        rank = type_map.get(r_type).zrevrank(rank_type, key)
        return rank if rank is None else rank + 1

    @classmethod
    def get_role_score(cls, rank_type, key, score_cast_func=int, r_type='default'):
        """
        获取某个玩家的分数
        :param rank_type:
        :param key:
        :param r_type:
        :param score_cast_func:
        :return:
        """
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        score = type_map.get(r_type).zscore(rank_type, key)
        return score_cast_func(score) if score else 0

    @classmethod
    def get_key_rank(cls, rank_type, key, r_type='default'):
        """
        获取某个key在榜单中的排名
        :param rank_type:
        :param key:
        :param r_type:
        :return:
        """
        type_map = {'ios': cls.ios_r, 'android': cls.android_r, 'default': cls.r}
        return type_map.get(r_type).zrevrank(rank_type, key)




