# socket
https://www.jb51.net/article/50858.htm
https://www.cnblogs.com/huihui0708/p/8594817.html
https://www.cnblogs.com/dpf-learn/p/8028088.html

## python 语言实现
``socket(family,type[,protocal])``使用给定的**地址族、套接字类型、协议编号**（默认为0）来创建套接字

family

| socket family          | 描述                                                                                                                                                                         |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| socket.AF_UNIX        | 只能够用于单一的Unix系统进程间通信                                                                                                                              |
| **socket.AF_INET**        | 服务器之间网络通信                                                                                                                                                    |
| socket.AF_INET6       | IPv6                                                                                                                                                                           |

| socket tpye                | 描述                                                                                   |
| ---------------------- | ------------------------------------------------------------------------------------------------------- |
| **socket.SOCK_STREAM**    | 流式socket , for **TCP  **                                                                                                                                                       |
| **socket.SOCK_DGRAM**     | 数据报式socket , for **UDP **                                                                                                                                                  |
| socket.SOCK_RAW       | 原始套接字，普通的套接字无法处理ICMP、IGMP等网络报文，而SOCKRAW可以；其次,SOCK_RAW也可以处理特殊的IPv4报文；此外，利用原始套接字，可以通过IP_HDRINCL套接字选项由用户构造IP头。 |
| socket.SOCK_SEQPACKET | 可靠的连续数据包服务  

1. TCP发送数据时，已建立好TCP连接，所以不需要指定地址。UDP是面向无连接的，每次发送要指定是发给谁。
2. 服务端与客户端不能直接发送列表，元组，字典。需要格式化字符串repr(data)。

| 描述            | 服务端socket函数                                                                                                      |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------- |
| s.bind(address)   | 将套接字绑定到地址,在AF_INET下,以元组（host,port）的形式表示地址.                                   |
| s.listen(backlog) | 开始监听TCP传入连接。backlog指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1，大部分应用程序设为5就可以了。 |
| s.accept()        | 接受TCP连接并返回（conn,address）,其中conn是新的套接字对象，可以用来接收和发送数据。address是连接客户端的地址。 |

| 描述                 | 客户端socket函数                                                                                   |
| ---------------------- | ------------------------------------------------------------------------------------------------------- |
| s.connect(address)     | 连接到address处的套接字。一般address的格式为元组（hostname,port），如果连接出错，返回socket.error错误。 |
| s.connect_ex(adddress) | 功能与connect(address)相同，但是成功返回0，失败返回errno的值。    

| 描述                               | 公共socket函数                                                                                                                                                                  |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| s.recv(bufsize[,flag])               | 接受TCP套接字的数据。数据以字符串形式返回，bufsize指定要接收的最大数据量。flag提供有关消息的其他信息，通常可以忽略。             |
| s.send(string[,flag])                | 发送TCP数据。将string中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于string的字节大小。                           |
| s.sendall(string[,flag])             | 完整发送TCP数据。将string中的数据发送到连接的套接字，但在返回之前会尝试发送所有数据。成功返回None，失败则抛出异常。              |
| s.recvfrom(bufsize[.flag])           | 接受UDP套接字的数据。与recv()类似，但返回值是（data,address）。其中data是包含接收数据的字符串，address是发送数据的套接字地址。       |
| s.sendto(string[,flag],address)      | 发送UDP数据。将数据发送到套接字，address是形式为（ipaddr，port）的元组，指定远程地址。返回值是发送的字节数。                            |
| s.close()                            | 关闭套接字。                                                                                                                                                                  |
| s.getpeername()                      | 返回连接套接字的远程地址。返回值通常是元组（ipaddr,port）。                                                                                                 |
| s.getsockname()                      | 返回套接字自己的地址。通常是一个元组(ipaddr,port)                                                                                                                 |
| s.setsockopt(level,optname,value)    | 设置给定套接字选项的值。                                                                                                                                                |
| s.getsockopt(level,optname[.buflen]) | 返回套接字选项的值。                                                                                                                                                      |
| s.settimeout(timeout)                | 设置套接字操作的超时期，timeout是一个浮点数，单位是秒。值为None表示没有超时期。一般，超时期应该在刚创建套接字时设置，因为它们可能用于连接的操作（如connect()） |
| s.gettimeout()                       | 返回当前超时期的值，单位是秒，如果没有设置超时期，则返回None。                                                                                         |
| s.fileno()                           | 返回套接字的文件描述符。                                                                                                                                                |
| s.setblocking(flag)                  | 如果flag为0，则将套接字设为非阻塞模式，否则将套接字设为阻塞模式（默认值）。非阻塞模式下，如果调用recv()没有发现任何数据，或send()调用无法立即发送数据，那么将引起socket.error异常。 |
| s.makefile()                         | 创建一个与该套接字相关连的文件  

![](https://images2018.cnblogs.com/blog/1258639/201803/1258639-20180318114052260-1357931949.png)

TODO: 
demo_1: 实现简单通信
https://www.cnblogs.com/huihui0708/p/8594817.html

**步骤**

| 步骤 | TCP客户端                        | TCP服务器                             |
| ------ | ----------------------------------- | ---------------------------------------- |
| 第一步 | 建立socket对象                  | 建立socket对象                       |
| 第二步 | 调用connect()建立一个和服务器的连接 | 设置socket选项（可选）           |
| 第三步 | 无                                 | 绑定到一个端口（也可以是一个指定的网卡） |
| 第四步 | 无                                 | 侦听连接                             |

**UDP连接**

| 步骤 | UDP            | TCP            |
| ------ | -------------- | -------------- |
| 第一步 | 建立socket对象 | 建立socket对象 |
| 第二步 | 设置socket选项 | 设置socket选项 |
| 第三步 | 绑定到一个端口 | 绑定到一个端口 |
| 第四步 | Recvfrom()     | listen()       |

demo_2: https://www.cnblogs.com/cnike/p/10726706.html
demo_3: 实现``requests.get()``

```python
import socket
url = 'www.sina.com.cn'
port = 80
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((url, port))
request_url = 'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n'
sock.send(request_url.encode())
response = b''
rec = sock.recv(1024)
while rec:
    response += rec
    rec = sock.recv(1024)s
```

demo_4: 简单的http服务器
https://www.cnblogs.com/dpf-learn/p/8028088.html


## c++ 实现