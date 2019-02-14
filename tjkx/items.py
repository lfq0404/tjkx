# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TjkxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # 标题
    public_time = scrapy.Field()  # 发布时间
    introduction = scrapy.Field()  # 导读
    details = scrapy.Field()  # 详情页面的详情部分
    # kxtt = scrapy.Field()  # 快讯头条
    # tjkx = scrapy.Field()  # 糖酒快讯
    # qydt = scrapy.Field()  # 企业动态
    # hydt = scrapy.Field()  # 行业动态

