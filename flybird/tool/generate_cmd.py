# -*- coding:utf-8 -*-
"""
Module Description:
Date: 2018-7-26
Author: QL Liu
"""
# 后台 1 ~ 1999
# 账户 2000 ~ 2999
# 网关 3000 ~ 3499
# 用户 3500 ~ 3999
# 充值 4000 ~ 4499
# 漫画 4500 ~ 5499

import json
import os


CMD_LIST = {
    # 后台
    "CreateAccount": 1, # 創建用戶 cmd
    "Login": 2,  # 登陸cmd
    "RefreshToken": 3, # 刷新token cmd
    "IndexPay": 4, # 支付數據請求cmd
    "IndexDay": 5, # 日數據請求cmd
    "IndexTime": 6, # 實時數據請求cmd
    "IndexLtv": 7, # ltv數據請求cmd
    "IndexIncrease": 8, # 新增用戶數據請求cmd
    "IndexRebate": 9, # 返利数据请求
    "SuperAdmin": 10, # 超级管理员创建用户
    "Leave": 12, # 留存数据获取接口
    "Dau": 13, # dau数据获取接口
    "Announcement": 15, # 公告管理
    "Email": 16, # 邮件管理
    "Banned": 17,  # 禁言管理
    "ServerStatusSet": 18,  # 服务器设置
    "BattleError": 19  #

}


if __name__ == "__main__":
    temp_list = {}
    for key, cmd in CMD_LIST.items():
        temp_list[key] = cmd

    temp_data = json.dumps(temp_list)
    cmd_path = os.path.join(os.path.dirname(os.getcwd()), 'doc/cmd/cmd.json')
    fo = open(cmd_path, 'w')
    fo.write(temp_data)
    fo.close()
