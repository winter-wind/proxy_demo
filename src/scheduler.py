# coding:gbk
from setting import TESTER_CYCLE,GETTER_CYCLE,API_HOST,API_PORT,TESTER_ENABLED,GETTER_ENABLED,API_ENABLED
from multiprocessing import Process
from api import app
from getter import Getter
from tester import Tester
import time

class Scheduler():
    def schedule_tester(self,cycle = TESTER_CYCLE):
        """
        定时测试代理
        """
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)#休眠时间
            
    def schedule_getter(self,cycle = GETTER_CYCLE):
        """
                    定时获取代理
        """
        print("==")
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)
            
    def schedule_api(self):
        """
        开启API
        """
        app.run(API_HOST,API_PORT)#可访问的ip和端口
        
    def run(self):
        print('代理池开始运行 ')
        
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()#并发线程
         
        """
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()  
            
        
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
        """