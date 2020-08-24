# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: QL Liu
"""
from net_base import CorsHandler
from base.network.protocol import Protocol
from base.network.user_request import handle_request
from base.log.log_manager import LogManager as Log
from base.db.redis_manager import RedisManager


class AdminRouter(object):
    """ 协议映射类：后台
    """

    @staticmethod
    def add_handler(handler_list):
        """
        添加响应函数
        :param handler_list:
        :return:
        """
        handler_list.append((Protocol.login, AdminHandler))
        handler_list.append((Protocol.create_account, AdminHandler))
        handler_list.append((Protocol.refresh_token, AdminHandler))
        handler_list.append((Protocol.index, AdminIndex))
        handler_list.append((Protocol.ad_status, AdStatus))
        handler_list.append((Protocol.update_client, ExcuteShellCommand))
        handler_list.append((Protocol.update_prod_client, ExcuteProdClientCommand))
        handler_list.append((Protocol.update_server, ExcuteUpdateServerCommand))
        handler_list.append((Protocol.update_prod_server, ExcuteUpdateProdServerCommand))
        handler_list.append((Protocol.update_outside_client, ExcuteOutsideProdClientCommand))


class AdminHandler(CorsHandler):

    def post(self):
        Log.logger.info('request: AdminHandler -- POST')
        handle_request(self)

    def get(self, *args, **kwargs):
        self.write('登陆  ')
        # Log.logger.warning('request: AdminHandler -- GET')
        # cmd = int(self.get_query_argument('cmd'))
        # handle_request(self, dict(cmd=cmd), False)


class AdminIndex(CorsHandler):

    def post(self):
        Log.logger.info('request: AdminIndex -- POST')
        handle_request(self)

    def get(self, *args, **kwargs):
        self.write('跳转登录')
        # Log.logger.warning('request: AdminIndex -- GET')
        # cmd = int(self.get_query_argument('cmd'))
        # handle_request(self, dict(cmd=cmd), False)


class ExcuteShellCommand(CorsHandler):

    def get(self):
        import os
        cmd1 = 'cd /root/vue-admin'
        cmd2 = 'svn up'
        cmd3 = '/usr/local/nginx/sbin/nginx -s reload'
        cmd = cmd1 + '&&' + cmd2 + '&&' + cmd3
        os.system(cmd)
        self.write('update ok')


class ExcuteProdClientCommand(CorsHandler):
    def get(self):
        import os
        cmd1 = 'cd /root/prod-admin'
        cmd2 = 'svn up'
        cmd3 = '/usr/local/nginx/sbin/nginx -s reload'
        cmd = cmd1 + '&&' + cmd2 + '&&' + cmd3
        os.system(cmd)
        self.write('update ok')


class ExcuteOutsideProdClientCommand(CorsHandler):
    def get(self):
        import os
        cmd1 = 'cd /root/outside-admin'
        cmd2 = 'svn up'
        cmd3 = '/usr/local/nginx/sbin/nginx -s reload'
        cmd = cmd1 + '&&' + cmd2 + '&&' + cmd3
        os.system(cmd)
        self.write('update ok')


class ExcuteUpdateServerCommand(CorsHandler):

    def get(self):
        import os
        cmd1 = 'cd /root/admin_server'
        cmd2 = 'svn up'
        cmd3 = 'supervisorctl restart baozi:admin-develop baozi:cron-develop baozi:email-develop'
        cmd = cmd1 + '&&' + cmd2 + '&&' + cmd3
        self.write('server update ok')
        os.system(cmd)


class ExcuteUpdateProdServerCommand(CorsHandler):

    def get(self):
        import os
        cmd1 = 'cd /root/admin_server'
        cmd2 = 'svn up'
        cmd3 = 'supervisorctl restart baozi:admin-prod baozi:cron-prod baozi:email-prod baozi:android-email-prod '
        cmd = cmd1 + '&&' + cmd2 + '&&' + cmd3
        self.write('server update ok')
        os.system(cmd)


class AdStatus(CorsHandler):
    def get(self):
        status = self.get_argument('status')
        if status == 'open':
            RedisManager.ios_r.set('ad:status', 1)
            self.write('open')
        else:
            RedisManager.ios_r.delete('ad:status')
            self.write('close')




