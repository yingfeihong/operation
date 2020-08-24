# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: QL Liu
"""
import tornado.web


class CorsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Credentials', 'false')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        self.set_header(
            'Access-Control-Allow-Headers',
            'x-requested-with, Authorization, '
            'Content-Type, Accept, Accept-Language,'
            ' Content-Language'
        )
        self.set_header('Access-Control-Allow-Methods',
                        'POST,GET,PUT,DELETE,OPTIONS')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()