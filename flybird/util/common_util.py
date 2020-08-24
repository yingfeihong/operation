# -*- coding: utf-8 -*-

""" 通用工具类

"""

import os


def cid_to_user_id(cid):
    """
    客户端显示ID转换为后台数据库ID
    :param cid: 客户端显示ID
    :return:
    """
    return int(cid) - 635600


def user_id_to_cid(user_id):
    """
    后台数据库ID转换为客户端显示ID
    :param user_id: 后台数据库用户ID
    :return:
    """
    return 635600 + int(user_id)


def dictionary_sort(src_dict):
    """
    基于value对字典排序
    :param src_dict: 待排序字典
    :return result: 返回值为列表类型          e.g [(key, value), (key, value)....]
    """
    result = sorted(src_dict.iteritems(), key=lambda item: item[1], reverse=True)
    return result


def dictionary_del_null(src_dict):
    """
    删除一个字典结构中的空值或者0值
    :param src_dict:
    :return:
    """
    for key in src_dict.keys():
        if src_dict[key] == 0 or src_dict[key] == []:
            del(src_dict[key])

    return src_dict


def binarySearch(target, sortedList):
    """
    二分查找算法
    :param target: 查找的目标值
    :param sortedList: 所查找的列表
    :return:
    """
    list_length = len(sortedList)
    start, end = 0, list_length - 1
    if list_length == 0:
        print 'empty list'
        return -1
    while start < end:
        middle = (start + end) / 2
        if target == sortedList[middle]:
            print 'find index:', middle
            return middle
        elif target < sortedList[middle]:
            end = middle - 1
        else:
            start = middle + 1
    print 'not find'
    return -1


def list_add(list_1, list_2):
    """
    列表相加 (两个列表长度相同)
    :param list_1: 第1个属性列表
    :param list_2: 第2个属性列表
    :return:
    """
    attr_list = []
    length = len(list_1)

    for i in range(0, length):
        attr_list.append(list_1[i] + list_2[i])

    return attr_list


def get_initialized_list(npc_count, item):
    """
    获取初始化好的列表结构
    :param npc_count:
    :param item:
    :return:
    """
    item_list = []

    for i in range(0, npc_count):
        item_list.append(item)

    return item_list


def get_file_full_path(file_name, file_dir='doc'):
    """
    获取文件名(包含全路径)
    :param file_dir: 文件路径           e.g. 'doc'
    :param file_name: 文件名           e.g. "Clothes.csv"
    :return:
    """
    return os.path.join(os.getcwd(), file_dir, file_name)


def get_field_index(tmp_list, value):
    """
    根据数组的内容，来获取该值的下标
    :return:
    """
    index = tmp_list.index(value)

    return index


def get_value(value):
    """
    安全获取value值，用在读取csv等外部文件时
    :param value:
    :return:
    """
    result = 0

    if value:
        result = value

    return result


def get_file_amount(file_dir):
    """
    统计目录中的文件数量
    :param file_dir: 文件路径           e.g. '../doc/'
    :return:
    """
    path = os.path.join(os.path.dirname(__file__)) + '/'
    file_dir = path + file_dir
    # print "get_file_amount(): file_dir:", file_dir

    count = len(os.listdir(file_dir))
    return count


def list_str_to_int(item_list):
    """
    把item为str型的列表，转换item为int型的列表
    :param item_list:
    :return:
    """
    new_list = []

    for item in item_list:
        new_list.append(int(item))

    return new_list


def get_pb_cmd(key):
    """
    获取pb的cmd
    :param key:
    :return:
    """
    from core.init.method_map import MethodMap
    return MethodMap.cmd_config.get(key)

