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
        �ж��Ƿ�ﵽ�˴��������
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
            
    def run(self):
        print('��ȡ����ʼִ��')
        if not self.is_over_threshold():#��ﵽ�˴��������
            #��callback_label��0����ʼ����self.crawler.__CrawlFuncCount__����ȡ������վ������������
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                #�õ�һ��������վ����
                callback = self.crawler.__CrawlFunc__[callback_label]
                
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)
                    
                print("����")