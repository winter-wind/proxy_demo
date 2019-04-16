# coding:gbk
import requests
from requests.exceptions import ConnectionError

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}

def get_page(url,options={}):
    """
    抓取代理
    ：param url：
    ：param options：
    ：return：
    """
    #dict生成字典，**options传入的为键值对类似于base_headers变量内容
    headers = dict(base_headers,**options)
    print('正在抓取',url)
    try:
        #打开网页并传入参数
        response = requests.get(url,headers=headers)
        print('抓取成功',url,response.status_code)
        #获取网页状态码，成功返回return
        if response.status_code ==200:
            return response.text
    except ConnectionError:
        print('抓取失败',url)
        return None
