#Redis数据库地址
REDIS_HOST = '192.168.1.26'
#端口
REDIS_PORT = '6379'
#密码
REDIS_PASSWORD = None

#最大分数可连接
MAX_SCORE = 100
#最小分数不可连接
MIN_SOCRE = 0
#初始分数
INITIAL_SCORE = 10

#有序集合的键名
REDIS_KEY = 'proxies'

# 代理池数量界限
POOL_UPPER_THRESHOLD = 50000

# 测试API，建议抓哪个网站测哪个
TEST_URL = 'https://www.163.com'
#测试网站返回的状态码
VALID_STATUS_CODES = [200, 302]
# 最大批测试量
BATCH_TEST_SIZE = 5

# API配置
API_HOST = '0.0.0.0'
API_PORT = 5555

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 检查周期
TESTER_CYCLE = 2
# 获取周期
GETTER_CYCLE = 3