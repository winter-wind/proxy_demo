#Redis���ݿ��ַ
REDIS_HOST = '192.168.1.26'
#�˿�
REDIS_PORT = '6379'
#����
REDIS_PASSWORD = None

#������������
MAX_SCORE = 100
#��С������������
MIN_SOCRE = 0
#��ʼ����
INITIAL_SCORE = 10

#���򼯺ϵļ���
REDIS_KEY = 'proxies'

# �������������
POOL_UPPER_THRESHOLD = 50000

# ����API������ץ�ĸ���վ���ĸ�
TEST_URL = 'https://www.163.com'
#������վ���ص�״̬��
VALID_STATUS_CODES = [200, 302]
# �����������
BATCH_TEST_SIZE = 5

# API����
API_HOST = '0.0.0.0'
API_PORT = 5555

# ����
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# �������
TESTER_CYCLE = 2
# ��ȡ����
GETTER_CYCLE = 3