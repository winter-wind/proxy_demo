import redis
from error import PoolEmptyError
from setting import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD,REDIS_KEY
from setting import MAX_SCORE,MIN_SOCRE,INITIAL_SCORE 
from random import choice

class RedisClient(object):
    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis地址
        :param port: Redis端口
        :param password: Redis密码
        """
        #连接数据库
        self.db = redis.StrictRedis(host=host,port=port,password=password,decode_responses=True)
        
    def add(self,proxy,score=INITIAL_SCORE):
        """
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        if not self.db.zscore(REDIS_KEY,proxy):#proxy是否是REDIS_KEY成员
            return self.db.zadd(REDIS_KEY, {proxy:score})#将score和proxy加入REDIS_KEY中
            
    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果最高分数不存在，则按照排名获取，否则异常
        :return 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)#返回分数为100的代理
        if len(result):
            return choice(result)#返回一个列表，元组或字符串的随机项（需要导入random import choice）
        else:
            result = self.db.zrevrange(REDIS_KEY,0,100)#返回0-100分数的代理，从大到小排列
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError#返回空池异常，raise如果后面有语句将不执行
                
    def decrease(self,proxy):
        """
        代理值减一分，分数小于最小值，则代理删除
        :param proxy: 代理
        :return: 修改后的代理分
        """
        score = self.db.zscore(REDIS_KEY,proxy)
        if score and score >MIN_SOCRE:#如果有值并且比0大
            print('代理',proxy,'当前分数',score,'减1')
            return self.db.zincrby(REDIS_KEY,-1,proxy)#将proxy的值减1
        else:#否则移除
            print('代理',proxy,'当前分数',score,'移除')
            return self.db.zrem(REDIS_KEY,proxy)#移除
            
    def exists(self,proxy):
        """
        判断是否在
        :param proxy: 代理
        :return: 是否存在
        """
        #当proxy不在REDIS_KEY中是为None,None == None为真，not后为假，所以返回假
        return not self.db.zscore(REDIS_KEY,proxy) == None
        
    def max(self,proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return:设置结果
        """
        print('代理',proxy,'可用，设置为',MAX_SCORE)
        return self.db.zadd(REDIS_KEY,{proxy:MAX_SCORE})#如果代理可用更新分数为100
        
    def count(self):
        """
        获取数量
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY)#返回有序集合的数量
        
    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        #返回全部0-100分数的代理
        return self.db.zrangebyscore(REDIS_KEY,MIN_SOCRE,MAX_SCORE)
            
            
                
    

