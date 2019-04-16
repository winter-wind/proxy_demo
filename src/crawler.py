# coding:gbk
import json
from utils import get_page
from pyquery import PyQuery as pq

class ProxyMetaclass(type):#Ԫ��
    def __new__(cls,name,bases,attrs):#attrs��һ���ֵ�
        count = 0
        attrs['__CrawlFunc__'] = []#������ֵ��д���һ����Ϊ'__CrawlFunc__'��ֵΪ�յ��б��ֵ�
        for k,v in attrs.items():#items()���б��ؿɱ�����(��, ֵ) Ԫ������
            #����ȡ������ͷ������бȽϣ������Ƿ����'crawl_'�������������ӵ�CrawlFunc���У������뵽�����ļ���
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls,name,bases,attrs)
        
class Crawler(object,metaclass=ProxyMetaclass):
    def get_proxies(self,callback):
        proxies = []
        #eval() ��������ִ��һ���ַ������ʽ�������ر��ʽ��ֵ��������ִ��һ������
        for proxy in eval('self.{}()'.format(callback)):
                            #format��������callback��ֵ��Ϊ��������crawl_daili66�ȣ���ϳɡ�self.callback()��
            print('�ɹ���ȡ������',proxy)
            proxies.append(proxy)
        return proxies
    
    def crawl_daili66(self,page_count=1):
        """
                     ��ȡ����66
        :param page_count: ҳ��
        :return: ����
        """    
        print('��ʼ�ռ�daili66')
        start_url = 'http://www.66ip.cn/{}.html'
        #����ַ�������url�е�{}ͨ��.format(page)��ֵ����ѭ����1��5ҳ
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:#������ҳҳ��
            print('Crawling',url)
            html = get_page(url)#��ȡ��ҳ״̬��
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':' .join([ip,port])
                
    def crawl_proxy360(self):
        """
                    ��ȡProxy360
        :return: ����
        """    
        print('��ʼ�ռ�proxy360')
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
                    ��ȡGoubanjia
        :return: ����
        """
        print('��ʼ�ռ�goubanjia')
        start_url = 'http://www.goubanjia.com/free/gngn/index.shtml'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            tds = doc('td.ip').items()
            for td in tds:
                td.find('p').remove()
                yield td.text().replace(' ','')