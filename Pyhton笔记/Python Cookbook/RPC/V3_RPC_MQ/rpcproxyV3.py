"""
用来传送请求的代理类
"""

import pickle
import json
import redis

class RPCProxy:
    def __init__(self, redis_conn):
        self._redis_conn = redis_conn
    
    def send(self, name, *args, **kwargs):
        """
        被调用，发送参数
        """
        self._redis_conn.rpush("request", json.dumps((name, args, kwargs))) 

    def recv(self):
        """
        run forever，收取结果
        """
        while True:
            if self._redis_conn.llen("response") > 0:
                result = json.loads(self._redis_conn.lpop("response")) 
                if isinstance(result, Exception): 
                    raise result 
                print("[INFO] Receive result: " + str(result))

if __name__ == "__main__":
    # 调用 proxy.add(), proxy 一看自己没有 add 方法
    # 就调用 __getattr__()
    # __getattr__() 在这里返回 do_rpc() 的返回值
    import redis
    from threading import Thread

    redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
    proxy = RPCProxy(redis_conn)

    t = Thread(target=proxy.recv, args=()) 
    t.start()

    t2 = Thread(target=proxy.send, args=("add", 5, 3)) 
    t2.start()
