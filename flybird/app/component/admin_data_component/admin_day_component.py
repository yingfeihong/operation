# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: QL Liu
"""
import datetime
import re
from app.constant.admin import APP_STORE
from base.log.log_manager import LogManager as Log
from base.db.db_manager import DBManager
from app.constant.admin import ANDROID


# cmd ：5
def index_day(data):
    #  传参展示数据
    if data:
        if data['gameName'] == u'马赛克英雄':
            del data['gameName']
            result_list = []
            data2 = {}
            in_list = []
            default = 0
            for key, values in data.items():
                in_list.append((key, values))
            for da_ta in in_list:
                if da_ta[0] == 'date':
                    data2[da_ta[0]] = {"$gte": da_ta[1][0], "$lte": da_ta[1][1]}
                elif da_ta[0] == 'channel_type':
                    default = 1
                    if da_ta[1] == ANDROID:
                        pass
                    else:
                        data2['channel_type'] = da_ta[1]
                else:
                    data2[da_ta[0]] = da_ta[1]
            if default == 0 or data['channel_type'] == APP_STORE:
                accounts = DBManager.get_multi_record('ios_day_data', 'admindb', data2)
            else:
                accounts = DBManager.get_multi_record('android_day_data', 'admindb', data2)
            for account in accounts:
                del account['_id']
                result_list.append(account)
        else:
            Log.logger.info('data having')
            in_list = []
            for key, values in data.items():
                in_list.append((key, values))
            data2 = {}
            Log.logger.info('in_list:%s' % in_list)
            for da_ta in in_list:
                if da_ta[0] == 'date':
                    # 如果传了起始和结束时间
                    if len(da_ta[1]) > 1:
                        data2[da_ta[0]] = {"$gte": da_ta[1][0], "$lte": da_ta[1][1]}
                    # 只传了开始时间，只显示当天
                    else:
                        data2[da_ta[0]] = da_ta[1][0]
                elif da_ta[0] == 'channel_type':
                    data2[da_ta[0]] = re.compile(da_ta[1])
                else:
                    data2[da_ta[0]] = da_ta[1]
            Log.logger.info('data2:%s' % data2)
            orders_info = DBManager.get_multi_record('admin_day_data','admindb', data2)
            result_list = []
            for order in orders_info:
                del order['_id']
                result_list.append(order)
    #  默认数据
    else:
        Log.logger.info('data none')
        now_time = datetime.datetime.now()
        seven_day_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        data = {'date': {"$lte": now_time.strftime('%Y-%m-%d'), '$gte': seven_day_ago.strftime('%Y-%m-%d')}}
        # 查询不同的表数据
        orders_info = DBManager.get_multi_record('admin_day_data', 'admindb', data)
        result_list = []
        for order in orders_info:
            del order['_id']
            result_list.append(order)

    return {'data': result_list}

