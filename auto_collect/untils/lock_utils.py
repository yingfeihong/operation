# -*- coding:utf-8 -*-
"""
Module Description:
Date:
Author: Yfh
"""
from redlock import RedLock
DEFAULT_DELAY = 1


class Mutex(RedLock):
    """ 单纯的 key 锁定，一般用于锁行为或业务逻辑 """
    def __init__(self, key, connection_details, delay_sec=DEFAULT_DELAY):
        if not key:
            raise ValueError('Mutex Key Invalided!')
        RedLock.__init__(self, key, retry_delay=delay_sec, connection_details=connection_details)
