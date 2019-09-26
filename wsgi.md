# wsgi
https://www.jianshu.com/p/c66d3adeaaed
https://blog.csdn.net/li_101357/article/details/52748323
- webserver gateway interface，定义webserver和python的交互方式
- 是一个server，处理http，接受用户请求，找到app对象，与app/framework通信。
- WSGI将Web组件分成了三类：Web 服务器（WSGI Server）、Web中间件（WSGI Middleware）与Web应用程序（WSGI Application）。
- 我们关系python web app：接受request，然会response。剩下的包括处理http协议，把python代码转化为req，resp，都交给wsgi服务器来进行

# gunicorn, gevent
- flask，Django都自带WSGI server，但是性能一般
- 所以我们用其他的服务来实现wsgi：gunicorn(支持wsgi的http server，支持gevent协程)
- gevent是一个基于libev的并发库。它为各种并发和网络相关的任务提供了整洁的API。gunicorn对于“协程”也就是Gevent的支持非常好。

替换flask自带wsgi的方式
- 写gunicorn配置
- 通过gunicorn启动（替代flask run）

gunicorn配置
https://blog.csdn.net/y472360651/article/details/78538188
https://www.jianshu.com/p/69e75fc3e08e
https://www.jianshu.com/p/fecf15ad0c9a

# nginx
https://www.cnblogs.com/wcwnina/p/8728391.html
-反向代理：接受客户端的请求，并分配给服务器，同时接受服务器响应
![代理](https://images2018.cnblogs.com/blog/1202586/201804/1202586-20180406180130452-1246060303.png)

# 性能测试
https://www.jianshu.com/p/8a4e85a0ef33
[系统吞吐量（TPS）、用户并发量、性能测试概念和公式](http://www.ha97.com/5095.html "系统吞吐量（TPS）、用户并发量、性能测试概念和公式")
[HTTP压测工具之wrk](https://www.jianshu.com/p/ac185e01cc30)
- 测量服务器可承受的QPS: ``QPS=并发数/平均响应时间``

```
-c, --connections:  总的连接数（每个线程处理的连接数=总连接数/线程数）

-d, --duration:        测试的持续时间，如2s(2second)，2m(2minute)，2h(hour)

-t, --threads:         需要执行的线程总数

-s, --script:          执行Lua脚本，这里写lua脚本的路径和名称，后面会给出案例

-H, --header:      需要添加的头信息，注意header的语法，举例，-H “token: abcdef”，说明一下，token，冒号，空格，abcdefg（不要忘记空格，否则会报错的）。

--latency:     显示延迟统计信息

--timeout:     超时的时间

wrk -t12 -c400 -d30s http://127.0.0.1:8080/index.html
```

```bash 
./wrk -t4 -c400 -d60s --latency -s ../post.lua http://172.22.22.192:8097/api/v1/chinese_gec
```

```lua
# post.lua
-- example HTTP POST script which demonstrates setting the
-- HTTP method, body, and adding a header

wrk.method = "POST"
wrk.body   = "sentence=俗话说，走路不知道骑马的幸苦。"
wrk.headers["Content-Type"] = "application/x-www-form-urlencoded"
```

wrk.headers["Content-Type"] = "application/json"

[实战](https://www.jianshu.com/p/26593d8c67be)

```
# 看硬件运行情况
top
u wangziqi
d 1

# gpu 占用和线程
watch -n 1 -d nvidia-smi
watch -n 1 -d ps -x

# wrk 发请求
./wrk -t4 -c400 -d60s --latency -s ../post.lua http://172.22.22.15:8097/api/v1/chinese_gec
```

cat /usr/local/cuda/version.txt
cat /proc/driver/nvidia/version

# gunicorn的四种模式
文档：https://docs.gunicorn.org/en/stable/design.html

server model: 
pre-fork woker model: A central master process that manages a set of worker processes.
master process 轮询每个子进程，监听信号。

worker 模式：
sync: synchronous worker class. 同步：每次只响应一个请求
async: Greenlets,eventlet,gevent, 多线程，异步（异步是实现多线程的一种手段）
tornado: 不推荐
AsyncIO: