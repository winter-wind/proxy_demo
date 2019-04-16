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
    ץȡ����
    ��param url��
    ��param options��
    ��return��
    """
    #dict�����ֵ䣬**options�����Ϊ��ֵ��������base_headers��������
    headers = dict(base_headers,**options)
    print('����ץȡ',url)
    try:
        #����ҳ���������
        response = requests.get(url,headers=headers)
        print('ץȡ�ɹ�',url,response.status_code)
        #��ȡ��ҳ״̬�룬�ɹ�����return
        if response.status_code ==200:
            return response.text
    except ConnectionError:
        print('ץȡʧ��',url)
        return None
