# -*- coding: utf-8 -*-

""" 工具类: 时间和日期

"""
import time
from datetime import datetime
from datetime import timedelta


def generate_time_list(interval, num):
    """
    生成多个固定间隔的时间点
    :param interval: 单位分钟
    :param num: 生成num个时间点
    :return:
    """
    time_list = []
    now_time = datetime.now()

    next_time = now_time
    for i in range(num):
        time_list.append(next_time)
        next_time += timedelta(minutes=interval)

    return time_list


def get_latest_timestamp(now_time, time_list):
    """
    获取最近的时间点
    :param now_time:
    :param time_list:
    :return:
    """
    length = len(time_list)
    latest_timestamp = time_list[length - 1]  # 设置默认值

    # 如果now_time_str大于所有的时间，则返回默认值
    if now_time >= time_list[length-1]:
        return latest_timestamp

    tmp = 0
    index = 1
    for timestamp in time_list:  # timestamp_list有序
        if now_time < time_list[index]:
            tmp = time_list[index-1]
            break

        index += 1

    latest_timestamp = tmp

    return latest_timestamp


def get_next_timestamp(time_list, now_time):
    """
    获取下一个刷新时间
    :param time_list:
    :param now_time:
    :return:
    """
    next_refresh_time = {}

    length = len(time_list)
    timestamp = get_latest_timestamp(now_time, time_list)
    index = time_list.index(timestamp)

    if index != length - 1:  # 如果不是今天最后一个刷新时间点
        next_refresh_time = time_list[index + 1]
    elif index == length - 1:  # 如果是今天最后一个刷新时间点
        next_refresh_time = time_list[0] + timedelta(days=1)  # 获取明天的第一个时间

    return next_refresh_time


def is_refresh_today(now_time, server_start_date, days_interval):
    """
    判断今天是否需要刷新
    :param now_time:
    :param server_start_date:
    :param days_interval:
    :return:
    """

    is_refresh = 0

    # 如果days_interval为-1，表示每天都刷，
    if days_interval == -1:
        is_refresh = 1
        return is_refresh

    time_delta = now_time - server_start_date
    days = time_delta.days

    # print "is_refresh_today()...", days, days_interval
    days_interval += 1  # 间隔天数，需要加1
    if days % days_interval == 0:
        is_refresh = 1

    return is_refresh


def get_today_start_date(now_time):
    """
    获取服务器启动日期. 用于多个需要刷新机制的系统。备注: 启动日期的时和分设置为0点0分0秒
    :param now_time:
    :return:
    """
    year = now_time.year
    month = now_time.month
    day = now_time.day

    hour = 0   # 设置为启动当天的0点0分0秒
    minute = 0
    second = 0

    time_str = str(year) + "-" + str(month) + "-" + str(day) \
               + " " + str(hour) + ":" + str(minute) + ":" + str(second)

    timestamp = time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S'))
    server_start_date = datetime.fromtimestamp(timestamp)

    return server_start_date


def hour_minute_str_to_time_dict(hour_minute_str, now_time):
    """
    时间_分钟字符串(例如"09:10")，转换为字典格式 ，包含时间格式的全部信息
    :param hour_minute_str:
    :param now_time:
    :return:
    """
    time_dict = {}

    # hour_minute_str为空， 直接返回空字典
    if not hour_minute_str:
        return time_dict

    tmp_list = hour_minute_str.split("_")
    hour = int(tmp_list[0])
    minute = int(tmp_list[1])

    time_dict["hour"] = hour
    time_dict["minute"] = minute

    # 添加日期,使之包含时间格式的所有信息
    time_dict["year"] = now_time.year
    time_dict["month"] = now_time.month
    time_dict["day"] = now_time.day

    return time_dict


def time_dict_to_format_time(time_dict):
    """
    获取标准时间格式
    :param time_dict:
    :return:
    """
    hour = time_dict["hour"]
    minute = time_dict["minute"]
    second = 0

    year = time_dict["year"]
    month = time_dict["month"]
    day = time_dict["day"]

    time_str = str(year) + "-" + str(month) + "-" + str(day)\
               + " " + str(hour) + ":" + str(minute) + ":" + str(second)

    timestamp = time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S'))

    format_time = datetime.fromtimestamp(timestamp)

    return format_time


def convert_to_time_dict(format_time):
    """
    获取自定义的时间字典time_dict
    :param format_time:
    :return:
    """
    time_dict = {"hour": format_time.hour
        , "minute": format_time.minute
        , "microsecond": format_time.microsecond
        , "year": format_time.year
        , "month": format_time.month
        , "day": format_time.day}

    return time_dict


def convert_to_format_time(time_str):
    """
    时间转换
    :param time_str:
    :return:
    """
    tmp_list = time_str.split(".")
    time_str = tmp_list[0]

    timestamp = time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S'))
    format_time = datetime.fromtimestamp(timestamp)

    return format_time


def get_zero_clock_timestamp():
    """
    获取0点的时间戳
    :return:
    """
    t = time.localtime(time.time())
    zero_clock_time = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t), '%Y-%m-%d %H:%M:%S'))
    return long(zero_clock_time)