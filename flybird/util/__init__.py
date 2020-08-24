# -*- coding:utf-8 -*-

# 这里用来记录一些全局性质的工具方法


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


def enum_to_dict(enum):
    """
    将上面的enum转换为dict字典
    :param enum:枚举实例
    :return:dict
    """
    enum_k = [k for k in dir(enum) if k[:2] != '__']
    return {k: getattr(enum, k) for k in enum_k}


def dict_to_enum(dict):
    return type('Enum', (), dict)
