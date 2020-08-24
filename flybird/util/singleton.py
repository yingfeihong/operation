# -*- coding:utf-8 -*-
"""
Module Description: 单例
Date: 2018-3-16
Author: QL Liu
"""


class Singleton(type):
    """
    Singleton Metaclass
    """

    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls.instance = None

    def __call__(cls, *args):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args)
        return cls.instance
