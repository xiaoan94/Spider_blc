# encoding:utf-8
'''
Created on 2018年5月1日

@author: liushouhua
'''
import requests
import json
import re
from bs4 import BeautifulSoup
url0 = "https://www.7234.cn/news/"
post_data = {"page": 1}
url = "https://www.7234.cn/fetch_articles/news?page=%s"%(post_data["page"])


res = requests.get(url)
if res.status_code == 200:
    data = res.content
    artlist=data.split('article-item')
    titlepattern = re.compile("alt=(.*?)src",re.S)
    artinfopattern = re.compile('desc(.*?)div',re.S)
    hrefpattern = re.compile('href=(.*?) target',re.S)
    
    for artitem in artlist[1:-2]:
        titleitem = re.findall(titlepattern,artitem)
        artinfoitem = re.findall(artinfopattern,artitem)
        hrefitem = re.findall(hrefpattern,artitem)[0]
        print hrefitem
