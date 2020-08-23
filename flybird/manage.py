# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: Yfh
"""
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options

from core.init.app_init import AdminServerInit

define("CONFIG", default='local', help="Config Name", type=str)
define("PORT", default='8888', help="Server Port", type=str)


# 入口函数
if __name__ == '__main__':
    # 处理传入参数
    options.parse_command_line()
    # 初始化
    app = AdminServerInit(options.CONFIG)
    # Log.logger.info("Config:%s  Port:%s listening......", options.CONFIG, options.PORT)
    # 监听端口，启动http server
    HTTPServer(AdminServerInit.get_handler_list()).listen(options.PORT)
    IOLoop.instance().start()
