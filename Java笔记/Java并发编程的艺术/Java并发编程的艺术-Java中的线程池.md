# Java中的线程池
Java中的线程池是运用场景最多的并发框架，几乎所有需要异步或并发执行任务的程序都可以使用线程池。在开发过程中，合理地使用线程池能够带来3个好处。
1. 降低资源消耗。通过重复利用已创建的线程降低线程创建和销毁造成的消耗。
2. 提高响应速度。当任务到达时，任务可以不需要等到线程创建就能立即执行。
3. 提高线程的可管理性。线程是稀缺资源，如果无限制地创建，不仅会消耗系统资源，还会降低系统的稳定性，使用线程池可以进行统一分配、调优和监控。但是，要做到合理利用线程池，必须对其实现原理了如指掌。

简单来说：
线程池创建的时候就创建了许多空线程。
使用的时候给这些空线程分配工作。
这样减少了不断创建、销毁线程的消耗。

# 线程池的实现
一些参数：
- 核心池大小：``corePoolSize``: 
    - 核心池：线程池基本大小，没有任务执行也维持这么大。
- ``maximumPoolSize``: 线程池允许创建的最大线程数
- 工作队列 ``runnableTaskQueue``: 用于保存等待执行的任务的阻塞队列
- ``ThreadFactory``: ``new ThreadFactoryBuilder().setNameFormat("XX-task-%d").build();``
- ``RejectedExecutionHandler``（饱和策略）: 满了怎么办

提交新任务给线程池
```
提交任务
   ↓
核心线程池 →是→ 工作队列  →是→ 线程池  →是→ 执行饱和策略
 是否满          是否满       是否满
   ↓              ↓            ↓ 
   否             否           否
   ↓              ↓            ↓
创建线程       存储任务到     创建线程
               工作队列
```

# 线程池的使用
```java
// 创建线程池
new ThreadPoolExecutor(corePoolSize, maximumPoolSize, keepAliveTime, milliseconds,runnableTaskQueue, handler); 

// 提交任务*2
// excute() 无返回值
// submit() 有返回值
threadsPool.execute(new Runnable() {
    @Override
    public void run() {
        // TODO Auto-generated method stub
    }
});

Future<Object> future = executor.submit(harReturnValuetask);    // 返回一个 future 对象

try {
    Object s = future.get();                                    // get() 获得返回值
} catch (InterruptedException e) {
    // 处理中断异常
} catch (ExecutionException e) {
    // 处理无法执行任务异常
} finally {
    // 关闭线程池
    executor.shutdown();
}

// 关闭线程池
// 它们的原理是遍历线程池中的工作线程，然后逐个调用线程的interrupt方法来中断线程，
// 所以无法响应中断的任务可能永远无法终止。
shutdown();                     // 一般
shutdownNow();                  // 不需要任务全部执行完

boolean flag = isShutdown();    // 只要调用了shutdown(), shutdownNow() 都返回 true
boolean flag2 = isTerminated(); // 真正关闭成功

// 监控线程池
threadsPool.taskCount;              // 线程池需要执行的任务数量。
threadsPool.completedTaskCount;     // 线程池在运行过程中已完成的任务数量，小于或等于taskCount。
threadsPool.largestPoolSize;        // 线程池里曾经创建过的最大线程数量。通过这个数据可以知道线程池是否曾经满过。如该数值等于线程池的最大大小，则表示线程池曾经满过。
threadsPool.getPoolSize;            // 线程池的线程数量。如果线程池不销毁的话，线程池里的线程不会自动销毁，所以这个大小只增不减。
threadsPool.getActiveCount;         // 获取活动的线程数。
```

**合理配置线程池**
分析：
- 任务的性质：CPU密集型任务、IO密集型任务和混合型任务。
- 任务的优先级：高、中和低。
- 任务的执行时间：长、中和短。
- 任务的依赖性：是否依赖其他系统资源，如数据库连接。

细节：
- ``int NCpu = Runtime.getRuntime().availableProcessors()`` 获得CPU个数
    - CPU密集型：``NCpu + 1``
    - IO密集型：``NCpu * 2``
- 数据库连接：类似IO密集型，等待时间长，设置多一些线程数更好