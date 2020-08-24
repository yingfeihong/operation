# -*- coding: utf-8 -*-

""" 读取Conf文件
"""


from ConfigParser import ConfigParser, NoSectionError


class ConfReader(ConfigParser):
    """ 读取Conf文件(服务端程序层面的配置文件)
    """

    def as_dict(self, section):

        d = self._defaults.copy()
        try:
            d.update(self._sections[section])
        except KeyError:
            if section != "DEFAULT":
                raise NoSectionError(section)
        return d

    def get_field(self, section, option=None, field_type=None):
        """
        获取对应类型的值
        :param section:
        :param option:
        :param field_type:
        :return:
        """
        if not (field_type and option):
            return self.as_dict(section)
        if field_type == 'string':
            field_value = self.get(section, option)
        elif field_type == 'int':
            field_value = self.getint(section, option)
        elif field_type == 'float':
            field_value = self.getfloat(section, option)
        elif field_type == 'boolean':
            field_value = self.getboolean(section, option)
        else:
            field_value = self.get(section, option)
        return field_value






