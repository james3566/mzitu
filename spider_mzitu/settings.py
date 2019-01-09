#python/spider/setings.py
"""目标网站、数据保存、代理服务器等相关信息"""

class Mzitu():
    """mzitu.com的相关设置"""
    
    def __init__(self):

        self.Hostreferer = {
                        'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
                        'Referer':'http://www.mzitu.com/'}
        
        self.path = "/python/photos/mzitu/"


class Mmjpg():
    """mmjpg.com的相关设置"""
    
    def __init__(self):

        self.Hostreferer = {
                #'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',已失效
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                'Referer':'http://www.mmjpg.com/'
                }
        
        self.path = "/python/photos/mmjpg/"


proxies = {
    "http": "http://119.101.116.107:9999",
    "http": "http://111.179.20.105:9999",
    "http": "http://49.84.152.31:26037",
    }