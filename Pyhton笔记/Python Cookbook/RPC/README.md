# V1

直接 socket 通信，借助 ``multiprocessing.connection`` 库封装了一下
本质收发消息 还是 ``socket.recv()`` 和 ``socket.send()`` 函数
rpcproxy 里面利用了 ``__getattr()__``，也就是 python 的动态特性，我要动态使用新的方法，所以用了子函数并返回函数（也就是闭包）

## Quick Starter

```bash
# 启动服务器
python rpcserver.py

# 启动客户端
python rpcclient.py
```

# V2

消息队列有两条
- request queue: 客户端是生产者,服务器是消费者。queue 里存要执行的函数和参数。
- response queue: 服务器是生产者,客户端是消费者。queue 里存执行的结果。

利用redis
- key: request, value:a fifo list
    - element: (fn_name, (args, kwargs))
- key: response, value: a fifo list
    - elemetn: (fn_name, result)

client 和 server 各自的线程都既发送也接收消息(和 v1 比起来只是多了 MQ)

## Quick Starter

```bash
# 启动redis
redis-server --port 6379

# 启动服务器
python rpcserver.py

# 启动客户端
python rpcclient.py
```

# V3

大体上和 v2 一样，但是把 client 的线程分成两种。有一个线程专门送参数，一个线程不断取结果。
这样的原因是
- 我不想 client 线程一直等着结果，被阻塞在计算步骤，而是发送异步任务。server 没必要拆成专门送结果和专门去参数计算的线程。
- 如果 server 崩了，redis 里面数据取不出来，可能会污染之后的操作


## Quick Starter

```bash
# 启动redis
redis-server --port 6379

# 启动服务器
python rpcserver.py

# 启动客户端
python rpcclient.py
```

# 版本迭代
- v1 直接RPC调用，等待 server 返回是阻塞的
- v2 client 和 server 各自的线程都既发送也接收消息(和 v1 比起来只是多了 MQ)
- v3 server 有多个工作线程不断完成：取参数，计算，发送结果 的过程。client 则是 有一个线程专门送参数，一个线程不断取结果



