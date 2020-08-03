文档： https://pypi.org/project/redis/
# Redis 基础
## Redis 数据类型
（**重点**）：区别其他KV数据库的很大一个优点（值有多种类型！）
- string
- set(unordered)
- list
- ordered set
- hash
	- kv pair (就是键可以是一个hashmap)

## Redis 内存划分
https://www.cnblogs.com/kismetv/p/8654978.html
### Redis占用了哪些内存
#### 1、数据
- 作为数据库，数据是最主要的部分；这部分占用的内存会统计在**used_memory**中。
- Redis使用键值对存储数据，其中的值（对象）包括5种类型，即字符串、哈希、列表、集合、有序集合。这5种类型是Redis对外提供的。
- (**bonus**)实际上，在Redis内部，每种类型可能有2种或更多的内部编码实现；此外，Redis在存储对象时，并不是直接将数据扔进内存，而是会对对象进行各种包装：如redisObject、SDS等；

#### 2、进程本身运行需要的内存
- Redis主进程本身运行肯定需要占用内存，如代码、常量池等等；这部分内存大约几兆，在大多数生产环境中与Redis数据占用的内存相比可以忽略。这部分内存不是由jemalloc分配，因此不会统计在used_memory中。
- 补充说明：除了主进程外，Redis创建的子进程运行也会占用内存，如Redis执行AOF、RDB重写时创建的子进程。当然，这部分内存不属于Redis进程，也不会统计在used_memory和used_memory_rss中。

#### 3、缓冲内存（TODO）
缓冲内存包括客户端缓冲区、复制积压缓冲区、AOF缓冲区等；其中，客户端缓冲存储客户端连接的输入输出缓冲；复制积压缓冲用于部分复制功能；AOF缓冲区用于在进行AOF重写时，保存最近的写入命令。在了解相应功能之前，不需要知道这些缓冲的细节；这部分内存由jemalloc分配，因此会统计在used_memory中。

#### 4、内存碎片
- 内存碎片是Redis在分配、回收物理内存过程中产生的。例如，如果对数据的更改频繁，而且数据之间的大小相差很大，可能导致redis释放的空间在物理内存中并没有释放，但redis又无法有效利用，这就形成了内存碎片。内存碎片不会统计在used_memory中。
- 内存碎片的产生与对数据进行的操作、数据的特点等都有关；此外，与使用的内存分配器也有关系：如果内存分配器设计合理，可以尽可能的减少内存碎片的产生。后面将要说到的jemalloc便在控制内存碎片方面做的很好。
- 如果Redis服务器中的内存碎片已经很大，可以通过安全重启的方式减小内存碎片：因为重启之后，Redis重新从备份文件中读取数据，在内存中进行重排，为每个数据重新选择合适的内存单元，减小内存碎片。

### Redis 内存分配细节
#### 内存分配器
Redis在编译时便会指定内存分配器；内存分配器可以是 libc 、jemalloc或者tcmalloc，默认是jemalloc。

**jemalloc**作为Redis的默认内存分配器，在减小内存碎片方面做的相对比较好。jemalloc在64位系统中，将内存空间划分为小、大、巨大三个范围；每个范围内又划分了许多小的内存块单位；当Redis存储数据时，会选择大小最合适的内存块进行存储。
#### redisObject
Redis对象有5种类型；无论是哪种类型，Redis都不会直接存储，而是通过**redisObject**对象进行存储。

(TODO) 五种数据结构在redis里面是怎么实现的。

#### 简单动态字符串SDS
```C
struct sdshdr {
    int len;
    int free;
    char buf[];
};
```
- buf表示字节数组，用来存储字符串
- len表示buf已使用的长度
- free表示buf未使用的长度


# Redis commands
存储方式; key-value

启动redis客户端
> redis-cli

在客户端中
> ping


备份和恢复数据
> SAVE

操作key [Command][Key_name]
> SET key value
> GET key
> KEYS pattern 
> KEYS *
> flushdb 删除所有key

## Redis持久化
- **RDB**：在指定的时间间隔能对你的数据进行快照存储。dump文件。
- **AOF**：持久化方式记录每次对服务器写的操作,当服务器重启的时候会重新执行这些命令来恢复原始的数据,AOF命令以redis协议追加保存每次写的操作到文件末尾.Redis还能对AOF文件进行后台重写,使得AOF文件的体积不至于过大。

选择：
- 如果你只希望你的数据在服务器运行的时候存在,你也可以不使用任何持久化方式。
- 你也可以同时开启两种持久化方式, 在这种情况下, 当redis重启的时候会优先载入AOF文件来恢复原始的数据,因为在通常情况下AOF文件保存的数据集要比RDB文件保存的数据集要完整。
- AOF文件通常较大，RDB可能会在突然断电时丢失文件

## Redis cluster
- 不是一致性hash，是**hash槽**``CRC16(key) % 16384``
- 主节点互相通信，互相ping-pong判断是否可以连上，一半以上没有回应则启用备用节点
- 主从结构（官方实现：3主3从），异步复制策略

# 发布订阅
https://www.runoob.com/redis/redis-pub-sub.html

客户端订阅channel，新消息将推送到订阅该channel的客户端
订阅者可以订阅一个或多个频道，发布者向一个频道发送消息后，所有订阅这个频道的订阅者都将收到消息，而发布者也将收到一个数值，这个数值是收到消息的订阅者的数量。订阅者只能收到自它开始订阅后发布者所发布的消息，之前发布的消息呢，就不可能收到了。

# 在python中使用redis
## 连接，crud

## pub/sub
- ``publish()``
将信息发布到指定的频道
- ``subscribe()``
订阅一个或者多个频道
- ``psubscribe()``
订阅一个或多个符合特定模式的频道
- ``unsubscribe()``
退订一个或多个频道
- ``punsubscribe()``
退订一个或多个特定模式的频道

item，是类似于：{'pattern': None, 'type': 'message', 'channel': 'liao', 'data': '300033 1'}
```python3
# coding=utf-8

import redis
r = redis.Redis()  # 连接
p = r.pubsub()  # 订阅模式
p.subscribe('test')  # 订阅

for item in p.listen():    # 监听状态，有消息就拿过来
    if item['type'] == 'message':  
		print item['channel']
        print item['data']
p.unsubscribe('test')
```

发布端
```python3
# coding=utf-8

import redis
r = redis.Redis()
while True:
    input = raw_input("publish:")
    if input == 'over':
        print '停止发布'
        break;
    r.publish('test', input)
```

# 实践：redis做任务队列
- redis怎么做任务队列（存什么）
- 怎么实现发布订阅
- 包装成装饰器（类似celery）

# Redis击穿
参见缓存穿透，击穿，雪崩