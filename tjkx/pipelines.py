# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy import Item
from twisted.enterprise import adbapi

import pymongo


class TjkxPipeline(object):
    def process_item(self, item, spider):
        """
        每个item pipeline组件都需要调用该方法
        这个方法必须返回一个Item对象，或是抛出DropItem异常
        :param item: 被爬取的item
        :param spider: 爬取该item的spider
        :return:
        """
        self.insert_db(item)
        return item

    def open_spider(self, spider):
        """
        在spider开启的时候自动被调用，在此可做一些初始化的操作
        :return:
        """
        # 数据库配置
        db_url = spider.settings.get('MONGODB_URI', 'mongodb://localhost:27017')
        db_name = spider.settings.get('MONGODB_DB_NAME', 'tjkxdb')

        self.db_client = pymongo.MongoClient(db_url)
        self.db = self.db_client[db_name]

    def close_spider(self, spider):
        """
        当spider被关闭时，这个方法被调用
        :return:
        """
        self.db_client.close()

    def insert_db(self, item):
        """
        插入数据
        :param item:
        :return:
        """
        if isinstance(item, Item):
            item = dict(item)
        self.db.tjkx.insert(item)