# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: QL Liu
"""
import time
import sys
from share import action_status_code as code
from lang.chs import MESSAGE
from base.log.log_manager import LogManager as Log


class BaseAction(object):
    # 设置保存的日志最大长度，若为-1，则不限制
    LOG_LEN = -1

    def __init__(self, args):
        self.args = args
        self.request = {}
        self.response = {}
        self.error_code = 0

    def before(self):
        """
        前期处理参数校验之类
        :return:
        """
        return True

    def do(self):
        """
        处理业务
        :return:
        """
        return True

    def get(self, attr, default=None):
        return self.args.get(attr, default)

    def take(self):
        Log.logger.info("remote_ip:{}".format(self.args['remote_ip']))
        if not self.before():

            return {'status': code.ARGS_ERROR, 'message': '参数错误', 'data': {}}
        result = self.do()
        self.response_after(result)

        return self.response

    def response_after(self, response):
        """
        消息返回的处理
        :return:
        """
        if isinstance(response, dict):
            self.response['status'] = code.OK
            self.response['message'] = MESSAGE.get(code.OK)
            self.response['data'] = response
        else:
            if response is None:
                response = code.OK
            self.response['status'] = response
            self.response['message'] = MESSAGE.get(response)
            self.response['data'] = dict()

    def after(self):
        """
        处理完业务之后的处理
        :return:
        """
        return True

    def get_str(self, key, default=None):
        """
        字符串参数类型检验
        :param key:
        :param default:
        :return:
        """
        val = self.get(key, default)
        if val is None:
            return False

        if not isinstance(val, basestring):
            return False

        return True

    def get_float(self, key, default=None, min_float=0.0, max_float=9999999999.0):
        """
        float类型参数检验
        :param key:
        :param default:
        :param min_float:
        :param max_float:
        :return:
        """
        val = self.get(key, default)
        if val is None:
            return False

        if not isinstance(val, float):
            return False

        if val < min_float or val > max_float:
            return False

        return True

    def get_int(self, key, default=None, min_int=-sys.maxint, max_int=sys.maxint):
        """
        整型参数类型检验
        :param key:
        :param default:
        :param min_int:
        :param max_int:
        :return:
        """
        val = self.get(key, default)
        if val is None:
            return False

        if not isinstance(val, int):
            return False

        if val < min_int or val > max_int:
            return False
        return True

    def get_bool(self, key):
        """
        bool类型参数检验
        :param key:
        :return:
        """
        val = self.get(key)
        if val is None:
            return False

        if not isinstance(val, bool):
            return False
        return True


class LogAction(BaseAction):
    """
    增加日志
    """
    def __init__(self, args):
        BaseAction.__init__(self, args)
        self.begin_time = time.time()
        # end_time的实际赋值在返回给客户端后赋值
        self.end_time = time.time()

    def after(self):
        Log.logger.info("request_time:{}ms".format((self.end_time - self.begin_time)*1000))