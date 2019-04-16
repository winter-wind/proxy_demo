# coding:gbk
from flask import Flask, g
from db import RedisClient

__all__ = ['app']
app = Flask(__name__)

def get_conn():
    if not hasattr(g,'redis'):#g对象是否存在redis属性
        g.redis = RedisClient()#如果没有则RedisClient赋给g.redis
        return g.redis#返回
    
@app.route('/')
def index():
    return '<h2>welcome to Proxy Pool System</h2>'

@app.route('/random')
def get_proxy():
    """
    获取随机可用代理
    :return: 随机代理
    """
    conn = get_conn()
    return conn.random()

@app.route('/count')
def get_countsz():
    """
    获取代理池总数
    :return: 代理池总数
    """
    conn = get_conn()
    return str(conn.count())

if __name__ == '__main__':
    app.run()