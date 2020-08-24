# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: Yfh
"""
import pymongo
from bson import ObjectId

db = pymongo.MongoClient("47.97.219.39:27017")
my_col = db["game"]
my_col.authenticate("gale", "Gale53489*&h!")
all_cash = my_col['cash_purchase_order'].find({'status': 2})
uid_list = []
for cash in all_cash:
    uid_list.append(cash['role_id'])
print len(uid_list)
uid_list = list(set(uid_list))
print len(uid_list)
result = []
for role_id in uid_list:
    twd_price = 0
    hkd_price = 0
    diamond = 0
    role = my_col['role_data'].find_one({'_id': ObjectId(role_id)})
    account = my_col['account_info'].find_one({'_id': ObjectId(role['user_id'])})
    for cash in my_col['cash_purchase_order'].find({'status': 2, 'role_id': role_id}):
        if cash['ency'] == 'TWD':
            twd_price += cash['price']
            if cash['product_id'] == 1:
                diamond += 66*3
            elif cash['product_id'] == 2:
                diamond += 260*3
            elif cash['product_id'] == 3:
                diamond += 860*3
            elif cash['product_id'] == 4:
                diamond += 1780*3
            elif cash['product_id'] == 5:
                diamond += 2980*3
            elif cash['product_id'] == 6:
                diamond += 5980*3
            elif cash['product_id'] == 7:
                diamond += 300*3
            elif cash['product_id'] == 20:
                diamond += 150*3
            elif cash['product_id'] == 21:
                diamond += 600*3
            else:
                pass
        elif cash['ency'] == 'HKD':
            hkd_price += cash['price']
            if cash['product_id'] == 1:
                diamond += 66 * 3
            elif cash['product_id'] == 2:
                diamond += 260 * 3
            elif cash['product_id'] == 3:
                diamond += 860 * 3
            elif cash['product_id'] == 4:
                diamond += 1780 * 3
            elif cash['product_id'] == 5:
                diamond += 2980 * 3
            elif cash['product_id'] == 6:
                diamond += 5980 * 3
            elif cash['product_id'] == 7:
                diamond += 300 * 3
            elif cash['product_id'] == 20:
                diamond += 150 * 3
            elif cash['product_id'] == 21:
                diamond += 600 * 3
            else:
                pass
        else:
            print cash['ency']
    data = {'uid': account['uid'], 'twd_price': twd_price,
            'hkd_price': hkd_price, 'diamond': diamond, 'get_status': False}
    print data
    result.append(data)
# my_col['xiaomi_rebate'].insert_many(result)


