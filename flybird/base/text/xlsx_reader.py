# -*- coding:utf-8 -*-
"""
Module Description:
Date: 2018-3-22
Author: QL Liu
"""
import re
import xlrd
from util.common_util import get_file_full_path


def load_config(file_name):
    """
    加载配置文件
    :param file_name:
    :return:
    """
    path = get_file_full_path(file_name)
    data = xlrd.open_workbook(path)
    sheet1 = data.sheet_by_index(0)
    nrows = sheet1.nrows
    row_type = sheet1.row_values(1)  # 对应xlsx表中的第二行数据：[int, string, intArray...] 表示各列的数据类型
    row_need = sheet1.row_values(2)  # 对应xlsx表中的第三行数据:[1, 0,...] 1:表示服务端需要
    idx = sheet1.row_values(0)  # 对应xlsx表中第一行数据: 字段名
    data = {}
    for i in range(4, nrows):
        row_data = sheet1.row_values(i)
        row_data_dict = {}
        for j in range(1, len(row_data)):  # ID 作为key,所以从第二列开始解析
            if row_need[j] == "":
                continue
            if int(row_need[j]) == 1:
                if row_type[j] == 'int' and row_data[j] != "":
                    item = int(row_data[j])
                elif row_type[j] == 'intArray':
                    item = deal_int_array(row_data[j])
                elif row_type[j] == 'stringArray':
                    item = deal_string_array(str(row_data[j]))
                else:
                    item = row_data[j]
                row_data_dict[idx[j]] = item
        if row_data[0] == "":
            continue
        data[int(row_data[0])] = row_data_dict
    return data


def deal_underline_data(data, item):
    """
    处理含有下划线的数据
    :return:
    """
    if '_' in data:  # x_y
        if data.split('_')[0].isdigit():
            temp_list = []
            for element in data.split('_'):
                temp_list.append(int(element))
            item.append(temp_list)
        else:
            item.append(data)
    else:
        item.append(data)


def deal_string_array(data):
    """
    处理stringArray类型数据
    :param data:
    :return:
    """
    temp = data.split('|')
    item = list()
    if len(temp) >= 1 and temp[0] != '':
        for _temp in temp:
            if _temp.isdigit():
                item.append(int(_temp))
            elif is_float(_temp):
                item.append(float(_temp))
            else:
                deal_underline_data(_temp, item)
    return item


def deal_int_array(data):
    """
    处理intArray数据
    :param data:
    :return:
    """
    temp = str(data)
    if isinstance(data, float):
        temp = str(int(data))
    temp = temp.split('|')
    if len(temp) == 1 and temp[0] == '':  # 需要过滤空的字段
        item = list()
    else:
        item = [int(x) for x in temp]
    return item


def is_float(data):
    """
    判断是否是float
    :param data:
    :return:
    """
    value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')  # 定义正则表达式
    return value.match(data)


