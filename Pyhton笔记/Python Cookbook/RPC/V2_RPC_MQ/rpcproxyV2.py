"""
用来传送请求的代理类
"""

import pickle
import json
import redis

class RPCProxy:
    def __init__(self, redis_conn):
        self._redis_conn = redis_conn
    
    def __getattr__(self, name):
        # python 查找属性/方法 会调用 __getattr__()
        # 这里给 RPCProxy 类添加了方法
        # print("[DEBUG] " + str(type(name)))     # str
        
        def do_rpc(*args, **kwargs): 
            self._redis_conn.rpush("request", json.dumps((name, args, kwargs))) 
            if self._redis_conn.llen("response") > 0:
                result = json.loads(self._redis_conn.lpop("response")) 
                if isinstance(result, Exception): 
                    raise result 
            else:
                result = None
            return result
        return do_rpc

if __name__ == "__main__":
    # 调用 proxy.add(), proxy 一看自己没有 add 方法
    # 就调用 __getattr__()
    # __getattr__() 在这里返回 do_rpc() 的返回值
    import redis
    for _ in range(10):
        redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
        proxy = RPCProxy(redis_conn)
        print(proxy.add(5, 3))

        redis_conn2 = redis.StrictRedis(host='localhost', port=6379, db=1)
        proxy2 = RPCProxy(redis_conn2)
        print(proxy2.sub(2, 3))  
