# coding:gbk
from db import  RedisClient
from crawler import Crawler
from setting import POOL_UPPER_THRESHOLD

class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()
        
    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
            
    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshold():#否达到了代理池限制
            #从callback_label（0）开始遍历self.crawler.__CrawlFuncCount__（获取代理网站方法的总数）
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                #得到一个代理网站方法
                callback = self.crawler.__CrawlFunc__[callback_label]
                
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)
                    
                print("结束")