文档： https://pypi.org/project/redis/
# redis
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