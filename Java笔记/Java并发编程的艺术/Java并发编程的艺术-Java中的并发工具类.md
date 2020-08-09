# 并发工具
提供一种并发流程控制的手段：实用于不同并发场景简化开发
不用并发工具也是可以的，只是并发工具在某些场景更好用
JDK并发包
- CountDownLatch
- CyclicBarrier
- Semaphore

Exchanger工具

# CountDownLatch
``CountDownLatch`` 允许一个或多个线程等待其他线程完成操作。

```java
// APIs of CountDownLatch

staticCountDownLatch c = new CountDownLatch(2); // 构造方法，传入N作为计数器
c.countDown();                                  // N-1
c.await();                                      // 阻塞当前线程
```

场景：
解析一个有很多sheet的excel，主线程分配每个线程解析一张sheet，解析完以后主线程打印解析完成。

# CyclicBarrier
让一组线程到达一个屏障（也可以叫同步点）时被阻塞，直到最后一个线程到达屏障时，屏障才会开门，所有被屏障拦截的线程才会继续运行。

场景：
CyclicBarrier可以用于多线程计算数据，最后合并计算结果的场景

## 对比CountDownLatch，CyclicBarrier
``CountDownLatch`` 的计数器只能使用一次，而 ``CyclicBarrier`` 的计数器可以使用 ``reset()`` 方法重置。所以 ``CyclicBarrier`` 能处理更为复杂的业务场景。例如，如果计算发生错误，可以重置计数器，并让线程重新执行一次。``CyclicBarrier`` 还提供其他有用的方法，比如 ``getNumberWaiting`` 方法可以获得 ``Cyclic-Barrier`` 阻塞的线程数量。 ``isBroken()`` 方法用来了解阻塞的线程是否被中断。

# Semaphore
不谈了吧，同步、互斥、有限资源限制都能用。

实现：
state, p(), V()

# Exchanger
todo