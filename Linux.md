# 系统管理
- 进程管理
- 工作管理
- 系统资源查看
- 系统定时任务

## 进程查看/管理
进程：**正在执行**的**程序和命令**
- 意味着有自己的地址空间
- 同时占有系统资源

Q: ``ls`` 有进程吗
A: 系统命令，是有进程的，但是很快就结束了

**进程管理：**
- **判断服务器健康状态**（***最重要的功能***）
	- 进程是否合法（例如病毒）
	- 资源占用情况
- 查看进程
- 杀死进程
	- 无法正常终止进程

### 判断服务器健康
``top``: 查看进程资源占用
``ps``: 查看系统中所有进程
``kill [pid]``: 杀死（非正常状态）进程

（？？？待实验）
```bash
ps -aux# Unix BSD 格式 -a 前台 -u 用户 -x 后台
top # 查看健康状态 -d 表示更新秒数
pstree  # 进程树 
pstree -p # 进程树+pid
```
**ps讲解：**
- VSZ：虚拟内存
- RSS：实际内存
- TTY：登录终端
	- tty1-tty7是本地控制台终端，1-6是字符终端，7是图形终端
	- pts/0-255 是虚拟终端

- STAT：**进程状态**
	- R：运行，S：睡眠， T：停止， s：包含子进程， +：后台进程
- TIME：占用CPU运算时间
- COMMAND：启动该进程的命令 

**top讲解**
- **此命令自身耗费资源较多**
- 系统运行时间，用户数量，1/5/15min平均负载（CPU核数）
- Tasks：zombie是正在终止还没完成的进程
- CPU信息：%id 指的是cpu空闲率
- 改变排序：``M`` 内存排序 ``P``进程排序

```
kill -l  # 查看所有的信号
1 重启
9 强制终止
15 正常终止

kill [signal] [pid]  # 默认15
kill -15 [pid]  # 强制终止进程
killall  # 杀死所有 -i 交互式
pkill  # [signal] [pid] this same as kill
pkill -t  # 踢出用户 
```

### 进程管理
```bash
# 放入后台是栈
[command] &  # 后台运行
ctrl+z  # 挂起（不运行） 
fg [%工作号] # 恢复到前台运行
bg [%工作号] # 恢复到后台运行

jobs -l  # 看后台命令状态
```

**系统信息查看**
```bash
vmstat [刷新延时] [刷新次数] # 查看系统资源
dmesg  # 查看系统信息
free  # 内存状态
free -m 兆
uname -a -r -s # 内核信息
lsb_release -a  # 发行版本
```
（？？？）
cache：缓存。先从硬盘加载到内存，然后进程从内存中调用。
buffer：缓冲。加速数据的写入，不是每一次写保存都存到硬盘，buffer存满了再一次性写入硬盘

```bash
# /proc 是一个存在内存中的文件夹
# 可以看很多信息
cat /proc/cpuinfo
```

```bash
# 列出进程调用的文件
# 可以用不同检索查看
lsof -c -u -p

e.g.
lsof -c init
```

## 共享内存管理
```bash
取得ipc信息：
ipcs [-m|-q|-s]
-m 输出有关共享内存(shared memory)的信息
-q 输出有关信息队列(message queue)的信息
-s 输出有关“遮断器”(semaphore)的信息
%ipcs -m

删除ipc
ipcrm -m|-q|-s shm_id
%ipcrm -m 105
```