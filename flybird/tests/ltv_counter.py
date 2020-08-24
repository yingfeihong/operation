# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: Yfh
"""
import pymongo
import time
from bson import ObjectId
from tool.time_change import timestamp_to_time, time_to_timestamp, time_add, time_add_detail


db = pymongo.MongoClient("s-bp1b263efa9a44e4-pub.mongodb.rds.aliyuncs.com:3717")
mycol = db["game"]
mycol.authenticate("gale", "Gale53489*&h!")


db2 = pymongo.MongoClient("47.97.219.39:27018")
mycol2 = db2["admindb"]
mycol2.authenticate("gale", "Gale53489*&h!")


# date_list = [1567353600 + i*24*60*60 for i in range(78)]
# result = []
# for i in date_list:
#     result.append({'date': timestamp_to_time(i), 'timestamp': i, 'channelName': 'appstore', 'gameName': '马赛克英雄'})
# mycol2['ltv_counter'].insert_many(result)

# result = []
# for i in mycol2['ltv_counter'].find():
#     role_list = []
#     for account in mycol['account_info'].find({'register_time':
#         {'$gte': i['timestamp'], '$lt': i['timestamp'] + 24*60*60}}):
#         role = mycol['role_data'].find_one({'user_id': str(account['_id'])})
#         if role:
#             role_list.append(str(role['_id']))
#     result.append({'role_list': role_list, 'counter_number': len(set(role_list)),
#                    'date': i['date'], 'counter_id': str(i['_id'])})
# mycol2['ltv_role'].insert_many(result)

#
# for i in mycol2['ltv_counter'].find():
#     range_number = int((time.time() - i['timestamp'])//86400)
#     obj = mycol2['ltv_role'].find_one({'counter_id': str(i['_id'])})
#     role_list = obj['role_list']
#     counter_number = obj['counter_number']
#     result = []
#     for j in range(range_number):
#         cash_price = 0
#         for cash in mycol['cash_purchase_order'].find({'status': 2, 'purchase_time':
#             {'$gte': i['timestamp'] + j*86400, '$lt': i['timestamp'] + j*86400 + 86400},
#                                                        'role_id': {'$in': role_list}}):
#             cash_price += cash['price']
#         result.append(cash_price)
#     time.sleep(30)
#     result_finally = []
#     for h in range(len(result)):
#         if counter_number != 0:
#             nu = sum((result[0: h + 1]))
#             nu = nu / float(counter_number)
#             result_finally.append(nu)
#     print result_finally
#     mycol2['ltv_counter'].update_one({'_id': i['_id']}, {'$set': {'ltv_list': result_finally}})


# from app.constant.admin import CHANNEL_LIST
# date_list = [1571155200 + i*24*60*60 for i in range(35)]
# result = []
# for i in date_list:
#     for channel in CHANNEL_LIST:
#         result.append({'date': timestamp_to_time(i), 'timestamp': i, 'channelName': channel, 'gameName': '马赛克英雄'})
# mycol2['ltv_counter_android'].insert_many(result)

# result = []
# for i in mycol2['ltv_counter_android'].find():
#     role_list = []
#     for account in mycol['account_info'].find({'register_time':
#         {'$gte': i['timestamp'], '$lt': i['timestamp'] + 24*60*60}, 'channel_type_ex': i['channelName']}):
#         role = mycol['role_data'].find_one({'user_id': str(account['_id'])})
#         if role:
#             role_list.append(str(role['_id']))
#     result.append({'role_list': role_list, 'counter_number': len(set(role_list)),
#                    'date': i['date'], 'counter_id': str(i['_id'])})
# mycol2['ltv_role_android'].insert_many(result)
# print 'ok'


# for i in mycol2['ltv_counter_android'].find():
#     range_number = int((time.time() - i['timestamp'])//86400)
#     obj = mycol2['ltv_role_android'].find_one({'counter_id': str(i['_id'])})
#     role_list = obj['role_list']
#     counter_number = obj['counter_number']
#     result = []
#     for j in range(range_number):
#         cash_price = 0
#         for cash in mycol['cash_purchase_order'].find({'status': 2, 'purchase_time':
#             {'$gte': i['timestamp'] + j*86400, '$lt': i['timestamp'] + j*86400 + 86400},
#                                                        'role_id': {'$in': role_list}}):
#             cash_price += cash['price']
#         result.append(cash_price)
#     result_finally = []
#     if counter_number != 0:
#         for h in range(len(result)):
#             nu = sum((result[0: h + 1]))
#             nu = nu / float(counter_number)
#             result_finally.append(nu)
#     print result_finally
#     mycol2['ltv_counter_android'].update_one({'_id': i['_id']}, {'$set': {'ltv_list': result_finally}})