# coding:gbk
from flask import Flask, g
from db import RedisClient

__all__ = ['app']
app = Flask(__name__)

def get_conn():
    if not hasattr(g,'redis'):#g�����Ƿ����redis����
        g.redis = RedisClient()#���û����RedisClient����g.redis
        return g.redis#����
    
@app.route('/')
def index():
    return '<h2>welcome to Proxy Pool System</h2>'

@app.route('/random')
def get_proxy():
    """
    ��ȡ������ô���
    :return: �������
    """
    conn = get_conn()
    return conn.random()

@app.route('/count')
def get_countsz():
    """
    ��ȡ���������
    :return: ���������
    """
    conn = get_conn()
    return str(conn.count())

if __name__ == '__main__':
    app.run()