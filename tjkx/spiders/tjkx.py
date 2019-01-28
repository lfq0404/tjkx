import scrapy
import re

from bs4 import BeautifulSoup
from scrapy.http import Request

from tjkx.items import TjkxItem

import tjkx.spiders.constants as cons
import tjkx.spiders.control as control


class BaseSpider(scrapy.Spider):
    """
    糖酒快讯基础爬虫
    1、首先执行scrapy.Spider中的start_requests
    2、再执行make_requests_from_url
    3、再用parse进行抓取
    """
    name = 'tjkx'

    def start_requests(self):
        for page_num in range(1, 10):
            url = cons.GET_MRBB_URL(page_num)
            yield Request(url, self.parse)

    def parse(self, response):
        """
        第一步：从列表页面进入
        :param response:
        :return:
        """
        text = response.text
        infos = BeautifulSoup(text, 'lxml').find('div', class_='bj-contents mar37').find_all('li')
        for i in infos:
            url = i.find('a')['href']  # 下一级网址
            public_date = control.str2date(i.find('i').text)  # 2019年01月28日 06:54 --> datetime.date(2019, 1, 28)
            if cons.MIN_DATE <= public_date <= cons.MAX_DATE:
                yield Request(url, callback=self.get_details)
            else:
                break

    def get_details(self, response):
        """
        第二步：获取详情
        :param response:
        :return:
        """
        text = response.text
        title_info = BeautifulSoup(text, 'lxml').find('h1')  # 以每页的标题为基础
        title = title_info.text  # 标题

        public_time_obj = title_info.next_sibling.next_sibling
        public_time = public_time_obj.find('span').text  # 发布时间

        introduction_obj = public_time_obj.next_sibling.next_sibling
        introduction = control.del_blank_str(introduction_obj.find('span').next_sibling)  # 导读

        details = introduction_obj.next_sibling.next_sibling.find_all('p')
        img_index = 0  # http://a.tjkximg.com 第2--5个之后的是内容
        wbtt = []  # 晚报头条
        tjkx = []  # 糖酒快讯
        qydt = []  # 企业动态
        hydt = []  # 行业动态
        for info in details:
            # 以图片为基准点
            img_info = info.find('img')
            if img_info:
                img_url = img_info['src']
                if cons.BASE_IMG_URL in img_url:
                    img_index += 1
                    if cons.MIN_IMG_INDEX <= img_index <= cons.MAX_IMG_INDEX:  # 获取第2张到第5张图片之间的信息
                        details_obj = control.BaseDetails()
                    else:
                        continue
                else:
                    continue








