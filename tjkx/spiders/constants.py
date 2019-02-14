import datetime
import re
import time
import random

import tjkx.spiders.control as con

GET_MRBB_URL = lambda page_num: 'http://info.tjkx.com/list/201803-{}.htm'.format(page_num)  # 获取每日播报url

MIN_DATE = con.str2date(input('开始日期（年-月-日）：'))  # 爬取的最小日期
MAX_DATE = con.str2date(input('开始日期（年-月-日）：'))  # 爬去的最大日期

MIN_TIME = datetime.datetime.strptime(str(MIN_DATE) + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
MAX_TIME = datetime.datetime.strptime(str(MAX_DATE) + ' 23:59:59', '%Y-%m-%d %H:%M:%S')


BASE_IMG_URL = 'http://a.tjkximg.com'  # 以图片作为基准的地址
PARTITION_SIGN = '骚操作的分隔符'  # 分割标识，骚操作
NEED_DELETE_MSGS = ['点击此处查看详情']  # 需要删除的信息
MIN_IMG_INDEX = 2  # 获取第2张到第5张图片之间的信息
MAX_IMG_INDEX = 5

KXTT_INDEX = 2  # 快讯头条
TJKX_INDEX = 3  # 糖酒快讯
QYDT_INDEX = 4  # 企业动态
HYDT_INDEX = 5  # 行业动态

BEGIN_RECORD_OBJ = re.compile('^1\.')  # 开始记录的标识
STOP_RECORD_OBJ = re.compile('^\d+\.')  # 匹配以数字开头编号的文本，可作为结束记录的标识
