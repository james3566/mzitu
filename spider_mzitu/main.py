#python/spider/main.py
"""爬取网站分类标签下的全部套图"""

import os
from PaMzitu import PaMzitu
from spider import group_picture

def classified_picture(url):
    pa = PaMzitu(url)    #建立分类标签对象
    pa.run()

if __name__ == '__main__': 
    os.system('cls')    #清空屏幕
    classified_picture("https://www.mzitu.com/tag/songguoer/")  #爬取分类图片
    # spider.group_picture("https://www.mzitu.com/162178")    #爬取套图