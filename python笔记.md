# python笔记
引用和复制                         
https://www.cnblogs.com/jiangzhaowei/p/5740913.html
作用域
https://www.cnblogs.com/summer-cool/p/3884595.html

# 引用和复制
- 传引用
- 浅复制
- 深复制

1.``b=a``让b和a指向同一片地址，所以改a，b也改了

```python3
a = [1,2,3]
b = a
a[0] = 0
print(b) # [0,2,3]
```
2.浅复制,表层被复制了，``a[1]`` 和 ``b[1]``还是指向的同一片地址

```python3
a = [1,[1,2,3],3]
b = a[:] 或者 b=list(a)
a[0] = 0
print(b) # [1,[1,2,3],3]

a[1][0] = 0
print(b) # [1,[0,2,3],3]
```
3.深复制，开辟了一片完全新的空间给b

```python3
a = [1,[1,2,3],3]
b = copy.deepcopy(a)
a[1][0] = 0
print(b) = [1,[1,2,3],3]
```

# 作用域
看文章 懒得记笔记了

# python 传参

# python 语言
## python 动态性

## python装饰器
### 装饰器
https://realpython.com/primer-on-python-decorators/   (还没看完)

一看就懂的example
```python3
def do_twice(func):
    def wrapper_do_twice():
        func()
        func()
    return wrapper_do_twice

@do_twice
def say_whee():
    print("Whee!")
```

需要参数的example
思路：``*args``, ``**kwargs``接受各种形式的参数
```python3
def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper_do_twice

@do_twice
def greet(name):
    print(f"Hello {name}")
```

returning values
```pyhton3
def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice

@do_twice
def return_greeting(name):
    print("Creating greeting")
    return f"Hi {name}"s
```

Introspection
```python3
import functools

def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice
```
### 其他
- @property
- @staticmethod
- @classmethod: 
	- 不用self，而用cls
	- 可以被类，子类直接调用，不用实例化

区别classmethod and staticmethod
staticmethod 不能访问类的属性

## 遍历
```python3
# zip用法
zip([iterable, ...])

>>> a = [1,2,3]
>>> b = [4,5,6]
>>> c = [4,5,6,7,8]
>>> zipped = zip(a,b)     # 返回一个对象
>>> zipped
<zip object at 0x103abc288>
>>> list(zipped)  # list() 转换为列表
[(1, 4), (2, 5), (3, 6)]
>>> list(zip(a,c))              # 元素个数与最短的列表一致
[(1, 4), (2, 5), (3, 6)]
 
>>> a1, a2 = zip(*zipped)          # 与 zip 相反，zip(*) 可理解为解压，返回二维矩阵式(tuple)
>>> a1
(1,2,3)
>>> list(a1)
[1, 2, 3]
>>> list(a2)
[4, 5, 6]
>>>


# emurate用法
# 用来简化for loops
>>>seasons = ['Spring', 'Summer', 'Fall', 'Winter']
>>> list(enumerate(seasons))
[(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
>>> list(enumerate(seasons, start=1))       # 下标从 1 开始
[(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]
```

## ``*``and ``**`` 

## ``__constant__``


## python内置函数
### ``filter()``
https://www.geeksforgeeks.org/filter-in-python/

``filter(function, sequence)``: The filter() method filters the given sequence with the help of a function that tests each element in the sequence to be true or not.

```
filter(function, sequence)
Parameters:
function: function that tests if each element of a 
sequence true or not.
sequence: sequence which needs to be filtered, it can 
be sets, lists, tuples, or containers of any iterators.
Retruns:
returns an iterator that is already filtered.
```

```python3
# 简单例子
# a list contains both even and odd numbers.  
seq = [0, 1, 2, 3, 5, 8, 13] 
  
# result contains odd numbers of the list 
result = filter(lambda x: x % 2, seq) 
print(list(result)) 
  
# result contains even numbers of the list 
result = filter(lambda x: x % 2 == 0, seq) 
print(list(result)) 
```

# python异常处理
# 傻逼编码
https://www.cnblogs.com/fkissx/p/5417363.html
https://www.cnblogs.com/busui/p/9340339.html (写的不错)

## 编码
python是怎么处理编码的？
python内部用unicode处理编码，网页一般都是utf-8编码（包括terminal为了显示中文也是）
``#encoding=utf-8``是为了让ide能正确用中文注释

python字符串是unicode编码，所以加入要发request，存数据库等等，可能需要str.encode('utf-8') 此时会转化为bytes，str.decode('utf-8')会把bytes转化成utf-8编码字符串

为什么要编码？
个人理解是内存存储用unicode(定长)，硬盘存储utf-8（变长），传输用bytes
## python的编码问题，为什么我总是有这种错误
```python3
#!/usr/bin/python3
 
str = "菜鸟教程";
str_utf8 = str.encode("UTF-8")
str_gbk = str.encode("GBK")
 
print(str)
 
print("UTF-8 编码：", str_utf8)
print("GBK 编码：", str_gbk)
 
print("UTF-8 解码：", str_utf8.decode('UTF-8','strict'))
print("GBK 解码：", str_gbk.decode('GBK','strict'))


# 以上实例输出结果如下：
菜鸟教程
UTF-8 编码： b'\xe8\x8f\x9c\xe9\xb8\x9f\xe6\x95\x99\xe7\xa8\x8b'
GBK 编码： b'\xb2\xcb\xc4\xf1\xbd\xcc\xb3\xcc'
UTF-8 解码： 菜鸟教程
GBK 解码： 菜鸟教程
```


# python 用ymal文件做配置
https://www.cnblogs.com/yoyoketang/p/8874392.html
https://www.jianshu.com/p/2787af33d86a
如何继承（引用）？： https://www.jianshu.com/p/4e755b8fdb81
在线解析：https://qii404.me/tools/yaml-parse

三个要点：
- ymal是啥：（是一种markup language），类似于json，写好以后可以被python读成dict和list
- 怎么写：基本语法，不同数据类型的表示，转义字符等
- 怎么读：安装pyymal，python先读文件，再用ymal.load()

坑
用*和&， 默认会override

# python多线程/python多进程

同步方法
- lock:
- condition(wait(),notify(),notifyall()):
- semaphore
- event

## 锁
```python3
import threading

lock = threading.Lock()
lock.acquire()
lock.release()

rlock = threading.RLock()
rlock.acquire()
rlock.release()
```
锁都是对象级而不是线程级别，即在某个线程运行的时候调用``lock.acquire()``和``lock.release()``，而不是线程调用``thread.acquire()``和``thread.release()``。（原因：假如是线程的方法，是没有意义的，例如thread.lock()。只有线程获得了锁对象才可以使用锁的方法，所以锁是对象级的，每次线程就看lock对象是什么状态来决定自己是否执行）

- ``threading.Lock()``: ①原始锁，原始锁是一个②在锁定时不属于特定线程的同步基元组件，它是能用的最低级的同步基元组件。原始锁处于 "锁定" 或者 "非锁定" 两种状态之一。它被创建时为非锁定状态。它有两个基本方法， acquire() 和 release() 。当状态为非锁定时， acquire() 将状态改为锁定并立即返回。当状态是锁定时， acquire() 将阻塞至其他线程调用 release() 将其改为非锁定状态，然后 acquire() 调用重置其为锁定状态并返回。 release() 只在锁定状态下调用； 它将状态改为非锁定并立即返回。如果尝试释放一个非锁定的锁，则会引发 RuntimeError  异常。锁支持 上下文管理协议，即支持with语句，下文例子中会用到。
- ``threadding.Rlock()``: 重入锁，若要锁定锁，线程调用其 acquire() 方法；一旦线程拥有了锁，方法将返回。若要解锁，线程调用 release() 方法。 ③acquire()/release() 对可以嵌套，重入锁必须由获取它的线程释放。一旦线程获得了重入锁，同一个线程再次获取它将不阻塞。只有最终 release() (最外面一对的 release() ) 将锁解开，才能让其他线程继续处理 acquire() 阻塞。；线程必须在每次获取它时释放一次。

Lock在锁定时不属于特定线程，也就是说，Lock可以在一个线程中上锁，在另一个线程中解锁。而对于RLock来说，只有当前线程才能释放本线程上的锁。

## Condition
https://www.jianshu.com/p/5d2579938517
中文名：条件变量
为什么：有些更复杂的条件Lock实现不了，condition支持更复杂的(在acquire(),release()的基础上还支持wait(),norify())

A线程在等待中，B线程在干活，B干活完毕之后通知A线程活干完了，B线程进入等待，而A线程得到了通知之后，不再继续等待，开始干活，干完之后通知B线程，如此循环，直到结束。

怎么使用：
```python3
import threading
class XiaoAi(threading.Thread):
    def __init__(self, cond):
        super().__init__(name="小爱")
        self.cond = cond  # condition对象

    def run(self):
		# wait()之前要先获得锁
        self.cond.acquire()

        self.cond.wait()
        print("{} : 在".format(self.name))
        self.cond.notify()

        self.cond.wait()
        print("{} : 好啊".format(self.name))
        self.cond.notify()

        self.cond.wait()
        print("{} : 不聊了，再见".format(self.name))
        self.cond.notify()

        self.cond.release()


class TianMao(threading.Thread):
    def __init__(self, cond):
        super().__init__(name="天猫精灵")
        self.cond = cond

    def run(self):
        self.cond.acquire()

        print("{} : 小爱同学".format(self.name))
        self.cond.notify()  # 并不会释放锁，而是通知XiaoAi，XiaoAi尝试取获取锁
        self.cond.wait()  # 释放锁，XiaoAi成功获取到锁

        print("{} : 我们来对古诗吧".format(self.name))
        self.cond.notify()
        self.cond.wait()

        print("{} : 我住长江头".format(self.name))
        self.cond.notify()
        self.cond.wait()

        self.cond.release()

if __name__ == "__main__":
    cond = threading.Condition()
    xiaoai = XiaoAi(cond)
    tianmao = TianMao(cond)
    
    # 启动顺序很重要
    xiaoai.start()
    tianmao.start()

# 执行结果
# 天猫精灵 : 小爱同学
# 小爱 : 在
# 天猫精灵 : 我们来对古诗吧
# 小爱 : 好啊
# 天猫精灵 : 我住长江头
# 小爱 : 不聊了，再见
```

源码分析：
```python3
# acquire([timeout])/release(): 调用关联的锁的相应方法。 

# wait([timeout]): 调用这个方法将使线程进入Condition的等待池等待通知，并释放锁。
    使用前线程必须已获得锁定，否则将抛出异常。 

# notify(): 调用这个方法将从等待池挑选一个线程并通知，收到通知的线程将自动调用
    acquire()尝试获得锁定（进入锁定池）；其他线程仍然在等待池中。调用这个方法不会
    释放锁定。使用前线程必须已获得锁定，否则将抛出异常。 

# notifyAll(): 调用这个方法将通知等待池中所有的线程，这些线程都将进入锁定池
    尝试获得锁定。调用这个方法不会释放锁定。使用前线程必须已获得锁定，否则将抛出异常。
```
https://www.jianshu.com/p/5d2579938517

## semaphore
Semaphore对象内部管理一个计数器(semaphore的value属性)，该计数器由每个``acquire()``调用递减，并由每个``release()``调用递增。计数器永远不会低于零，当``acquire()``发现计数器为零时，线程阻塞，等待其他线程调用release()。
Semaphore对象支持上下文管理协议。(``with()``)
**用于保护有限容量的资源。**

```python3
import threading
import time


sem = threading.Semaphore(3)


class DemoThread(threading.Thread):

    def run(self):
        print('{0} is waiting semaphore.'.format(self.name))
        sem.acquire()
        print('{0} acquired semaphore({1}).'.format(self.name, time.ctime()))
        time.sleep(5)
        print('{0} release semaphore.'.format(self.name))
        sem.release()


if __name__ == '__main__':
    threads = []
    for i in range(8):
        threads.append(DemoThread(name='Thread-' + str(i)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()
```

## event
也是用线程间的沟通，线程可以获取其他线程的状态
即程序中的其一个线程需要通过判断某个线程的状态来确定自己下一步的操作，就用到了event对象
python中一种**标志位**方法，我们可以通过对event的设置和清除，并让子线程根据event的状态来执行相应的操作即可完成对线程的控制
```
# event.wait()：如果标志位设定了，它不做任何事，如果没有设定，则将会锁住，等待标志位的设定

# event.set()：设置标志位，某线程检测标志位为True即执行

# event.clear()：清除标志位
```

example
原文链接：https://blog.csdn.net/nzjdsds/article/details/91129359
```python
#在这里我们模仿一个红绿灯的应用场景，绿灯亮的时候，车可以通过，红灯亮的时候要等待。
import time
import threading
 
event = threading.Event()#首先要获取一个event对象
 
def lighter():
    count = 0
    event.set() #先设置绿灯
    while True:
        if count >5 and count < 10: #改成红灯
            event.clear() #把标志位清了
            print("红灯")
        elif count >10:
            event.set() #变绿灯
            count = 0
        else:
            print("绿灯")
        time.sleep(1)
        count +=1
 
def car(name):
    while True:
        if event.is_set(): #代表绿灯
            print("[%s] 正在开过"% name )
            time.sleep(1)
        else:
            print("[%s] 正在等待" %name)
            event.wait()#车的这个线程就锁在这里不动了，一直到set的时候，才会继续执行car的这个线程
 
 
light = threading.Thread(target=lighter,)
light.start()
 
car1 = threading.Thread(target=car,args=("奔驰",))
car1.start()
```

python 异步模块
`` import concurrent.futures``
线程：``concurrent.futures.ThreadPoolExecutor()``
进程：``concurrent.futures.ProcessPoolExecutor()``

# 上下文管理协议
``with as`` 语句
https://www.cnblogs.com/greatkyle/p/6796991.html
为了让一个对象兼容with语句，必须在这个对象的类中声明__enter__和__exit__方法
```python3
enter(self)
exit(self, exc_type, exc_val, exc_tb)

# enter:出现with语句，对象就会触发__enter__,其返回值会赋给as后的变量名

# exit:with代码执行结束后，会执行__exit__。
```
