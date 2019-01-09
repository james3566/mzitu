#python/spider/spider.py
"""爬取目标网站相关数据，本脚本可单独下载套图"""
import os
import sys
import time
import requests
import threading
import settings
from bs4 import BeautifulSoup
import tools


def get_mess(url,Hostreferer=settings.Mzitu().Hostreferer):
    """通过链接 url 返回对应页面的 mess 信息"""
    html = requests.get(
            url,
            proxies = settings.proxies, 
            headers = Hostreferer
            ) #模拟浏览器访问    
    html.coding = 'utf-8'   #设置编码
    return BeautifulSoup(html.text, 'html.parser')

def page_m(url,jpg_id):
    """爬取单个页面的数据"""
    mess = get_mess(url,Hostreferer=settings.Mzitu().Hostreferer)  
    name = mess.find('img')['alt']                  #抓取图片名称
    file_name = name + '(' +str(jpg_id) + ')'       #为图片名称编号 
    sys.stdout.write("\n%s 正在爬取：%s" % (time.ctime(),file_name))
    if os.path.exists(file_name + ".jpg") == False:

        jpg = requests.get(mess.find('img')['src'],
                                    proxies = settings.proxies, 
                                    headers = settings.Mzitu().Hostreferer
                                    )
        with open(file_name + '.jpg', 'wb') as f:
            f.write(jpg.content)
            f.close
    else:
        print("文件已存在，跳过！")

@tools.timerX
def group_picture(url, path='/python/photos/mzitu/'):
    """爬取套图页面的数据"""
    mess = get_mess(url,Hostreferer=settings.Mzitu().Hostreferer)      #解析网页数据
    name = mess.find('h2').text       #获取套图名称
    tao_path = path + name                              #存放路径
    max_number = int(mess.find_all('span')[10].text)    #套图共有张数
    print(tao_path)
    #循环爬取套图中的图片
    while os.path.exists(tao_path) == False:            #如路径文件夹存在，就退出任务进程
        # print("\n正在创建----%s----文件夹\n"%tao_path)  
        os.makedirs(tao_path)                           #创建并进入文件夹
        os.chdir(tao_path)
    
        #循环把下载任务装入线程列表
        threadList = []
        for i in range(1, max_number + 1):  #遍历每张图片编号
            jpg_url = url + r"/" + str(i)  #拼接图片链接
            t=threading.Thread(target=page_m,args=(jpg_url,i))  #生成任务线程，调用 page_m() 函数
            threadList.append(t)                                #装入线程列表

        tools.thread_start(threadList)  #开启多线程

        # imgCut(os.path.abspath('.'))        #把图片水印部分裁剪掉
        tools.url_log(url, name)  #写入日志
