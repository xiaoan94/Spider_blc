# encoding:utf-8
'''
Created on 2018年4月28日

@author: liushouhua
'''
import scrapy
from scrapy import Request
from ihuopinspider.items import IhuopinspiderItem
import json

class NewsSpider(scrapy.Spider):
    name = "newscontent"
#     allowed_domains = ['m.ihuoqiu.com']
    url = "https://www.ihuoqiu.com/Home/Index"
#     start_urls = [url ,]
    def start_requests(self):
#         url = "https://www.ihuoqiu.com/Home/Index"
        data = '''{"Type":1,"PageIndex":1,"PageSize":10}'''
        yield scrapy.FormRequest(
            url = self.url,
            method="POST", 
            body=json.dumps(data), 
            headers={'Content-Type': 'application/json'},
            callback = self.parse
        )
    def parse(self, response):
        
        
        f = open('spider.txt','a')
        f.write(response.body)
        print response.body
#         print "qweqe标价标价"
#         
        item = IhuopinspiderItem        
        res = response.xpath('/html/body/div[2]/div[1]/div[3]/div/div')        
        for line in res:
            item['title'] = line.xpath('./div/div[1]/h3/a/text()').extract()[0]
            print "继续标记：",item['title']
            item['author']=line.xpath('./div/div[1]/h3/a/text()' ).extract()[0]
            #时间
            item['time'] = line.xpath('./div/div[1]/h3/a/text()' ).extract()[0]
            #内容
            item['content'] = line.xpath('./div/div[1]/h3/a/text()' ).extract()[0]
            #图片
            item['picture'] = line.xpath('./div/div[1]/h3/a/text()' ).extract()[0]
            
        
            
        urls = self.url    
        print urls
        print "URL链接标记"
        yield Request(urls , callback = self.parse)