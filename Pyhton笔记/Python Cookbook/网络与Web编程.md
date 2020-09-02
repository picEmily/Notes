# 基础类库

## socket  库

文档：https://docs.python.org/3/library/socket.html

参考：https://www.cnblogs.com/wrxblog/p/9777700.html

Cpython 解释器能调用系统调用的函数

Python Socket 库直译了UNIX系统的 Socket API，就像 C 中 ``<sys/socket.h>``

### 常用函数和方法

- socket()
- ``socket.bind()``：将套接字绑定到 *address*
- ``socket.listen()``：启动一个服务器用于监听连接
- ``socket.accept()``：接受一个连接。此 scoket 必须绑定到一个地址上并且监听连接
- ``socket.connect()``：连接到 *address* 处的远程套接字
- ``socket.connect_ex()``
- ``socket.send()/socket.sentall()``:发送数据给套接字。本套接字必须已连接到远程套接字
- ``socket.recv()``：从套接字接收数据。返回值是一个字节对象，表示接收到的数据
- ``socket.close()``

<img src="C:\Users\wangd\Desktop\Python Cookbook\Socket API调用顺序.png" style="zoom:50%;" />

**sever 与 client 通信**

1. server: socket 实例 调用 ``accept() `` 方法， client: socket 实例 调用 ``connect()`` 方法建立连接
2. server 与 client 的 socket 能够调用 ``recv()`` 和 ``send()`` 收发数据了

### 套接字的协议族

- AF_\*: address family 地址（协议族）
    - socket.AF_UNIX
    - socket.AF_INET：网络地址 (host, port)
    - socket.AF_INET6
    - socket.BLUETOOTH：蓝牙地址
    - ...
- SOCK_\*: 套接字类型
    - socket.SOCK_STREAM：面向连接的 socket，基于TCP
    - socket.SOCK_DGRAM：(Data Gram)无保障的 socket，面向字节流，基于UDP
    - socket.SOCK_RAW
    - socket.SOCK_RDM
    - socket.SOCK_SEQPACKET

```python
# 通过 socket 库实现服务器
from socket import socket, AF_INET, SOCK_STREAM
def echo_handler(address, client_sock): 
    print('Got connection from {}'.format(address)) 
    while True: 
        msg = client_sock.recv(8192)			# buffer size:8192  
        if not msg: 
            break 
        client_sock.sendall(msg) 
    client_sock.close()

def echo_server(address, backlog=5): 
    sock = socket(AF_INET, SOCK_STREAM)			# 面向网络，TCP协议
    sock.bind(address) 						   # 套接字绑定地址
    sock.listen(backlog) 					   # 开始监听连接, backlog指定系统允许暂未 accept 的连接数，超过后将拒绝新连接
    while True: 
        client_sock, client_addr = sock.accept()	# 接收客户端套接字
        echo_handler(client_addr, client_sock)		# 处理客户端套接字
        
if __name__ == '__main__': 
    echo_server(('', 20000))					# 地址：localhost:20000

```



## multiprocessing 库

进程间通信可以使用 ``multiprocessing.connection``，比如实现 PRC 的时候

``multiprocessing.connection`` 建立在 ``socket`` 库上

主要关注 ``Connection``,  ``Listener``,  ``Client`` 三个类

- ``Listener``: This is a wrapper for a bound socket which is 'listening' for connections

  - ``Listener`` 类，其实例用来做 server 的 socket
  - ``server_socket = Listener(address) `` Listener 对象实际上是把 socket 对象包了一层。实例在初始化的时候就执行了 ``bind()``, ``listen()``，``server_socket._listener`` 是一个 socket 对象
  - ``server_socket.accept()`` 实际上调用了 ``server_socket._listener.accept()``
  
- ``Connection``
- ``Connection`` 类，封装了一个调用了 ``connect()`` 方法的 socket
- ``Client``: Returns a connection (socket 对象) to the address of a `Listener`
  - ``Client`` 方法，返回 Connection 对象的实例，也就是用来做 client 的 socket


# SocketServer  库

封装了 ``Socket`` API，提供简单的服务器 API

封装了多线程/进程 API

```
# server
        +------------+
        | BaseServer |
        +------------+
              |
              v
        +-----------+        +------------------+
        | TCPServer |------->| UnixStreamServer |
        +-----------+        +------------------+
              |
              v
        +-----------+        +--------------------+
        | UDPServer |------->| UnixDatagramServer |
        +-----------+        +--------------------+
```



```
# handler

        +------------+			+------------------------+
        | BaseServer | ------->  | DatagramRequestHandler |
        +------------+			+------------------------+
              |
              v
        +----------------------+        
        | StreamRequestHandler |
        +----------------------+        
```

# cgi 库

创建简单的 REST 接口

WSGI 标准：web程序必须是一个可调用对象（实现 ``__call__()`` 方法），且可接受两个参数：environ（环境参数）和start_response（回调函数）

实现了WSGI规范的接口函数，不用考虑底层实现，可以直接响应并处理http请求，通过start_response返回**响应状态**和**响应头**，通过返回值返回**响应主体**。

# RPC

## 阻塞式，单线程

调用远程主机的 python 程序。比如我可以把一个远程主机当数据库。

实际上也是通过 socket 通信

构造一个 ``handle_connection(func, client_socket)`` 方法，client_socket 把参数发送给 server_socket ，server_socket 通过执行 ``func(*args, **kwargs)``，再把结果发送给 client_socket 

## 异步

concurrentfuture???

## 利用消息队列

mq里存了什么

client和server如何存取参数和结果？

- 维护两个队列：args_queue[], result_queue[]

zeromq

redis

```
# 示意图

Client             		Server   
------------------------------------------          
client              worker(thread)     
         \        /
cleint  -- queue    
         /        \
client              worker(thread)
```

