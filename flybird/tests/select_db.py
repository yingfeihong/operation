# -*- coding:utf-8 -*-

import pymongo
import datetime
#
# list_all = []
db = pymongo.MongoClient(["47.97.219.39:27117"])
mydb = db["game"]
mydb.authenticate("gale", "Gale53489*&h!")
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# mydbname = client['admindb']
a = 0
for i in mydb['t1_cash_purchase_order'].find({'channel_type': 11, 'status': 2}):
    a += i['price']
print a
# for i in mydb['battle_error_data'].find():
#     mydbname['battle_error_data_android'].insert_one(i)
# print 'ok'
# # client = pymongo.MongoClient("mongodb://localhost:27017/")
# mydbname = client['android_test']
#
# for x in mydb['cash_purchase_order'].find():
#     if mydbname['role_data'].find_one({'_id':x['role_id']}):
#         print 'ok',x['role_id'],mydbname['role_data'].find_one({'_id':x['role_id']})['_id']
#
#     else:
#         print 123456789

#
# for i in mydb['cash_purchase_order'].find():
#     print 1
#     mydbname['android_cash_purchase_order'].insert_one(i)


# for x in mydb['account_info'].find():
#     print 1
#     role = mydb['role_data'].find_one({'user_id':str(x['_id'])})
#     if role:
#         list_all.append({
#             'account':x['account'],
#             'uid':x['uid'],
#             'channel_type_ex':x['channel_type_ex'],
#             'role_name':role['role_name'],
#             'cumulative_recharge':role['cumulative_recharge'],
#         })
#
# print len(list_all)
# print list_all
#
# mycol['admin_static'].insert_many(list_all)
#
# print 'over'


# list_a = []
# for x in mydb['role_data'].find():
#     cash = mydb['cash_purchase_order'].find({'role_id':str(x['_id']) ,'status': 2})
#     if cash:
#         a = 0
#         for y in cash:
#             a += y['price']
#     else:
#         a = 0
#     print a,x['cumulative_recharge']
#     if a!=x['cumulative_recharge']:
#         print {
#             'role':x['role_name'],
#             'cum':x['cumulative_recharge'],
#             'cash':a
#         }
#         list_a.append({
#             'role':x['role_name'],
#             'cum':x['cumulative_recharge'],
#             'cash':a
#         })
#
# print list_a


# a = 0
# for x in mydb['cash_purchase_order'].find({'status': 2}):
#     a += x['price']
#     print a


# mydbcol.delete_many({'cumulative_recharge':0})
# print 'ok'
import json
import requests
from tool.time_change import time_add_detail
# #
# #
# # def cq_account():
# #     url = 'https://m.lianhuigame.com//user/queryUser.json'
# #     now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# #     start_time = time_add_detail(now_time,-1)
# #     data = {'startDate': start_time, 'endDate': now_time}
# #     print data
# #     result = json.loads(requests.post(url, data=data).text)
# #     print result
# #
# # cq_account()


# def cq_pay():
#     now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     url = 'https://m.lianhuigame.com/pay/queryOrder.json'
#     data = {'startDate': '2019-09-25 00:00:00', 'endDate': now_time, 'type': 1}
#     print data
#     result = json.loads(requests.post(url, data=data).text)
#     print len(result['result'])
#     for i in result['result']:
#         print i
#     print data
#
#
# cq_pay()

# 传奇账户流水数据插入
# def cq_account():
#     url = 'https://m.lianhuigame.com/pay/queryOrder.json'
#     data = {'startDate': '2019-01-01 16:13:00', 'endDate': '2019-10-21 16:13:00', 'type': 1, 'gameId'}
#     result = requests.post(url, data).text
#     # result = json.loads(requests.post(url, data={'type': 1}).text)
#     print result


# cq_account()