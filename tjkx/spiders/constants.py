import datetime

GET_MRBB_URL = lambda page_num: 'http://info.tjkx.com/list/201803-{}.htm'.format(page_num)  # 获取每日播报url

MIN_DATE = datetime.date(2019, 1, 1)  # 爬取的最小日期
MAX_DATE = datetime.date(2020, 1, 4)  # 爬去的最大日期

BASE_IMG_URL = 'http://a.tjkximg.com'  # 以图片作为基准的地址
MIN_IMG_INDEX = 2  # 获取第2张到第5张图片之间的信息
MAX_IMG_INDEX = 5

WBTT_INDEX = 2  # 晚报头条
TJKX_INDEX = 3  # 糖酒快讯
QYDT_INDEX = 4  # 企业动态
HYDT_INDEX = 5  # 行业动态
