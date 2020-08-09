# Lock 接口
- 隐式锁：synchronized 关键字
- 显示锁：Lock接口

Lock接口能实现比 synchronized 关键字更多的特性
- 非阻塞获取锁 ``tryLock()``
- 被中断获取锁 ``lockInterruptibly()``
- 超时获取锁 ``tryLock()``

## 重入锁 ReentrantLock
特点：
- 支持一个线程对资源重复加锁
- 支持公平锁和非公平锁

notes: 
- synchronized 隐式重入
- mutex 不支持重入

公平与不公平重入锁
- 公平：按照请求时间顺序分配锁（先来后到顺序）
- 非公平：实现更简单，默认

同步锁的实现：
- 继承 AQS
- 支持一个线程对资源重复加锁需要实现：
    1. **线程再次获取锁**。锁需要去识别获取锁的线程是否为当前占据锁的线程，如果是，则再次成功获取。
    2. **锁的最终释放**。线程重复n次获取了锁，随后在第n次释放该锁后，其他线程能够获取到该锁。锁的最终释放要求锁对于获取进行计数自增，计数表示当前锁被重复获取的次数，而锁被释放时，计数自减，当计数等于0时表示锁已经成功释放。

## 读写锁 ReentrantReadWriteLock
- 读锁：共享锁
- 写锁：排他锁

作用：避免干啥都被阻塞，提高并发性

```java
// sample
// 不要再try里获取锁
// 一定在finally里释放锁。
private static final fn() {
    // 获取锁
    try {
        // do something
    } finally {
        // 释放锁
    }
}
```

# 队列同步器 AQS(AbstractQueuedSynchronizer)
队列同步器是构建锁和其他同步组件的框架，子类继承 AQS
- 它使用了一个int成员变量表示同步状态
- 通过内置的FIFO队列来完成资源获取线程的排队工作
- 各种方法
    - 提供一组方法管理同步状态: ``getState()``、``setState(int newState)``和``compareAndSetState(int expect,int update)`` （应该都是线程安全且原子的）
    - 提供一组可重写方法，其子类根据需求重写
    - 提供一组模板方法，子类实现


Notes：
- 我的理解是管程
- 实现的同步组件包括 ``ReentrantLock``、``ReentrantReadWriteLock`` 和 ``CountDownLatch`` 等

## 同步器的接口
todo

## 同步器的实现
todo

# Condition 接口
有两种 Condition 方法，用起来差不太多
- Object (java.lang.Object)的监视器方法
    - java里所有对象都有
- Condition 接口提供的监视器方法
    - ConditionObject是同步器AbstractQueuedSynchronizer的内部类

## Condition 的接口

```java
Lock lock = new ReentrantLock();
Condition condition = lock.newCondition();

public void conditionWait() throws InterruptedException {
    lock.lock();
    try {
        condition.await();
    } finally {
        lock.unlock();
    }
} 


public void conditionSignal() throws InterruptedException {
    lock.lock();
    try {
        condition.signal();
    } finally {
        lock.unlock();
    }
}
```
分析：
- Condition 是依赖 Lock 对象的。Condition 是 lock 对象创建出来的。
- condition 对象作为成员变量
- 当调用await()方法后，当前线程会释放锁并在此等待，而其他线程调用Condition对象的signal()方法，通知当前线程后，当前线程才从await()方法返回，并且在返回前已经获取了锁

例子 BoundedQueue 讲的很清楚
notes: condition对象的取名，``notFull``表示队列不满的状态，如果满了说明未达到该条件，调用``notFull.await()``。如果一个操作导致队列不满，满足条件，调用``notFull.signal()``

## Condition 的实现
``ConditionObject`` 是同步器 ``AbstractQueuedSynchronizer`` 的内部类，因为 ``Condition`` 的操作需要获取相关联的锁，所以作为同步器的内部类也较为合理。每个 ``Condition`` 对象都包含着一个队列（以下称为**等待队列**），该队列是 ``Condition`` 对象实现等待/通知功能的关键。

**等待队列，等待和唤醒**
- 等待队列上是在 Condition 对象上等待的线程
    - 链表结构
    - FIFO
- ``condition.await()`` 当前对象释放锁，进入等待队列
- ``condition.signal()`` 唤醒在等待队列中等待时间最长的节点