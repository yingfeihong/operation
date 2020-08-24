# -*- coding: utf-8 -*-

""" 全局定义
"""

IGNORE_PROTOCOL_LIST = [r"/admin/login",
                        # r"/admin/index",
                        r"/admin/account/create",
                        r"/admin/token/refresh"]  # 忽略的协议列表
TOKEN_SECRET_KEY = "NGHH%$**5678&"
ACCESS_TOKEN_EXPIRATION = 3600 * 2  # 过期时间2小时
REFRESH_TOKEN_EXPIRATION = 15 * 24 * 60 * 60  # 刷新token过期时间15天





