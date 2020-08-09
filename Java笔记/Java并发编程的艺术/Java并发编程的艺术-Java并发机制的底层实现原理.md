# Java并发机制的底层实现原理
JVM是如何实现锁（操作系统层面），交给CPU执行？**Java中的大部分容器
和框架都依赖于本章介绍的volatile和原子操作的实现原理**
- ``volatile``
- ``synchronized``
- 原子操作

# Volatile的应用
真实操作系统在内存之间还有一个**处理器缓存**
内存- >处理器缓存->操作系统

```java
volatile instance = new Singleton();

=======assembly code========（JIT编译器）
0x01a3de1d: movb $0×0,0×1104800(%esi); // 取内存里一块地址
0x01a3de24: lock addl $0×0,(%esp);	 // valotile 会调用lock指令
```

**Lock指令的作用**
- Lock前缀指令会引起处理器缓存回写到内存
	- 锁定这块内存区的缓存，保证原子性
- 这个**写回操作**导致其他CPU缓存该内存地址数据无效
	- （说白了就是强制刷新所有处理器对valotile修饰变量的马上刷新）

# synchronized 的实现原理与应用
一些概念
- synchronized  和 valotile 相比更重量，又叫重量级锁。
- synchronized 实现**隐式**的锁。
- synchronized 让每一个对象都可以作为**锁**
- 访问同步代码块得到锁，退出或抛出异常释放锁。
- 是一种独占锁，**悲观锁**

synchronized 表现三种形式
- 对于普通同步方法，锁是当前实例对象
- 对于静态同步方法，锁是当前类的Class对象
- 对于同步方法块，锁是Synchonized括号里配置的对象

synchronized 在JVM的实现原理
- JVM基于进入和退出Monitor对象来实现方法同步和代码块同步
- monitorenter指令是在编译后插入到同步代码块的开始位置，而monitorexit是插入到方法结
束处和异常处
	- 任何对象都有一个monitor与之关联
	- monitor被持有后处于**锁定状态**
	- （monitor就是管程，是对共享数据结构和获取/释放锁的一个封装）

synchronized 存在哪里？
- **Java对象头**的 Mark Word 里。包括对象的HashCode，分代年龄（GC标记），锁位标记。

> Java对象头的结构
- Mark Word
	- Hashcode
	- GC对象分代年龄
	- **锁位标记**：锁的状态
- Class Metadata Address：存指针
- Array Length：如果是数组的话，数组的长度

锁的四种状态
- 无状态锁，偏向锁，轻量级锁，重量级锁（级别从低到高）。锁随着竞争升级，但是不能降级。

偏向锁，轻量级锁，重量级锁对比
- todo

TODO：CAS是什么 Compare and Swap 还是 Compare and Set？？？
输入两个数值，旧值和新值。
先比较旧值，没有变化才换成新值
                                           
# 原子操作的实现原理
一些概念
- CAS：Compare and Swap，比较并交换
	- 无锁算法，乐观锁
	- 有三个操作数：内存值V，旧值A，新值B。仅当旧值A和内存值V相同（即不发生变化），将内存值V修改成B，否则什么都不做。
	- ``java.util.concurrent``中大多数类都使用了CAS算法
	- CAS同时具有volatile读和volatile写的内存语义
	- CAS有好多方法``compareAndSwapInt()``, ``compareAndSetState()``，通过调用本地方法实现
- CPU Pipeline：一条指令会被5，6个逻辑电路处理，在一个CPU时钟周期完成一条指令

**处理器如何保证原子性**
- 硬件决定了读取一个字节是原子性的。总线加锁和缓存加锁保证复杂情况的原子性（跨多个缓存行，跨页表等） 
- 总线加锁
	- 总线锁锁定了CPU和内存之间的通信
	- CPU操作共享变量的时候排他：CPU发出 LOCK# 信号，独占共享内存（其他CPU缓存如果缓存该共享变量的内存地址，那么也不能操作）
- 缓存加锁
	- 相比总线加锁开销较小
	- 不在总线上声言 #LOCK 信号，通过**缓存一致性**。
	- 如果某内存被缓存，若执行锁操作回写到内存，其他该内存的缓存无效（？？？没看懂，大概这个意思）

很多指令都会加锁，这些指令实现总线加锁和缓存加锁
- 逻辑操作：ADD OR 
- 交换指令：XADD，CMPXCHG
- 位指令：BTS，BTR，BTC

**Java如何保证原子性**
- 锁（偏向锁，轻量级锁，重量级锁）。轻量级锁，重量级锁的实现也是基于CAS。
- 循环CAS实现原子操作，CMPXCHG指令
	- 循环CAS操作直到成功（个人理解：CAS操作本身不是原子性的，但是宏观上把整个代码块变成原子操作）
	- CAS原子操作的三大问题(？？？暂时没看懂)

例子，线程安全计数器
```java
private void safeCount() {
	for (;;) {
		int i = atomicI.get();
		boolean suc = atomicI.compareAndSet(i, i++); // CAS操作保证+1操作的原子性
		if (suc) {
			break;
		}
	}
}

// private void unsafeCount() { i++; }
```

Java里的CAS利用处理器的 CMPXCHG 指令

为什么CAS能实现安全计数器？？？
