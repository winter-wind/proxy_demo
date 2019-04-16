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
        #创建实例,供后面其它方法使用
        self.redis = RedisClient()
     
    #异步请求   
    """
            通过async关键字定义一个协程（coroutine），协程也是一种对象。协程不能直接运行，需要把协程加入到事件循环（loop），
            由后者在适当的时候调用协程。asyncio.get_event_loop方法可以创建一个事件循环，
            然后使用run_until_complete将协程注册到事件循环，并启动事件循环

    """
    async def test_single_proxy(self,proxy):
        """
                测试单个代理
        :param proxy: 单个代理
        :return: None
        """
        #verify_ssl (布尔类型) –对HTTPS请求验证SSL证书(默认是验证的)。如果某些网站证书无效的话也可禁用。(该参数可选)
        conn = aiohttp.TCPConnector(verify_ssl = False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print("正在测试",proxy)
                #with:对try…expect…finally语法的一种简化，并且提供了对于异常非常好的处理方式
                async with session.get(TEST_URL,proxy=real_proxy,timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:#获取状态码
                        self.redis.max(proxy)#调用方法：db.py=>max(proxy)  该代理分数100
                        print('代理可用',proxy)
                    else:
                        self.redis.decrease(proxy)#调用方法：  该代理分数减1
                        print('请求响应码不合法',proxy)
            except (ClientError,ClientConnectionError,TimeoutError,AttributeError):
                self.redis.decrease(proxy)#如果出错，调用方法：  该代理分数减1
                print('代理请求失败',proxy)
                
    def run(self):
        """
        测试主函数
        :return:None
        """
        print('测试器开始运行')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()#调用异步处理
            #批量测试
            for i in range(0,len(proxies),BATCH_TEST_SIZE):
                #上面是获取0到proxies以BATCH_TEST_SIZE为步长分段
                #例：range(0,100,5)就分成0-5，5-10以此类推
                #显示分段内容例proxies[0:0,5]就显示前5个，如果是[1:1,5]就显示后5个
                test_proxies = proxies[i:i + BATCH_TEST_SIZE]
                #从test_proxies中获取proxy，放入测试单个代理方法中测试
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                """
                wait 的使用常见场景：开了 3 个协程，它们分别用不同方法去做同一件事，
                                        你只需要它们其中一个完成就可以了，这时，你可以使用 wait。
                """
                loop.run_until_complete(asyncio.wait(tasks))#程序开始执行
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误',e.args)
            
