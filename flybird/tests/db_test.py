# -*- coding:utf-8 -*-

from base.db.db_manager import DBManager
import time,datetime

#將字符串時間轉時間戳
def change_time(param):
    pass


def test_select():
    result = DBManager.get_record('t_cash_purchase_order',{'price':98})
    print result
    print result['_id']
    # id = result['_id']
    # print str(id)=='5c8a0c4ed0930f70a94f1a99'
    #
    # result2 = DBManager.get_multi_record('t_role_data',{'user_id':str(id)})
    # for i in result2:
    #     print i
    #     print 'success'
    #     id2 = i['_id']
    #     print id2
    #     result3 = DBManager.get_multi_record('t_cash_purchase_order',{'role_id':str(id2)})
    #     for j in result3:
    #         print j

# def test_db():
#     # now_time2 = datetime.datetime.now()
#     result = DBManager.get_multi_record('cash_purchase_order',{})
#     # result = DBManager.get_record('cash_purchase_order',{})
#     a = []
#     status_dic = {1:'进行中',2:'成功' ,3:'失败', 4:'等待校验'}
#     channel_type_dic = {1:'苹果',2:'galegame', 3:4399,4:'bilibili',5: 'vivo',6: '小米',7:'华为', 8:'应用宝' ,9:'taptap',
#                         10:'oppo',11:'好游快爆',12:'九玩聚合',1000:'自己',0:'未知','galegame':'galegame'}
#     c = 0
#     for i in result:
#         c+=1
#         print c
#         print i['channel_type']
#         print type(i['channel_type'])
#         a.append({
#             "gameName":'马赛克英雄',
#             "amount":i['price'],
#             # "payType":i['pay_type'],
#             "status":status_dic[i['status']],
#             "gmtCreate":i['purchase_time'],
#             "gmtFinish":i['purchase_time'],
#             "channelId":i['transaction_id'],
#             "channelName":channel_type_dic[i['channel_type']],
#             "userId":i['role_id'],
#             "orderNo":i['_id']
#         })
#     print a
#     print len(a)
#     for j in a:
#         DBManager.insert_record('admin_test_pay',j)