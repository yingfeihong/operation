# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: QL Liu
"""

from base.log.log_manager import LogManager as Log
from base.db.db_manager import DBManager
import datetime


# cmd ：8
def index_increase(data):
    #  传参展示数据
    Log.logger.info('data:%s' % data)
    print data
    if data:
        Log.logger.warning('data having')
        in_list = []
        for key, values in data.items():
            in_list.append((key, values))
        data2 = {}
        Log.logger.warning('in_list:%s' % in_list)
        for da_ta in in_list:
            if da_ta[0] == 'gmtCreate':
                data2[da_ta[0]] = {"$gte": da_ta[1][0], "$lte": da_ta[1][1]}
            elif da_ta[0] == 'gmtFinish':
                data2[da_ta[0]] = {'gmtFinish': {'$gte': da_ta[1][0], '$lte': da_ta[1][1]}}
            else:
                data2[da_ta[0]] = da_ta[1]
        Log.logger.warning('data2:%s' % data2)
        orders_info = DBManager.get_multi_record('paydata', data2)
        result_list = []
        for order in orders_info:
            del order['_id']
            result_list.append(order)
    #  默认数据
    else:
        Log.logger.warning('data none')
        now_time = datetime.datetime.now()
        seven_day_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        data = {'gmtCreate': {"$lte": now_time, '$gte': seven_day_ago}}
        orders_info = DBManager.get_multi_record('paydata', data)
        result_list = []
        for order in orders_info:
            del order['_id']
            result_list.append(order)

    return {'data': result_list}
