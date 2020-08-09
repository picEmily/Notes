# Java并发容器和框架
- Doug Lea 大佬提供的一组工具，数据结构
- 分为阻塞和非阻塞（CAS）实现

# ``ConcurrentHashMap`` 的实现原理与使用
- 线程安全 (相比``HashMap``)
- 高效 (相比``HashTable``)

> **补充**：``HashMap`` 和 ``HashTable`` 的结构  
> ``HashMap`` 的结构:底层数组 + 链表，不支持多线程。多线程会占满CPU。  
> ``HashTable`` 就是单纯的用 ``synchronized`` 关键字保证线程安全。所以读/写操作都排他，这样的效率很低  
> ``ConcurrentHashMap`` 使用的是**分段锁**技术  

**分段锁**：容器有很多把锁,每个锁只分配一段数据。可以提高并发。

## ``ConcurrentHashMap`` 的结构

# Fork/Join 框架
- 把大任务分解成小任务，再把小任务汇总
    - 窃取任务
- 个人理解是模仿操作系统的

**Fork/Join的设计**
- 分割任务
- 执行任务并合并结果
    - 工作线程存在双端队列里
    - 有一个任务完成队列，有一个线程专门合并数据

## Fork/Join框架的使用

```java
// fork(), join()方法继承自 ForkJoinTask 类
// 重写 compute()

//       ForkJoinTask
//            ↓
//        extends
//            ↓
//RecursiveAction RecursiveTask    
```
- ``RecursiveAction``: no return 
- ``RecursiveTask``: return

```java
// 线程池管理工作线程

//              ForkJoinPool 
//                  ↓
// ForkJoinTask数组     ForkJoinWorkerThread数组
```
- ``ForkJoinTask``数组: ??? ``fork()``, ``join()``
- ``ForkJoinWorkerThread``数组: 工作线程，执行任务的线程
- todo：？？？没看太懂

**例子**
计算1+2+3+4

```java
// Two sub tasks, each one operates an add operation
// Return tasks use RecursiveTask class

package sample;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.Future;
import java.util.concurrent.RecursiveTask;

public class CountTask extends ForkJoinTask<Integer> {
    private static final int THRESHOLD = 2;     // 最多分成两个任务
    private int start;                          // 计算加法的起点
    private int end;

    public CountTask(int start, int end) {
        // 构造方法
        this.start = start;
        this.end = end;
    }


    /*
    * 我们要实现的方法，用来定义我们的工作
    * 类似 OS 中的exec()
    */
    @override
    protected Integer compute() {
        int sum = 0;

        boolean canCompute = (end - start) <= THRESHOLD;
        if (canCompute) {
            // 没达到阈值才计算
            for (int i = start; i <= end; i++) {
                sum += 1;
            }
        } else {
            // 大于阈值则分成子任务
            int mid = (start + end) / 2;
            CountTask leftTask = new CountTask(start, mid);
            CountTask rightTask = new CountTask(mid+1, end);

            // 执行
            leftTask.fork();                        // 会进入compute() 方法 
            rightTask.fork();

            // 获取结果
            int leftResult = leftTask.join();       // 等待执行完并返回结果
            int rightResult = rightTask.join();

            sum = leftResult + rightResult;
        }
    }
    return sum;

}

public static void main(String[] args) {
    ForkJoinPool forkJoinPool = new ForkJoinPool();     // 线程池
    CountTask task = new CountTask(1, 4);               // 我们的自定义任务
    Future<Integer> result = forkJoinPool.submit(task); // 执行 CountTask 的任务

    try {
        System.out.println(result.get());               // get() 获取线程池结果    
    } catch (InterruptedException e) {
        // doing nothing here
    } catch (ExecutionExeption e) {
        // doing nothing here
    }
}
```

## Fork/Join框架的实现原理