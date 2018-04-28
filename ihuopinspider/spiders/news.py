# encoding:utf-8
'''
Created on 2018年4月28日

@author: liushouhua
'''
import scrapy
from scrapy import Request
from ihuopinspider.items import IhuopinspiderItem

class NewsSpider(scrapy.Spider):
    name = "newscontent"
    allowed_domains = ['m.ihuoqiu.com']
    url = "http://m.ihuoqiu.com/index"
    start_urls = [url ,]
    def parse(self, response):
        item = IhuopinspiderItem
        res = response.xpath("//*[@id='IndexPage']/div[2]/div[2]/div[2]")
        
        for line in res:
            item['title'] = line.xpath('./div[1]/div[2]/div[2]/span[2]/text()' ).extract()[0].strip()
            item['author']="q"
            #时间
            item['time'] = "q"
            #内容
            item['content'] = "q"
            #图片
            item['picture'] = "q"
            
        
            
        urls = self.url    
        yield Request(urls , callback = self.parse)