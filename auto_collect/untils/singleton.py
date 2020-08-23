# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: Yfh
"""
import threading


class Singleton(object):
    """
    线程安全单例
    """
    instance = None
    lock = threading.RLock()

    def __init__(self):
        pass
    
    def __new__(cls, *args, **kwargs):
        with cls.lock:
            if not cls.instance:
                cls.instance = object.__new__(cls)
            return cls.instance
