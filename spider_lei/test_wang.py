# encoding:utf-8
'''
Created on 2018年5月1日

@author: wangruoyu
'''
import requests
import re
from bs4 import BeautifulSoup
import json

url = "https://www.ihuoqiu.com/MAPI/GetArticleInfoData"
#文章链接 requests payload
url_data = "ImX18T140t8bqX7oDun6uw__2C__2C"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
    "Connection":"keep-alive",
    "Content-Type":"application/json;charset=UTF-8",
    "Origin":"http://m.ihuoqiu.com",
    "Referer":"http://m.ihuoqiu.com/article?id=%(url_data)s&type=1"
}

data = '''{Type: "1", data: "%s"}'''%url_data
response =requests.post(url=url,data=data,headers=headers)

if response.status_code == 200:
    article_json = json.loads(response.content)
    article_content = article_json.get("data",[])
    art_content_list = article_content.split(',"')
    article = art_content_list[2]
    print article
    pattern = re.compile('img src=(.*?)\" ',re.S)
    item = re.findall(pattern,article)
    print item
    #按照自然段分割
    article = article.split("</")
    article1 = []    
    for i in article:
        article1.append(BeautifulSoup(i,'lxml').get_text())     
#     #将文章按照自然段存入list之中
    allart=[]
    for j in article1:
        concent=j.split(">")
        if len(concent)>1:
            allart.append(concent[-1])
#     print allart
    
#     for i in allart:
#         print i
# #     
    
    
    
    