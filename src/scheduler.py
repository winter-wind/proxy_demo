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
        ��ʱ���Դ���
        """
        tester = Tester()
        while True:
            print('��������ʼ����')
            tester.run()
            time.sleep(cycle)#����ʱ��
            
    def schedule_getter(self,cycle = GETTER_CYCLE):
        """
                    ��ʱ��ȡ����
        """
        print("==")
        getter = Getter()
        while True:
            print('��ʼץȡ����')
            getter.run()
            time.sleep(cycle)
            
    def schedule_api(self):
        """
        ����API
        """
        app.run(API_HOST,API_PORT)#�ɷ��ʵ�ip�Ͷ˿�
        
    def run(self):
        print('����ؿ�ʼ���� ')
        
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()#�����߳�
         
        """
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()  
            
        
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
        """