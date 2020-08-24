# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: QL Liu
"""

import re
from base.log.log_manager import LogManager as Log
from base.db.db_manager import DBManager
import datetime
from app.constant.admin import MSK_GAME
from app.constant.admin import APP_STORE
from app.constant.admin import CHANNEL_MAP_FOR_ANDROID


# cmd ：6
def index_time(data):
    #  传参展示数据
    Log.logger.info('data:%s' % data)
    if data:
        if data['gameName'] == u'马赛克英雄':
            del data['gameName']
            Log.logger.info('data having')
            in_list = []
            default = 0
            for key,values in data.items():
                in_list.append((key, values))
            data2 = {}
            Log.logger.info('in_list:%s' % in_list)
            # 前端必须传入时间
            for da_ta in in_list:
                if da_ta[0] == 'channel_type':
                    default = 1
                    data2['channel_type'] = da_ta[1]
                else:
                    data2[da_ta[0]] = da_ta[1]
            Log.logger.info('data2:%s' % data2)
            if default == 0 or data['channel_type'] == APP_STORE:
                orders_info = DBManager.get_multi_record('ios_time', 'admindb', data2)
            else:
                print data2
                orders_info = DBManager.get_multi_record('android_time', 'admindb', data2)
            result_list = []
            print data2
            for order in orders_info:
                del order['_id']
                result_list.append(order)
        else:
            in_list = []
            for key, values in data.items():
                in_list.append((key, values))
            data2 = {}
            Log.logger.info('in_list:%s' % in_list)
            for da_ta in in_list:
                if da_ta[0] == 'channel_type':
                    data2[da_ta[0]] = re.compile(da_ta[1])
                else:
                    data2[da_ta[0]] = da_ta[1]
            Log.logger.info('data2:%s' % data2)
            orders_info = DBManager.get_multi_record('admin_time_data', 'admindb', data2)
            result_list = []
            for order in orders_info:
                del order['_id']
                result_list.append(order)

    #  默认数据
    else:
        Log.logger.info('data none')
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        data = {'date': now_time}
        orders_info = DBManager.get_multi_record('ios_time', 'admindb', data)
        result_list = []
        for order in orders_info:
            del order['_id']
            result_list.append(order)

    return {'data': result_list}
