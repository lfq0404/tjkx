import scrapy

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
            if not i.find('a'):
                continue
            url = i.find('a')['href']  # 下一级网址
            if i.find('i'):
                public_date = control.str2date(i.find('i').text)  # 2019年01月28日 06:54 --> datetime.date(2019, 1, 28)
            else:
                print('找不到网址：', i)
                continue
            if cons.MIN_DATE <= public_date <= cons.MAX_DATE:
                print('下一级网址是：', url)
                yield Request(url, callback=self.get_details)

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
        public_time = control.str2time(public_time_obj.find('span').text)  # 发布时间

        introduction_obj = public_time_obj.next_sibling.next_sibling
        introduction = control.del_blank_str(introduction_obj.find('span').next_sibling)  # 导读
        introduction = control.deal_introduction(introduction)  #

        details = introduction_obj.next_sibling.next_sibling.find_all('p')
        details_text = []  # 整个详情页面的汇总
        details_result = []  # 筛选后的详情信息(头条 + 快讯 + 企业动态 + 行业动态)
        # kxtt = []  # 快讯头条
        # tjkx = []  # 糖酒快讯
        # qydt = []  # 企业动态
        # hydt = []  # 行业动态
        for info in details:
            # 获取文本信息 + 图片信息（作为分割）
            text = info.text
            if not text:
                text = info.find('img') and info.find('img')['src']
                if text and cons.BASE_IMG_URL in text:
                    text = cons.PARTITION_SIGN
                else:
                    text = ''
            text = control.del_blank_str(text)

            if text:
                if text not in cons.NEED_DELETE_MSGS:
                    details_text.append(text)

        # 提取对应的信息，目前不需要分类，直接把整个页面的数据返回
        # 分隔符后不是以'数字.'形式开头的进行剔除
        begin_record = False
        stop_record = False
        for index, i in enumerate(details_text):
            # 如果运行进行记录（以1.开始，并且图片紧接着的不是以数字开头的值）
            if begin_record and not stop_record:
                # 判断图片紧接着的是不是以数字开头的内容
                if i == cons.PARTITION_SIGN:
                    if (index + 1 == len(details_text)) or (not cons.STOP_RECORD_OBJ.match(details_text[index + 1])):
                        stop_record = True
                else:
                    details_result.append(i)
            # 以1.开头的才运行开始进行记录
            else:
                if cons.BEGIN_RECORD_OBJ.match(i):
                    begin_record = True
                    details_result.append(i)

        # 保存数据
        item = TjkxItem()
        item['title'] = title
        item['public_time'] = public_time
        item['introduction'] = introduction
        item['details'] = details_result

        print('已经保存完成', response)

        return item
