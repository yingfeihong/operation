# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: Yfh
"""
from concurrent.futures import ThreadPoolExecutor

from common.constant.constant_host import HOST_LIST
from core.main_task import task


def manager():
    pool = ThreadPoolExecutor(10)
    for host in HOST_LIST:
        pool.submit(task, host)


if __name__ == '__main__':
    manager()
