# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class IhuopinspiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #新闻标题
    title = Field()
    #作者
    author=Field()
    #时间
    time = Field()
    #内容
    