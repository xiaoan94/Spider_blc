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
    url = "https://www.7234.cn/news/"
    start_urls = [url ,]

    def parse(self, response):
        
        
#         f = open('spider.txt','a')
#         f.write(response.body)
#         print response.body
# #         print "qweqe标价标价"
#         
        item = IhuopinspiderItem        
        res = response.xpath('/html/body/div[2]/div[1]/div[3]/div/div') 
        i = len(res)      
        ll = [] 
        for num  in res:
            item['title'] = res.xpath('./div[1]/div/div[1]/h3/text()').extract()[0]
            print "继续标记：",item['title']
            item['author']=res.xpath('//*[@id="js_content"]/p[num+1]/text()').extract()[0]
            #时间
            item['time'] = res.xpath('//*[@id="js_content"]/p[num+1]/text()').extract()[0]
            #内容
            item['content'] = res.xpath('//*[@id="js_content"]/p[num+1]/text()').extract()[0]
            #图片
            item['picture'] = res.xpath('//*[@id="js_content"]/p[num+1]/text()').extract()[0]
            
        
            
        urls = self.url    
        print urls
        print "URL链接标记"
        yield Request(urls , callback = self.parse)