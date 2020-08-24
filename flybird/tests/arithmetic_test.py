# -*- coding:utf-8 -*-
"""
Module Description:
Date:
Author: Yfh
"""

import random


def do_list_date(arr_a, arr_b):
    """
    one
    :param arr_a:
    :param arr_b:
    :return: result
    """
    result = []
    for array in arr_a:
        if array not in arr_b:
            result.append(array)
    return result


def goat_list_date():
    """
    second
    :return: result
    """
    start_list = [0, 1]*16
    random.shuffle(start_list)
    del start_list[6]


if __name__ == '__main__':
    goat_list_date()
