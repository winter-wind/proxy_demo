# coding:gbk
from setting import TEST_URL,VALID_STATUS_CODES,BATCH_TEST_SIZE
from db import RedisClient
from aiohttp import ClientError
import aiohttp
import asyncio
import time
from aiohttp.client_exceptions import ClientConnectionError 
class Tester(object):
    def __init__(self):
        #����ʵ��,��������������ʹ��
        self.redis = RedisClient()
     
    #�첽����   
    """
            ͨ��async�ؼ��ֶ���һ��Э�̣�coroutine����Э��Ҳ��һ�ֶ���Э�̲���ֱ�����У���Ҫ��Э�̼��뵽�¼�ѭ����loop����
            �ɺ������ʵ���ʱ�����Э�̡�asyncio.get_event_loop�������Դ���һ���¼�ѭ����
            Ȼ��ʹ��run_until_complete��Э��ע�ᵽ�¼�ѭ�����������¼�ѭ��

    """
    async def test_single_proxy(self,proxy):
        """
                ���Ե�������
        :param proxy: ��������
        :return: None
        """
        #verify_ssl (��������) �C��HTTPS������֤SSL֤��(Ĭ������֤��)�����ĳЩ��վ֤����Ч�Ļ�Ҳ�ɽ��á�(�ò�����ѡ)
        conn = aiohttp.TCPConnector(verify_ssl = False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print("���ڲ���",proxy)
                #with:��try��expect��finally�﷨��һ�ּ򻯣������ṩ�˶����쳣�ǳ��õĴ���ʽ
                async with session.get(TEST_URL,proxy=real_proxy,timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:#��ȡ״̬��
                        self.redis.max(proxy)#���÷�����db.py=>max(proxy)  �ô������100
                        print('�������',proxy)
                    else:
                        self.redis.decrease(proxy)#���÷�����  �ô��������1
                        print('������Ӧ�벻�Ϸ�',proxy)
            except (ClientError,ClientConnectionError,TimeoutError,AttributeError):
                self.redis.decrease(proxy)#����������÷�����  �ô��������1
                print('��������ʧ��',proxy)
                
    def run(self):
        """
        ����������
        :return:None
        """
        print('��������ʼ����')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()#�����첽����
            #��������
            for i in range(0,len(proxies),BATCH_TEST_SIZE):
                #�����ǻ�ȡ0��proxies��BATCH_TEST_SIZEΪ�����ֶ�
                #����range(0,100,5)�ͷֳ�0-5��5-10�Դ�����
                #��ʾ�ֶ�������proxies[0:0,5]����ʾǰ5���������[1:1,5]����ʾ��5��
                test_proxies = proxies[i:i + BATCH_TEST_SIZE]
                #��test_proxies�л�ȡproxy��������Ե����������в���
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                """
                wait ��ʹ�ó������������� 3 ��Э�̣����Ƿֱ��ò�ͬ����ȥ��ͬһ���£�
                                        ��ֻ��Ҫ��������һ����ɾͿ����ˣ���ʱ�������ʹ�� wait��
                """
                loop.run_until_complete(asyncio.wait(tasks))#����ʼִ��
                time.sleep(5)
        except Exception as e:
            print('��������������',e.args)
            
