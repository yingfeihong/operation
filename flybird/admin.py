# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: QL Liu
"""
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options

from config.server_config import ServerConfig
from core.init.admin_init import AdminServerInit
from base.log.log_manager import LogManager as Log


define("CONFIG", default='local', help="Config Name", type=str)
define("PORT", default='1000', help="Server Port", type=str)


# 入口函数
if __name__ == '__main__':
    # 处理传入参数
    options.parse_command_line()
    # 初始化
    AdminServerInit.init(options.CONFIG)
    if options.PORT == '1000':
        options.PORT = ServerConfig.get_server_info(section='AdminServer', field='port')
    Log.logger.info("Config:%s  Port:%s listening......", options.CONFIG, options.PORT)
    # 监听端口，启动http server
    HTTPServer(AdminServerInit.get_handler_list()).listen(options.PORT)
    IOLoop.instance().start()
