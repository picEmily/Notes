- I/O多路复用：
	- 系统调用select，poll，epoll
- Linux五种I/O模型

# Linux I/O 模型
## 同步/异步，阻塞/非阻塞
参考：
[同步、异步、阻塞与非阻塞](https://www.jianshu.com/p/aed6067eeac9 "同步、异步、阻塞与非阻塞")
[五种I/O模型](https://www.jianshu.com/p/486b0965c296 "五种I/O模型")

### 消息的通知机制
- 同步：
	- 同步就是一个任务的完成需要依赖另外一个任务时，只有等待被依赖的任务完成后，依赖的任务才能算完成，这是一种**可靠的任务序列**
	- 一个同步调用发出后，调用者要一直等待返回消息（结果）通知后，才能进行后续的执行
- 异步：
	- 异步是不需要等待被依赖的任务完成，只是通知被依赖的任务要完成什么工作，**依赖的任务也立即执行**，只要自己完成了整个任务就算完成，**不可靠的任务序列**
	- 当一个异步过程调用发出后，调用者不能立刻得到返回消息（结果）。实际处理这个调用的部件**在完成后，通过状态、通知和回调来通知调用者**

### 进程（线程）等待消息通知时的状态
**程序在等待调用结果（消息，返回值）时的状态.**
- 阻塞
	- 阻塞调用是指调用结果返回之前，当前线程会被**挂起**，一直处于等待消息通知，不能够执行其他业务。函数只有在得到结果之后才会返回
- 非阻塞
	- 非阻塞和阻塞的概念相对应，指在不能立刻得到结果之前，**该函数不会阻塞当前线程，而会立刻返回**。
	- 非阻塞的方式可以明显的提高CPU的利用率，但是也带了另外一种后果就是系统的线程切换增加

### 同步/异步 与 阻塞/非阻塞
参考：
https://www.cnblogs.com/straybirds/p/9479158.html
图：同步阻塞
![BIO](https://images2018.cnblogs.com/blog/874126/201808/874126-20180815215329688-621626362.png)

图：同步非阻塞
![NIO](https://images2018.cnblogs.com/blog/874126/201808/874126-20180815215551173-501412222.png)

- 同步阻塞BIO：
	- ``socket()``,  ``read()``等将``fd``不设置``O_NONBLOCK``
	- 用户线程发起IO，由用户空间转到内核空间。
	- 内核等到数据包到达后，然后将接收的数据拷贝到用户空间，完成I/O
- 同步非阻塞NIO：
	- ``socket()``,  ``read()``等将``fd``设置为``O_NONBLOCK``
	- 用户线程发起IO请求时立即返回
	- 但并未读取到任何数据，用户线程**需要不断地发起IO请求**，直到数据到达后，才真正读取到数据，继续执行。
- 异步非阻塞AIO：
	- 异步非阻塞
	- 函数会**马上返回**（不会被阻塞），当所关注的事件被触发时会调用之前注册的回调函数进行处理
- 异步阻塞（？？？）：
	- 感觉不是很常用，个人理解就是内核立即返回，但是用户进程不继续执行，一直到IO完成，内核通知用户线程，用户线程继续执行
	- 等待消息通知，但是也不做其他事情（被阻塞），一直到被通知

## 五种I/O模型
- 阻塞
- 非阻塞
- I/O复用
- 信号驱动I/O
- 异步I/O

# IO多路复用

## 什么是I/O多路复用（I/O multiplexing）
**多进程并发处理I/O：**
- **一个I/O流进来，我们就开启一个进程处理这个I/O流**
那么假设现在有一百万个I/O流进来，那我们就需要开启一百万个进程一一对应处理这些I/O流（——这就是传统意义下的多进程并发处理）。
- 一百万个进程，**CPU占有率极高**，这个实现方式及其的不合理。

**I/O多路复用模型**
- **一个线程，通过记录I/O流的状态来同时管理多个I/O，可以提高服务器的吞吐能力**
	- **与多进程和多线程技术相比，I/O多路复用技术的最大优势是系统开销小，系统不必创建进程/线程，也不必维护这些进程/线程，从而大大减小了系统的开销。**
- 将多个I/O凑在一起，通过记录传入的每一个I/O流的状态来**同时管理多个IO**


**分类：**
- 多进程并发处理IO
	- 阻塞I/O模型
	- 非阻塞I/O模型
- I/O复用模型
	- select
	- poll
	- epoll
- 信号驱动I/O模型
- 异步I/O模型

## 什么时候使用I/O多路复用
- 当客户处理**多个描述符**时（一般是交互式输入和网络套接口），必须使用I/O复用。
- 当一个客户同时处理多个套接口时，而这种情况是可能的，但很少出现。
- 如果一个TCP服务器既要处理监听套接口，又要处理已连接套接口，一般也要用到I/O复用。
- 如果一个服务器即要处理TCP，又要处理UDP，一般要使用I/O复用。
- 如果一个服务器要**处理多个服务或多个协议**，一般要使用I/O复用。

## select，poll，epoll
来自ubuntu文档

### select
```C
int select(int nfds, fd_set *readfds, fd_set *writefds,
          fd_set *exceptfds, struct timeval *timeout);

void FD_CLR(int fd, fd_set *set);
int  FD_ISSET(int fd, fd_set *set);
void FD_SET(int fd, fd_set *set);
void FD_ZERO(fd_set *set);
```

- ``select()``  and ``pselect()`` allow a program to **monitor multiple file descriptors, waiting until one or more of the file descriptors become "ready" for some class of I/O operation **(e.g., input possible).  
- A file descriptor is considered  ready  if it is possible to perform a corresponding I/O operation (e.g., read(2) without blocking, or a sufficiently small write(2)).
- ``select()`` can monitor only file descriptors numbers that are less than **FD_SETSIZE**; poll(2) does not  have  this limitation.

参数解释：
- 有三种sets of file descriptors
	- ``readfds``: 是否可以读字符（只要不是EOF都可以读）
	- ``writefds``: 是否可以写如文件
	- ``excepfds``: be watched for exceptional conditions
- 四种macros管理sets
	- FD_ZERO() clears a set.  
	- FD_SET() add a given file descriptor to a set
	- FD_CLR() remove a given file descriptor from a set.
	- FD_ISSET() tests to see if a file descriptor is part of the set; this is useful after select() returns.

> fd and FILE*
> https://stackoverflow.com/questions/5256599/what-are-file-descriptors-explained-in-simple-terms
> 简而言之就是 ``FILE*``是对``fd``的封装，``fd``是直接和kernal交流，``FILE*``提供了更多对外接口
> - A file descriptor is an opaque handle that is used in the interface between user and kernel space to identify file/socket resources. Therefore, when you use open() or socket() (system calls to interface to the kernel), you are given a file descriptor, which is an integer (it is actually an index into the processes u structure - but that is not important). Therefore, if you want to interface directly with the kernel, using system calls to read(), write(), close() etc. the handle you use is a file descriptor.
- There is a layer of abstraction overlaid on the system calls, which is the stdio interface. This provides more functionality/features than the basic system calls do. For this interface, the opaque handle you get is a ``FILE*``, which is returned by the fopen() call. There are many many functions that use the stdio interface fprintf(), fscanf(), fclose(), which are there to make your life easier. In C, stdin, stdout, and stderr are FILE*, which in UNIX respectively map to file descriptors 0, 1 and 2.

### poll
```C
int poll(struct pollfd *fds, nfds_t nfds, int timeout);

struct pollfd {
   int   fd;         /* file descriptor */
   short events;     /* requested events */
   short revents;    /* returned events */
};
```
- ``poll()`` performs a similar task to ``select(2)``: it waits for one of a set of file descriptors to become ready to perform I/O.
- The set of file descriptors to be monitored is specified in the ``fds`` argument, which is an array of structures of the ``pollfd``

### epoll
- epoll和前两者调用过程不太一样，**没有描述符限制**，使用**监听回调的机制**
- epoll**使用一个文件描述符管理多个描述符**，将用户关系的文件描述符的事件存放到内核的一个**事件表**中，这样在用户空间和内核空间的**copy只需一次**

**方法：**
epoll事先通过``epoll_ctl()``来注册一个文件描述符，一旦基于某个文件描述符就绪时，内核会采用类似callback的回调机制，迅速激活这个文件描述符，当进程调用``epoll_wait()``时便得到通知。
- ``epoll_create()``: creates a new epoll instance and returns a file  descriptor  referring  to  that  instance.
- ``epoll_ctl()``: particular file descriptors is registered via epoll_ctl(2).
- ``epoll_wait()``: waits for I/O events, blocking the calling thread if no events are currently available


**lT/ET**
- LT: 当epoll_wait检测到描述符事件发生并将此事件通知应用程序，应用程序**可以不立即处理该事件**。下次调用epoll_wait时，会再次响应应用程序并通知此事件。
- ET: 当epoll_wait检测到描述符事件发生并将此事件通知应用程序，应用程序**必须立即处理该事件**。如果不处理，下次调用epoll_wait时，不会再次响应应用程序并通知此事件。



## 三者对比
**select and poll:**
- 都是将用户传入的数组拷贝到内核空间，然后查询每个fd对应的设备状态
- 用轮询的方式查询所有流（能读取数据/写入数据的流），复杂度O(N)
- select 是数组存，poll基于链表存

**select/poll and epoll**