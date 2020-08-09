# Executor框架
我们不会为了每一个任务都创建新线程  
所以需要分开**工作单元**和**执行机制**
- 工作单元：``Runnable``，``Callable``
- 执行机制：``Executor`` 框架：**将任务的提交和任务的执行分开**

``Executor`` 是**用户级**线程调度器  
``Executor``框架 将这些**任务**映射为固定数量的**线程**  
操作系统内核将这些线程映射到硬件处理器上 

```
task task task ... task task        (任务)
            ↓
        Executor 框架
            ↓
    线程池：thread thread thread    (用户线程)
            ↓
        OS kernal
            ↓
    CPU线程 CPU线程                 (内核线程)
```

## Executor 框架的使用
**Executor 框架的组成**
- 任务：实现 ``Runnable`` 或者 ``Callable`` 接口
    - 他们的实现类可以被 ``ThreadPoolExecutor`` 和``ScheduledThreadPoolExecutor`` 执行
- 任务的执行：实现 ``ExecutorService`` 接口的 ``ThreadPoolExecutor`` 类和``ScheduledThreadPoolExecutor`` 类
    - ThreadPoolExecutor 用来执行被提交的任务
    - ScheduledThreadPoolExecutor 可以在给定的延迟后运行命令，或者定期执行命令
- 异步计算的结果：接口 ``Future`` 和实现 ``Future`` 接口的 ``FutureTask`` 类。

**Executor框架的使用**
1. 主线程首先要创建实现 ``Runnable`` 或者 ``Callable`` 接口的任务对象。工具类Executors可以把一个 ``Runnable`` 对象封装为一个 ``Callable`` 对象(``Executors.callable(Runnable task)``或 ``Executors.callable(Runnable task，Object resule)``)。
2. 然后可以把 ``Runnable`` 对象直接交给 ``ExecutorService`` 执行(``ExecutorService.execute(Runnablecommand)``)；或者也可以把Runnable对象或Callable对象提交给 ``ExecutorService`` 执行(``ExecutorService.submit(Runnable task)``或``ExecutorService.submit(Callable<T>task)``)。
3. 如果执行 ``ExecutorService.submit(…)``，``ExecutorService`` 将返回一个实现 ``Future`` 接口的对象(到目前为止的JDK中，返回的是 ``FutureTask`` 对象)。由于 ``FutureTask`` 实现了``Runnable``，程序员也可以创建 ``FutureTask``，然后直接交给 ``ExecutorService`` 执行。
最后，主线程可以执行 ``FutureTask.get()`` 方法来等待任务执行完成。主线程也可以执行 ``FutureTask.cancel(boolean mayInterruptIfRunning)`` 来取消此任务的执行。

# Executor框架的成员详解
- ``ThreadPoolExecutor``
- ``ScheduledThreadPoolExecutor``
- ``Future`` interface: ``FutureTask`` 是它的一个实现类
- ``Runnable`` interface
- ``Callable`` interface

## ``ThreadPoolExecutor``

## ``ScheduledThreadPoolExecutor``

## ``Futuretask``