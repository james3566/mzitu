#python/spider/PaMzitu.py
"""关于分类标签的类"""

import multiprocessing as mp
from functools import wraps
import time
import settings
import tools
import spider

class PaMzitu():
    def __init__(self, fen_url):
        self.fen_url = fen_url      #接收分类页面链接
        self.tao_urls = []          #建立套图链接列表，初始为空
        self.name = ''              #页面题目作为保存图片文件夹名，初始为为空
        self.fen_path = ''
        self.get_tao_urls_list()
        
    def get_tao_urls_list(self,i=1):
        """获取分类标签下的所有套图的链接列表tao_urls"""
                               
        while i:                            #建立循环，退出退出循环条件为i='404 '(注意404后有空格)
            start_url = self.fen_url + "page/%d/" % i       #拼接标签分页面链接
            mess = spider.get_mess(start_url)                #获取初始页面数据  
            name = mess.find('title').text.split(r'-')[0]  #获取页面题目
                         
            if name == "404 ":
                break      #页面题目为'404 '时，获取的是说明超出标签分页范围的页面，退出循环
            elif self.name == '':            #页面题目为空时才写入，确保以后不被重新写入
                self.name = name.strip()    #strip（）是去除字符串前后的空格
            
            self.fen_path = settings.Mzitu().path + self.name + r'/'  #拼接保存图片总路径
            
            #获取标签分页面上的套图链接列表
            postlist = mess.find("div", class_="postlist")  #获取<div, class_="postlist">这一块的内容
            urls = postlist.find_all('a')   #获取快中所有 <a 子块的内容，返回的是list
            for u in urls:              #获取list中每个元素中的链接装入self.tao_urls
                u = u['href'].strip()   #提取'href'中的链接，strip()是去除字符串两端空格
                if u not in self.tao_urls:      #过滤重复元素
                    self.tao_urls.append(u)     #将获得的链接加入套图链接列表中
            i += 1

    @tools.timerJ()      
    def run(self, ProcessesMaxNumber=8):
        """爬虫开始运行。使用进程池，默认进程数 8 个"""
        pool = mp.Pool(processes=ProcessesMaxNumber)
        for url in self.tao_urls:
            pool.apply_async(spider.group_picture, args=(url, self.fen_path))
        pool.close()
        pool.join()


    
