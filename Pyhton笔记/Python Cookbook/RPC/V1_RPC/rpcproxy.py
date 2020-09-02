"""
用来传送请求的代理类
"""

import pickle
import json

class RPCProxy:
    def __init__(self, connection):
        self._connection = connection
    
    def __getattr__(self, name):
        # python 查找属性/方法 会调用 __getattr__()
        # 这里给 RPCProxy 类添加了方法
        print("[DEBUG] " + str(type(name)))     # str
        def do_rpc(*args, **kwargs): 
            self._connection.send(json.dumps((name, args, kwargs))) 
            result = json.loads(self._connection.recv()) 
            if isinstance(result, Exception): 
                raise result 
            return result
        return do_rpc

if __name__ == "__main__":
    from multiprocessing.connection import Client
    c = Client(('', 2333), authkey=b'funkymonkey')
    proxy = RPCProxy(c)
    # 调用 proxy.add(), proxy 一看自己没有 add 方法
    # 就调用 __getattr__()
    # __getattr__() 在这里返回 do_rpc() 的返回值
    print(proxy.add(2, 3))  