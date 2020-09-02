import pickle                                       # json 也行，就是一种编码方式
from multiprocessing.connection import Listener     # 封装了socket，用来监听连接
from threading import Thread

import json
import redis

class RPCHandler:
    """
    PRC处理器类
    """
    def __init__(self):
        self._function = {}     # key: function name, value: function

    def register_function(self, func):
        """
        params:
            function func
        """
        self._function[func.__name__] = func

    def handle_connection(self, redis_conn):
        """
        params:
            Socket connection

        """
        try:
            while True:
                # Receive a message
                if redis_conn.llen("request") == 0:
                    continue
                func_name, args, kwargs = json.loads(redis_conn.lpop("request"))
                # func_name, args, kwargs = connection.recv()
                print("[INFO] function: {0}, args: {1}, kwargs: {2}".format(func_name, str(args), str(kwargs)))
                # Run the RPC and send a response
                resp = self._function[func_name](*args, **kwargs)
                print("[INFO] Result: " + json.dumps(resp))
                redis_conn.rpush("response", json.dumps(resp))
        except EOFError:
            # try...except... 是判断文件结束符 EOF 的常用方法（判断输入结束）
            # 或者用 stdin
            pass

def rpc_server(handler, db):
    redis_conn = redis.StrictRedis(host='localhost', port=6379, db=db)
    print("Server client starts listening...")
    while True:
        try:
            handler.handle_connection(redis_conn)
        except:
            pass


class RemoteFunc():
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def sub(a, b):
        return a - b


if __name__ == "__main__":
    # run server
    from threading import Thread
    # Register with a handler 
    handler = RPCHandler() 
    handler.register_function(RemoteFunc.add)
    t = Thread(target=rpc_server, args=(handler, 0)) 
    t.start()

    handler2 = RPCHandler() 
    handler2.register_function(RemoteFunc.sub)
    t2 = Thread(target=rpc_server, args=(handler2, 1)) 
    t2.start()
