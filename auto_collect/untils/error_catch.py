# -*- coding:utf-8 -*-
"""
Module Description:
Date:
Author: Yfh
"""
import traceback
import logging
from functools import wraps


def catch_error(func):
    """
    错误捕获

    >>> @catch_error
    >>> def func():
    >>>       pass
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            traceback.print_exc(e)
            logging.error("error is {}".format(e))
            # return None
    return wrapper


def catch_err_with_dft_rtn(default_rtn=None):
    """
    错误捕获,并可设置报错时的返回值

    >>> @catch_err_with_dft_rtn(default_rtn=3)
    >>> def func():
    >>>       pass

    :param default_rtn:报错时返回的值
    :return
    """
    def out_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                traceback.print_exc(e)
                return default_rtn
        return wrapper
    return out_wrapper
