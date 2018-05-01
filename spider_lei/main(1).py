# encoding:utf-8
"""
作者：王若愚
工作：1.合并文章查询程序与获取文章内容程序
     2.添加sql语句
时间：2018/05/01 03:16
"""
import scrapy
from bs4 import BeautifulSoup
import time
import sched
import re
from apscheduler.schedulers.blocking import BlockingScheduler
# import queue
import Queue
import requests
import json
# import pymysql
# 设定间隔时间 秒
inc = 5
class main(object):
    def __init__(self):
        self.url = 'https://www.ihuoqiu.com/MAPI/GetArticleListData'  # 首页网址url
        self.urlqueue = Queue.Queue() # python2 创建url的队列
#         self.urlqueue = queue.Queue()  #python3 创建url的队列
        
        # 模拟成浏览器
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
            'Referer': 'http://m.ihuoqiu.com/index',
            'Origin': 'http://m.ihuoqiu.com',
            'Connection':'keep-alive',
            'Content-Type':'application/json;charset=utf-8',
        }        
        #设定schedule对象
        self.schedule = sched.scheduler(time.time, time.sleep) 

        self.article = []  # 存放标题的变量
        self.content = {}    # 存放文章内容
    
    def perform_command(self,inc):
        self.schedule.enter(inc,0,self.perform_command,(inc,))
        self.run_()
    def timming_exe(self,inc = inc):
        #enter 用来安排事件的发生
        self.schedule.enter(inc,0,self.perform_command,(inc,))
        self.schedule.run()
        
    def run(self,count):        
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
        post_data = '''{"Type":1,"PageIndex":1,"PageSize":%s}'''%(count)
        #r = requests.post(url=self.url, data=post_data, headers=self.headers, proxies=proxy_addr, verify=False)
        r = requests.post(url=self.url, data=post_data, headers=self.headers)

        # 从页面代码中获取title的链接
        if r.status_code == 200:
            # 获得页面代码
            data = r.content
            j_data = json.loads(data)
            #print (j_data)

            #将页面转化为json格式
            if "code" in j_data.keys() and j_data.get("code") == 200:
                all_articles = j_data.get("data", [])
                all_articles_list = all_articles[2:-2].split("},{")
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
                    ArticleInfo = article_info.get("ArticleInfo", "No finding the information")
                    #获取页面链接
                    Url_data = article_info.get("data1", None)
#                     print Url_data
                    #获取文章内容
                    article = self.get_article_content(Url_data)
                    article_content = article["allart"]
                    article_picture = article["picture"]
#                     print article_content
                    Title  = ArticleInfo.get("Title", "No finding the content")
                    ImgUrl = ArticleInfo.get("ImgUrl","No finding the img")
                    Source = ArticleInfo.get("Source","No finding the source")
                    Author = ArticleInfo.get("Author","No finding the author")
                    ShortDescription = ArticleInfo.get("ShortDescription", "No finding the description")
                    
                    #将文章数据保存为json格式
                    self.content = {
                        "Title":Title.encode,
                        "ImgUrl":ImgUrl.encode,
                        "Source":Source.encode,
                        "Author":Author.encode,
                        "ShortDescription":ShortDescription.encode,
                        "article_content":article_content,
                        "article_picture":article_picture
                    }
                    self.article.append(self.content)
                    
            #show the list of article
            print("The length is:",len(self.article))
            #展示采集数据
            for i in self.article:
                f = open("art.txt","a")
                f.write(str(i))
                print 1
#                 print("the article is:",i)
            """
            准备导入数据库
            """
#             self.import_to_db(self.article)
        else:
            print(u"页面加载失败")
            time.sleep(100)
            self.run()
            return None
    #将文章数据导入到mysql中
#     def import_to_db(self,art):
#         #创建 connection链接
#         connection = pymysql.connect(host='mysql-wang.cekkdnv29igt.us-west-2.rds.amazonaws.com',
#                        port=3306,user='scrapy',passwd='scrapy25806',charset='utf8')
#         try:
#             with self.connection.cursor() as cursor:
#                 sql = "CREATE database if not exists LWL"
#                 cursor.execute(sql)
#                 cursor.execute("use LWL")
#                 #在该数据库中创建一个名为article的表
#                 sql = "CREATE TABLE if not exists article(Title VARCHAR(200),Author VARCHAR(20),Url_data VARCHAR(20),Content text)"
#                 cursor.execute(sql)
#                 sql = "INSERT INTO article(Title,Author,Content) VALUES(%s,%s,%s,%s)"
#                 try:
#                     #开始插入数据
#                     for db_art in art:
#                         cursor.execute(sql,(db_art.get("Title", None),db_art.get("Author", None),db_art.get("Url_data",None),db_art.get("Content",None)))
#                         self.connection.commit()
#                 except:
#                     self.connection.rollback()
#                 """
#                 增加一个去重功能
#                 """
#         finally:
#             self.connection.close()
    def get_article_content(self,Url_data):
        url = "https://www.ihuoqiu.com/MAPI/GetArticleInfoData"
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
            "Connection":"keep-alive",
            "Content-Type":"application/json;charset=UTF-8",
            "Origin":"http://m.ihuoqiu.com",
            "Referer":"http://m.ihuoqiu.com/article?id="+str(Url_data)+"&type=1"
        }
        data = '''{Type: "1", data: "%s"}'''%Url_data
        response =requests.post(url=url,data=data,headers=headers)
        article1 = []
        allart=[]#存放文章
        if response.status_code == 200:
            #将文章内容转化为正常格式
            article_json = json.loads(response.content)
            article_content = article_json.get("data",[])
            art_content_list = article_content.split(',"')
            article = art_content_list[2]
            pattern = re.compile('img src=.*?(.*?)\" ',re.S)
            picture = re.findall(pattern,article)
            article = article.split("</")
            
            for item in article:
                article1.append(BeautifulSoup(item,'lxml').get_text())
            for each in article1:
                concent=each.split(">")
                if len(concent)>1:
                    allart.append(concent[-1])
            return {"allart":allart,"picture":picture}
            

if __name__ == "__main__":
    tit = main()   
    tit.run(10)#首次爬取全部内容把10改为502以上数字
    sche = BlockingScheduler()
    sche.add_job(tit.run(10), 'interval',  days = 1)#每天爬取最新的20篇文章（每天更新文章不超过20篇所以能把每天更新的文章都爬取下来）
    sche.start()
# except ConnectionError as e:
#     print(e)