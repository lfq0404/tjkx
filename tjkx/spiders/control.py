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


def str2time(str_time):
    """
    str格式要求：年月日[时[分[秒]]]，以非数字分割
    eg：2018-08-08、2018-08-08 08:12:12、2018-08-08 23等
    返回格式：年:月:日 时:分:秒
    """
    str_date = re.split('[^\d]+', str_time.strip())
    int_date = [i for i in map(lambda s: int(s), str_date)]
    return datetime.datetime(*int_date[:6])


def date2chstr(date):
    """
    将date转为中文字符串
    :param date:
    :return:
    """
    str_date = str(date)  # '2019-01-21'
    str_date = str_date.replace('-', '年', 1)
    str_date = str_date.replace('-', '月', 1)
    return str_date


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


def deal_introduction(msg):
    """
    处理导读的特殊格式
    传入：'#河套酒业 早间播报#1.四川省人大提案：建立三支酒类发展基金；“梦之蓝经典咏流传百家姓礼盒”1月22日上线......更多行业重磅新闻，敬请关注糖酒快讯每日播报！'
    返回: 1.四川省人大提案：建立三支酒类发展基金；“梦之蓝经典咏流传百家姓礼盒”1月22日上线
    :param msg:
    :return:
    """
    obj = re.compile('#.*?#(.*?)\.{6}')
    msg = obj.findall(msg)[0]

    return msg


def del_src_number(msg):
    """
    去掉原来的编号
    :param msg: 1.xxx
    :return:
    """
    obj = re.compile('^\d+?\.')
    msg = obj.sub('', msg)

    return msg
