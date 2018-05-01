# encoding:utf-8
'''
Created on 2018年5月1日

@author: liushouhua
'''
import requests
import json
import re
from bs4 import BeautifulSoup
url0 = "https://www.7234.cn/"
post_data = {"page": 1}#数字代表页数，通过改变数字爬取其他野内容
url = "https://www.7234.cn/fetch_articles/news?page=%s"%(post_data["page"])

fp = open("cont.txt","a")
res = requests.get(url)
if res.status_code == 200:
    data = res.content
    fp.write(data)
    artlist=data.split('article-item')
#     print artlist
    titlepattern = re.compile("alt=(.*?)src",re.S)
    artinfopattern = re.compile('desc(.*?)div',re.S)
    hrefpattern = re.compile('href=(.*?) target',re.S)
    
    for artitem in artlist[1:-2]:
        titleitem = re.findall(titlepattern,artitem)
#         print titleitem
        artinfoitem = re.findall(artinfopattern,artitem)
#         print artinfoitem
        hrefitem = re.findall(hrefpattern,artitem)[0]#url0+hrefitem是文章正文链接
        print hrefitem[3:-2]
#         print artitem
#         print hrefitem
