# -*- coding: utf-8 -*-

""" 统计代码行数
"""

import os


class CountCodeLine(object):
    """
    """

    @classmethod
    def init(cls, project_path):
        """ 初始化
        """
        cls.count_lines(project_path)

    @classmethod
    def count_lines(cls, project_path):
        """ 统计项目代码总行数
        """
        total_line = 0
        file_lines = {}

        for root, dirs, files in os.walk(project_path):
            for item in files:
                if item.find(".pyc") != -1:
                    continue

                if item.find("__init__") != -1:
                    continue

                if item.find(".py") != -1:
                    file_path = root + os.sep + item
                    count = len(open(file_path, 'r').readlines())
                    total_line += count

                    file_lines[item] = count

        from util.common_util import dictionary_sort
        file_lines_num_list = dictionary_sort(file_lines)

        print "Total lines of all files: ", total_line
        for item in file_lines_num_list:
            print item


# 主函数
if __name__ == '__main__':
    # path = "D:/game_server"
    path = os.path.dirname(os.getcwd())
    print path
    CountCodeLine.init(path)
