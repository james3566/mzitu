#python/spider/tools.py

import os
import sys
import time
import threading
import requests
from functools import wraps
import settings



def url_log(url, name):
    """爬取日志：记录下载时间、套图链接、套图名称，url为套图链接，name为套图名称"""
    os.chdir(sys.path[0])  #进入保存日志路径(脚本路径)
    with open("pa_log.log",'a') as lf:
        lf.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
                + "," + url + "," + name + "\n")
        lf.close
    # os.chdir(re_path)   #返回保存套图路径

def timerJ(path=''):
            """装饰器：进程计时器"""
            def pass_(func):
                @wraps(func)
                def watchdog(*args, **kwargs):
                    starttime = time.time()
                    print('开始执行多进程爬虫！下载文件保存路径：%s'%path)
                    func(*args, **kwargs)
                    print('所有任务进程完成，用时 %d 秒。'%(time.time()-starttime))
                return watchdog
            return pass_

def timerX(func):
    """装饰器：线程计时器"""
    @wraps(func)
    def watchdog(*args, **kwargs):
        starttime = time.time()
        # print('开始执行多线程爬虫！')
        func(*args, **kwargs)
        sys.stdout.write('\n本进程任务完成，用时 %d 秒。'%(time.time()-starttime))
    return watchdog

def progress(func):
    """装饰器：输出显示任务完成进度条"""
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        threadlist = args[0]
        n = len(threadlist)
        i = 1
        for t in threadlist:		#遍历线程列表
            #百分比进度条效果
            x = (i / n) * 100   #计算当前完成任务数占总任务数的百分比
            a = 40*(x/100)      #计算进度条中表示已完成任务的亮条部分的数值
            b = 40 - a          #计算进度条中表示未完成任务的空格部分的数值
            # sys.stdout.write('\r>>convert image %d/%d'%(i,x)+'%')
            sys.stdout.write('\r|%s%s |   %d/%d    %d%%     ' % (int(a) * '▇', int(b) * ' ', i, n, x))

            t.setDaemon(True)       #守护模式（后台）
            # t.setDaemon(False)  #用户模式线程
            t.start()  #开启线程
            i += 1  #完成任务数加 1
        t.join()    #在此处阻塞主线程，等待全部子线程结束后再执行主线程

        #return func(*args,**kwargs)    #返回func就等同于func被调用。这句不运行就是不调用原函数了
                                        #相当于用装饰器替代了被装饰的函数
    return wrapped_function

# @progress   #进度条装饰器
def thread_start(threadList):
    """开启线程列表里的任务线程"""
    for t in threadList:		#遍历线程列表
        t.setDaemon(True)       #守护模式（后台）
        # t.setDaemon(False)      #用户模式线程
        t.start()               #开启线程
    t.join()  #作用为阻塞主线程，等待 t 线程结束后再执行主线程  