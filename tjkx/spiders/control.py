import re
import datetime

import tjkx.spiders.constants as cons


def str2date(str_date):
    """
    str格式要求：年月日[时[分[秒]]]，以非数字分割
    eg：2018-08-08、2018-08-08 08:12:12、2018-08-08 23等
    返回格式：年:月:日
    """
    str_date = re.split('[^\d]+', str_date.strip())
    int_date = [i for i in map(lambda s: int(s), str_date)]
    return datetime.date(*int_date[:3])


def del_blank_str(msg):
    """
    删除msg中开头和结尾的的空白字符
    :param msg:
    :return:
    """
    obj1 = re.compile('^\s*')  # 开头空白字符
    obj2 = re.compile('\s*$')  # 结尾空白字符
    msg = obj1.sub('', msg)
    msg = obj2.sub('', msg)

    return msg


class BaseDetails:
    def __init__(self):
        self.details_list = []  # 详细信息列表，最终返回时需要以换行符分割

    def add_details(self, new_msg):
        self.details_list.append(new_msg)


