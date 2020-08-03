# celery

loglevel
debug: 啥都出
info： 一般情况

来自官方文档
https://www.linode.com/docs/development/python/task-queue-celery-rabbitmq/

https://docs.celeryproject.org/en/latest/getting-started/brokers/redis.html

注册此app并连接消息队列
```python3
## celerytask.py

# Create the app and set the broker location (redis)

# 方法一
app = Celery(__name__, broker='redis://localhost:6379/0',
              backend='redis://localhost:6379/0')

# 方法二
app = Celery(__name__)
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

# 设置option
app.conf.broker_transport_options = {'visibility_timeout': 3600}
```

注册celery task
```python3
@app.task
def task():
	pass
```

启动
```bash
## redis
redis-server

## celery worker
celery -A celerytask worker --loglevel=info
```

## 常用方法
```python3
# task 是之前注册过的一个celery task
t = task.delay() # t得到这个task对象
t.ready() # return True/False 是否完成
t.get() # 得到函数的返回值

# AsynResult 对象
```

## windows 的奇怪错误
https://github.com/celery/celery/issues/4081
两个方法
一个是启动celery worker时候加上``-P eventlet``
一个是在注册app的文件里加上
```python
import os
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
```

4.0 的问题
https://blog.csdn.net/libing_thinking/article/details/78622943

https://celery.readthedocs.io/en/latest/faq.html#is-celery-dependent-on-pickle

https://stackoverflow.com/questions/41956480/how-to-pass-large-chunk-of-data-to-celery/46072582#46072582

celerty.task 传入database对象是不好的
http://tbwisk.github.io/2016/08/26/celeryPractice.html