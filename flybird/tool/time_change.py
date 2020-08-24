# -*- coding:utf-8 -*-

"""
转换时间模块
"""

import datetime
import time


def timestamp_to_time(target):
    """
    时间戳转时间
    :param target:
    :return:
    """
    dateArray = datetime.datetime.utcfromtimestamp(target)
    result = dateArray.strftime("%Y-%m-%d")
    # result = time_add(result, 1)
    return result


def time_to_timestamp(target):
    """
    时间转时间戳
    :param target:
    :return:
    """
    timeArray = time.strptime(target, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


# 日期加减
def time_add(date, target):
    """
    输入字符串日期加减（到日）
    :param date:
    :param target:
    :return:
    """
    date1 = datetime.datetime.strptime(date, "%Y-%m-%d")
    result = date1 + datetime.timedelta(days=target)
    result = result.strftime("%Y-%m-%d")
    return result


# 日期加减
def time_add_detail(date, target):
    """
    输入字符串日期加减（到秒）
    :param date:
    :param target:
    :return:
    """
    date1 = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    result = date1 + datetime.timedelta(days=target)
    result = result.strftime("%Y-%m-%d %H:%M:%S")
    return result

