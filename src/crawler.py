# coding:gbk
import json
from utils import get_page
from pyquery import PyQuery as pq

class ProxyMetaclass(type):#元类
    def __new__(cls,name,bases,attrs):#attrs是一个字典
        count = 0
        attrs['__CrawlFunc__'] = []#在这个字典中创建一个键为'__CrawlFunc__'，值为空的列表字典
        for k,v in attrs.items():#items()以列表返回可遍历的(键, 值) 元组数组
            #将获取到的类和方法进行比较，名字是否包含'crawl_'，如果包含就添加到CrawlFunc键中，并记入到总数的键里
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls,name,bases,attrs)
        
class Crawler(object,metaclass=ProxyMetaclass):
    def get_proxies(self,callback):
        proxies = []
        #eval() 函数用来执行一个字符串表达式，并返回表达式的值，这里是执行一个方法
        for proxy in eval('self.{}()'.format(callback)):
                            #format（）：将callback的值作为方法名（crawl_daili66等）组合成“self.callback()”
            print('成功获取到代理',proxy)
            proxies.append(proxy)
        return proxies
    
    def crawl_daili66(self,page_count=1):
        """
                     获取代理66
        :param page_count: 页码
        :return: 代理
        """    
        print('开始收集daili66')
        start_url = 'http://www.66ip.cn/{}.html'
        #组合字符串，将url中的{}通过.format(page)赋值，用循环从1到5页
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:#遍历网页页码
            print('Crawling',url)
            html = get_page(url)#获取网页状态码
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':' .join([ip,port])
                
    def crawl_proxy360(self):
        """
                    获取Proxy360
        :return: 代理
        """    
        print('开始收集proxy360')
        start_url = 'http://www.proxy360.cn/Region/China'
        print('Crawling',start_url)
        html = get_page(start_url)
        if html:
            doc = pq(html)
            lines = doc('div[name="list_proxy_ip"]').items()
            for line in lines:
                ip = line.find('.tbBottomLine:nth-child(1)').text()
                port = line.find('.tbBottomLine:nth-child(2)').text()
                yield ':' .join([ip,port])

    def crawl_goubanjia(self):
        """
                    获取Goubanjia
        :return: 代理
        """
        print('开始收集goubanjia')
        start_url = 'http://www.goubanjia.com/free/gngn/index.shtml'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            tds = doc('td.ip').items()
            for td in tds:
                td.find('p').remove()
                yield td.text().replace(' ','')