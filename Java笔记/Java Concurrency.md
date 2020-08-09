# Java Concurrency
参考：https://docs.oracle.com/javase/tutorial/essential/concurrency/
- Process and Thread
- Thread Object
- Synchronization
- Liveness
- Guarded Blocks
- Immutable Objects
- High level concurrency Object

Notes: the tutorial is for JDK 8 
# Process and Thread
略
**5种状态**
创建，就绪，执行，阻塞，销毁
（写代码的时候着重关注就绪，执行，阻塞）

# Thread Object
都和``Thread``对象有关
- To directly control thread creation and management, simply instantiate Thread each time the application needs to initiate an asynchronous task.
- To abstract thread management from the rest of your application, pass the application's tasks to an executor.？？？

**两种实例化Thread的方法**
- implements Runnable (more general)
- extends Thread (easier but limited)

**sleep，interrupts，joins**
- ``Thread.sleep(4000)`` 挂起进程特定时间
	- 唤醒的时间不一定准确
- An *interrupt* is an indication to a thread that it should stop what it is doing and do something else
	- 一般是终止
	- 通过catch InterruptedException
- If ``t`` is a Thread object whose thread is currently executing
	- ``t.join()`` causes the current thread to pause execution until t's thread terminates
	- 主线程等待子线程的终止。也就是 在子线程调用了join()方法后面的代码，只有等到子线程结束了才能执行
	- 唤醒的时间不一定准确

sleep(),join()都有可能引起InterruptedException，所以写的时候要写成
```java
try {
    Thread.sleep(5000);
} catch (InterruptedException e) {
	// ...
}
```

# Synchronization
线程通过共享内存交流
- 所谓共享内存就是：fields（字段，成员变量），引用的对象
- 两类错误：1. *thread interference* 2. *memory consistency errors*
- 通过同步避免错误 1. exclusive access 2. happens-before

**synchronized**
- synchronized methods
	- 同一个对象不能有两个synchronized methods同时执行
	- happends-before relationship：写操作会被其他线程看到
- synchronized statements
- Synchronization is based on *intrinsic lock* or *monitor lock*
	- 功能：1. exclusive access 2. happens-before
	- When a thread invokes a **synchronized method**, it automatically acquires the intrinsic lock for that method's object and releases it when the method returns. The lock release occurs even if the return was caused by an uncaught exception.

**原子性和``volatile``**
原子操作减少synchronized code的使用，更简单
- 原子性操作有两种（变量的读和写）
	- **Reads and writes** are atomic for reference variables and for most primitive variables (all types except long and double).
	- Reads and writes are atomic for all variables declared volatile (including long and double variables).

> 原子操作能exclusive access，但是不能避免memory consistency错误，这个时候要用``volatile``

``volatile`` --> happens-before relationship
- 变量的变化对所有线程可见

**Liveness**
- 死锁
- 饥饿
- 活锁：A thread often acts in response to the action of another thread. If the other thread's action is also a response to the action of another thread, then livelock may result. 
	- 我等待的线程要等待另一个线程
	- 有可能解开

# Guarded Blocks
线程在某些条件下才能执行，轮询是一种办法，但是效率显然不高
用``wait()``/``notifyAll()``/``notify()``
- 执行``object.wait()``的对象要拥有锁，执行以后会释放锁
- 其他阻塞在该对象上的线程线程会获得锁，当某个条件发生的时候执行``Object.notifyAll()``，等待锁的线程就会收到消息
	- ``notify()``只会通知一个线程
- 注意
	- 永远**在synchronized的函数或对象里使用**wait、notify和notifyAll（因为对象需要持有锁才能调用这些方法）
	- 永远在while循环里而不是if语句下使用wait。这样，循环会在线程睡眠前后都检查wait的条件，并在条件实际上并未改变的情况下处理唤醒通知。 https://blog.csdn.net/xiabodan/article/details/102724088
	- 永远在多线程间共享的对象上使用wait。

在生产消费者模型中，通过共享对象来通信。这里的条件是如果生产者还没生产data，那么消费者不消费data，反之亦然。

# Immutable Objects
我的理解就是 mutable objects 可能出现脏读。
两次读之间别的线程提交了某个写操作改变了这个对象
当我们要改变对象的时候通过创造新对象的方式

# High Level Concurrency Objects
以下内容都来自 ``java.util.concurrent`` 并发包

``java.util.concurrent.locks``
https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/locks/package-summary.html
我么在 synchronized 中使用的隐式的锁，实际上它是基于reentrant lock 对象。 Lock对象也通过 Condition对象支持 wait/notify 机制。
使用 Lock 的好处：
- 有意向锁的实现 their ability to back out of an attempt to acquire a lock. 
	- The ``tryLock`` method backs out if the lock is not available immediately or before a timeout expires (if specified).
	- The ``lockInterruptibly`` method backs out if another thread sends an interrupt before the lock is acquired.
例子没看太懂？？？ 为什么要这么写

**Executors** 【没看完】
在其他的地方管理线程，而不是每次都new一个Tread对象。
封装这些方法的对象叫 ``executors`` 
- Executor Interfaces
	- Executor, a simple interface that supports launching new tasks.
	- ExecutorService, a subinterface of Executor, which adds features that help manage the lifecycle, both of the individual tasks and of the executor itself.
	- ScheduledExecutorService, a subinterface of ExecutorService, supports future and/or periodic execution of tasks.
- Thread Pools 线程池
	- worker thread，**减小创建进程的开销**，thread 对象使用固定的内存
	- 简单的使用：``java.util.concurrent.Executors``包中有两种方法1. newCachedThreadPool 2.newSingleThreadExecutor 
	- 另外还有``java.util.concurrent.ThreadPoolExecutor `` 和 ``java.util.concurrent.ScheduledThreadPool`` 
- Fork/Join 一种借鉴自多进程的框架
	- 实现自``ExecutorService``，也用了线程池。实现``ForkJoinPool`` 类

**Concurrent Collections**
- ``BlockingQueue``
- ``HashMap`` -> ``ConcurrentHashMap``
- ``TreeMap`` -> ``ConcurrentSkipList``

**Atomic Variables**
java.util.concurrent.atomic 提供一些支持原子操作的对象，他们的 set 和 get 方法工作起来和 volatile 修饰的变量一样，有 happens-before relationship

```java
import java.util.concurrent.atomic.AtomicInteger;

class AtomicCounter {
    private AtomicInteger c = new AtomicInteger(0);

    public void increment() {
        c.incrementAndGet();
    }

    public void decrement() {
        c.decrementAndGet();
    }

    public int value() {
        return c.get();
    }

}
```
 
**Concurrent Random Numbers**

补充：并发工具
- ``CountDownLatch`` 类
- ``CyclicBarrier`` 类
- ``Semaphore`` 类