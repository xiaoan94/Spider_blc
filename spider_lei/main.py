#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
import Queue
import requests
import json


class main(object):

    def __init__(self):
        self.url = 'https://www.ihuoqiu.com/MAPI/GetArticleListData'  # 首页网址url
        self.urlqueue = Queue.Queue() # 创建url的队列

        # 模拟成浏览器
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
            'Referer': 'http://m.ihuoqiu.com/index',
            'Origin': 'http://m.ihuoqiu.com',
            'Content-Type': 'application/json;charset=utf-8',
        }

        self.title = []  # 存放标题的变量

    def run(self):
        # 该线程要执行的任务,即获得url队列,传入页面的url获得页面的代码
        response = None
        content = ''
        """
        # 使用代理服务器访问网页
        proxy_addr = {
            "http": "http://127.0.0.1:8080",
            "https": "https://127.0.0.1:8080"
                      }
        """
        # 构建请求的request
        post_data = '''{"Type":1,"PageIndex":1,"PageSize":10}'''
        #r = requests.post(url=self.url, data=post_data, headers=self.headers, proxies=proxy_addr, verify=False)
        r = requests.post(url=self.url, data=post_data, headers=self.headers)

        # 从页面代码中获取title的链接
        if r.status_code == 200:
            # 获得页面代码
            data = r.content
            j_data = json.loads(data)
            #print j_data

            if "code" in j_data.keys() and j_data.get("code") == 200:
                all_articles = j_data.get("data", [])
                all_articles_list = all_articles[1:-1].split("},{")
                ll = []
                for one in all_articles_list:
                    if one[0] == u"{" and one[-1] != u"}":
                        one = one + u"}"
                    elif one[0] != u"{" and one[-1] != u"}":
                        one = u"{" + one + u"}"
                    elif one[0] != u"{" and one[-1] == u"}":
                        one = u"{" + one
                    one = json.loads(one)
                    ll.append(one)
                for article_info in ll:
                    #print article_info
                    ArticleInfo = article_info.get("ArticleInfo", None)
                    title = ArticleInfo.get("Title", "Error")
                    ShortDescription = ArticleInfo.get("ShortDescription", "Error")
                    url_data = article_info.get("data1", None)
                    self.title.append((title, url_data,ShortDescription))
            print len(self.title)
        else:
            print u"页面加载失败"
            return None



if __name__ == "__main__":
    tit = main()
    tit.run()