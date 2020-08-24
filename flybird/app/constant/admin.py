# -*- coding:utf-8 -*-
"""
Module Description:
date 2019 - 1 - 2
author cy-h
"""
from util import enum

CHANNEL_TYPE = enum(APP_STORE='appstore', GALE_GAME='galegame', GAME_4399='ssjj', GAME_BILI='bilibili',
                    GAME_VIVO='vivo', GAME_XIAOMI='xiaomi', GAME_HUAWEI='huawei', GAME_TENCENT='tencent',
                    GAME_TAPTAP='taptap', GAME_OPPO='oppo', GAME_HAOYOU='haoyoukuaibao',
                    GAME_JIUWAN='jiuwan', GAME_UC='uc', GAME_BAIDU='baidu', GAME_YOUYUN='youyun', GAME_QIHOO='qihoo',
                    GAME_MEIZU='meizu', GAME_MAOZHUA='maozhua', GAME_MIGU='migu', DEVELOP='develop')

# 登录公告redis Key
LOGIN_ANNOUNCEMENT = "login:announcement"
MAINTENANCE_ANNOUNCEMENT = "maintenance:announcement"
ANNOUNCEMENT_FOR_LOGIN = '登陆公告'
ANNOUNCEMENT_FOR_MAINTAIN = '维护公告'
ANNOUNCEMENT_FOR_ROLL = '滚动公告'
SURPLUS_TIME = 15 * 24 * 60 * 60
REBATE_TIME = 90 * 24 * 60 * 60
MSK_GAME = '马赛克英雄'
APP_STORE = 'appstore'
ANDROID = 'android'
# 最大循环次数
MAX_CIRCULATE_NUM = 1000

SERVER_STATUS_KEY = "gate:server:status:{}"
# 发送对象
SEND_OBJECT = enum(MANY=1, ONE=0)
SET_STATUS = enum(OPEN=1, CLOSE=0)
BAN_TYPE = enum(SELECT=1, BAN=0)
STATUS_TYPE = enum(BAN=0, TALK=1)
ANNOUNCEMENT_TYPE = enum(ADD_LOGIN=0, ADD_MAINTENANCE=1, ADD_ROLL=5, SELECT=2, DELETE=3, ALTER=4)
EMAIL_TYPE = enum(SEND=0, DELETE=1, GET=2)
PAYMENT_STATUS = enum(PROCESSING=1, SUCCESS=2, FAIL=3)
RED_DOT_TIP = enum(DISPATCH=1, DAILY_TASK=2, EMAIL=3, ACHIEVEMENT=4)
CHANNEL_MAP = {'appstore': 'ios', 'android': 'android'}
CHANNEL_MAP_DB = {'appstore': 'iosgame', 'android': 'androidgame'}
IOS_GAME = 'iosgame'
ANDROID_GAME = 'androidgame'
CHANNEL_MAP_FOR_ANDROID = {
                              '4399': 'ssjj', 'B站': 'bilibili', 'OPPO': 'oppo',
                              'VIVO': 'vivo', '小米': 'xiaomi', '华为': 'huawei',
                              'UC': 'huawei', '百度': 'baidu', '魅族': 'meizu',
                              '360': 'qihoo', 'taptap': 'taptap', '好游快爆': 'haoyoukuaibao',
                              '猫爪': 'maozhua', '咪咕': 'migu', '应用宝': 'tencent',
                              '当乐网': 'danglewang', '拇指玩': 'mzw', '爱奇艺': 'iqiyi',
                              '搜狗': 'sogou', '葫芦侠': 'gourd', '虫虫助手': 'chong',
                              '木蚂蚁': 'mumayi'
                            }
CHANNEL_LIST = [
        'ssjj', 'bilibili', 'oppo', 'vivo',
        'xiaomi', 'huawei', 'uc', 'baidu',
        'meizu', 'qihoo', 'taptap', 'haoyoukuaibao',
        'maozhua', 'migu', 'yybsingle', 'danglewang',
        'mzw', 'iqiyi', 'sogou', 'gourd',
        'chong', 'mumayi', 'youyi', 'wufan', 'tianyuyou', 'youxifan'
    ]



