import pickle                                       # json 也行，就是一种编码方式
from multiprocessing.connection import Listener     # 封装了socket，用来监听连接
from threading import Thread

import json

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

    def handle_connection(self, connection):
        """
        params:
            Socket connection

        """
        try:
            while True:
                # Receive a message
                func_name, args, kwargs = json.loads(connection.recv())
                # func_name, args, kwargs = connection.recv()
                print("[INFO] function: {0}, args: {1}, kwargs: {2}".format(func_name, str(args), str(kwargs)))
                # Run the RPC and send a response
                resp = self._function[func_name](*args, **kwargs)
                print("[INFO] Result: " + json.dumps(resp))
                connection.send(json.dumps(resp))
        except EOFError:
            # try...except... 是判断文件结束符 EOF 的常用方法（判断输入结束）
            # 或者用 stdin
            pass

def rpc_server(handler, address, authkey):
    socket = Listener(address, authkey=authkey)
    while True:
        client = socket.accept()
        # handle_connection(client)
        t = Thread(target=handler.handle_connection, args=(client, ))   
        t.daemon = True
        t.start()

class RemoteFunc():
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def sub(a, b):
        return a - b


if __name__ == "__main__":
    # Register with a handler 
    handler = RPCHandler() 
    handler.register_function(RemoteFunc.add) 
    handler.register_function(RemoteFunc.sub)
    # run server
    rpc_server(handler, ("", 2333), authkey=b'funkymonkey')
