# -*- coding: utf-8 -*-

""" 读取CSV文件

"""

import csv


class CSVReader(object):
    """ 读取CSV文件
    """

    field_name_list = []

    @classmethod
    def parse(cls, file_name, func_parse_line):
        """
        解析读取后的文档
        :param func_parse_line:  解析文档每一行的函数
        :param file_name:
        :return:
        """
        doc = cls.read(file_name)  # 读取文件

        i = 0
        try:
            for row in doc:
                if i >= 2:  # 跳过第1行和第2行
                    func_parse_line(row)  # 解析每一行
                    # print row
                elif i == 1:  # 第一行为字段名称
                    cls.field_name_list = row
                i += 1
        except:
            print 'Error %s line:%d' % (file_name, i + 1)
            raise

        return doc

    @classmethod
    def read(cls, file_name):
        """
        读取文件
        :param file_name: csv文件名
        :return:
        """
        csv_file = open(file_name, 'rb')
        doc = csv.reader(csv_file)
        return doc
