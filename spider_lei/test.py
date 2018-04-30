# encoding:utf-8
'''
Created on 2018年4月30日

@author: liushouhua
'''
import requests
import json
import re
import urllib
from bs4 import BeautifulSoup
url_data = "ARXo5jMpGJErk99__2BF32ZQw__2C__2C"  #前面获取到的url_data
url = "https://www.ihuoqiu.com/MAPI/GetArticleInfoData"
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
            'Referer': 'http://m.ihuoqiu.com/article?id=%(url_data)s&type=1',
            'Origin': 'http://m.ihuoqiu.com',
            'Connection':'keep-alive',
            'Content-Type':'application/json;charset=utf-8',
        }

data = '''{Type: "1", data: "%s"}'''%url_data
# response = requests.get(url)
# html = response.text
# page = urllib.urlopen(url)
# print page.read()
r = requests.post(url=url,data=data, headers=headers)
if r.status_code == 200:
    data = r.content
    art_json = json.loads(data)
    art_content = art_json.get("data", [])
    art_content_list = art_content.split(',"')
    print art_content_list[2]                              #文章所在字符
#     at=all_articles.get("Remark", [])

# for item in all_articles_list:
#     print item



# session = requests.session()
# page = urllib.urlopen(url)#打开网址
# html = page.read()        #读取网页内容，保存到htlm中
# bs0bj=BeautifulSoup(html,'lxml') #创建一个beautifulsoup的类
# # namelist=bs0bj.findAll("p",{"style":"white-space: normal;box-sizing: border-box;"})#通过标签筛选文字信息
# namelist=bs0bj.findAll("p")
# for name in namelist:
#     print (name.get_text())       

# import requests 
# session = requests.session()
# url1 = 'http://zqyjbg.com/resinfo/listCom-2.html'
# url2 = 'http://zqyjbg.com/resinfo/info/viewResComQuery.html?flag=flag_2&pageQuery=true&pageNum=2'
# headers = {
# "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
#             'host': 'zqyjbg.com',
#             'Accept-Language': 'zh-CN,zh;q=0.8',
#             'Accept-Encoding': 'gzip, deflate, sdch',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#             'Upgrade-Insecure-Requests': '1',
#             'Connection': 'keep-alive'
#          }
# r1 = session.get(url)
# r2 = session.get(url2)
# print(r1.text)   
    
    
    
    
    