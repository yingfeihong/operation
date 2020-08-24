# -*- coding: utf-8 -*-

""" 通信协议
"""


class Protocol(object):
    """ 通信协议
    """
    # 后台
    create_account = r"/admin/account/create"
    login = r"/admin/login"
    refresh_token = r"/admin/token/refresh"
    index = r"/admin/index"
    ad_status = r"/ad/status"
    update_client = r'/client/update'
    update_prod_client = r'/prod/client/update'
    update_outside_client = r'/outside/client/update'
    update_server = r'/server/update'
    update_prod_server = r'/prod/server/update'
    super_admin = r'/super/admin'














