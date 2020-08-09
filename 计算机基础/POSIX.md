# POSIX
可移植操作系统接口
Portable Operating System Interface

## POSIX
The Portable Operating System Interface (POSIX) is a family of **standards** specified by the IEEE Computer Society for m**aintaining compatibility between operating systems**. 

**POSIX defines the application programming interface (API), along with command line shells and utility interfaces, for software compatibility with variants of Unix and other operating systems.**

## 作用
在C标准函数的基础上，额外添加了许多功能
平时使用的命令行本身就是调用了这些接口的程序
> Whereas the standard C library functions provide only simple file reading/writing, the POSIX functions add more comprehensive services, including access to filesystem metadata (e.g. modification time, who can access files), directory contents, and filesystem operations that are necessary for implementing Unix commands like ls and mkdir, which are themselves just executable programs. There is one POSIX function you will use for this assignment: the function access to check the user's permissions (how they can access a file) for a file. Take a look at its manual page to get a preview. We'll explain access in more detail later in the spec.

## Environment
In Unix system, programs run in the context of the user's "environment". The environment is a list of key-value pairs that provide information about the terminal session and configure the way processes behave.

**查看环境变量**
```bash
printenv  # 打印所有环境变量
printenv USER SHELL HOME  # 打印USER，SHELL，HOME
env BINKY=1 OTHERARG=2 ./myprogram  # 设置环境变量的同时运行程序
```

