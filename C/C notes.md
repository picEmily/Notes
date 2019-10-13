# 预处理器和头文件
## 预处理
https://www.runoob.com/cprogramming/c-preprocessors.html
C 预处理器是一个文本替换工具
C 预处理器不是编译器的组成部分，但是它是编译过程中一个单独的步骤。
所有的预处理器命令都是以井号（#）开头。它必须是第一个非空字符，为了增强可读性，预处理器指令应从第一列开始。

宏就是一种预处理器处理的东西
宏可以定义一些常量和函数

## 头文件
头文件是扩展名为 .h 的文件，包含了 C **函数声明和宏定义**，被多个源文件中引用共享。有两种类型的头文件：程序员编写的头文件和编译器自带的头文件。

在程序中要使用头文件，需要使用 C 预处理指令 #include 来引用它。前面我们已经看过 stdio.h 头文件，它是编译器自带的头文件。

引用头文件相当于复制头文件的内容，但是我们不会直接在源文件中复制头文件的内容，因为这么做很容易出错，特别在程序是由多个源文件组成的时候。

A simple practice in C 或 C++ 程序中，**建议把所有的常量、宏、系统全局变量和函数原型写在头文件中**，在需要的时候随时引用这些头文件。

- 引用系统头文件用``<>``,引用用户头文件用``"file"``

# C 错误处理
http://www.runoob.com/cprogramming/c-error-handling.html

C 语言不提供对错误处理的直接支持，但是作为一种系统编程语言，它以返回值的形式允许您访问底层数据。在发生错误时，**大多数的 C 或 UNIX 函数调用返回 1 或 NULL，同时会设置一个错误代码 errno**，该错误代码是全局变量，表示在函数调用期间发生了错误。您可以在 errno.h 头文件中找到各种各样的错误代码。

所以，C 程序员可以通过检查返回值，然后根据返回值决定采取哪种适当的动作。开发人员应该在程序初始化时，**把 errno 设置为 0，这是一种良好的编程习惯。0 值表示程序中没有错误**。

## perror() 和 strerror()
**C 语言提供了 perror() 和 strerror() 函数来显示与 errno 相关的文本消息**
- ``perror()`` 函数显示您传给它的字符串，后跟一个冒号、一个空格和当前 errno 值的文本表示形式。
- ``strerror()`` 函数，返回一个指针，指针指向当前 errno 值的文本表示形式。

（1） perror
- 头文件：``stdio.h``
``void perror(const char *msg);``
- 它是基于errno的当前值，在标准错上产生一条出错信息，然后返回。
它先输出由msg字符串，然后是一个冒号后头接着对应于errno值的出错信息。
例： 
```
perror（“sendto”）；
```
打印出：``sendto: Permission denied``

（2）strerror

- 头文件：``string.h``
``char * strerror(int errnum);``
- 此函数将errnum（它通常就说errno值）映射为一个出错信息字符串，并返回错误此字符串
例：
```
printf(“errno is: %d\n”,errno)；
printf(“errno is: %d\n”,strerror（errno)）；
```
结果：``errno is 13``
　　 ``Permission denied``

（3）perror和strerror区别和联系：
- perror和strerror都是根据errno的值打印错误信息的。
- perror是将errno对应的错误消息的字符串打印到标准错误输出上，即stderr或2上，若你的程序将标准错误输出重定向到/dev/null，那就看不到了，就不能用perror了。
而 strerror的作用只是将errno对应的错误消息字符串返回.你可以自己决定咋样处理字符串，比如可以存到日志，也可以直接printf出来。

## Linux error() 
```
#include <error.h>

void error(int status, int errnum, const char *format, ...);
```


TODO:::
```
       error()  is  a general error-reporting function.  It flushes stdout, and then outputs to stderr the program name, a colon and a space,
       the message specified by the printf(3)-style format string format, and, if errnum is nonzero, a second colon and a space  followed  by
       the  string  given  by  strerror(errnum).  Any arguments required for format should follow format in the argument list.  The output is
       terminated by a newline character.

       The program name printed by error() is the value of the global variable program_invocation_name(3).  program_invocation_name initially
       has the same value as main()'s argv[0].  The value of this variable can be modified to change the output of error().

       If status has a nonzero value, then error() calls exit(3) to terminate the program using the given value as the exit status.
```

# main函数
```C
int main() {
	return 0;
}

int main(int argc, char *argv[]) {
	// argc 是命令行传进来参数个数
	// argv是命令行参数，其中argv[0]是文件名
	return 0;
}
```

# 存储类
变量/函数范围和生命周期
https://www.runoob.com/cprogramming/c-storage-classes.html

- 一般局部变量默认auto
- 全局变量默认static
- extern是用来生命在别的文件中声明的变量/函数
- register为了更快速访问（存在寄存器中）

# 变量类型
**关于 double 类型与 float 类型：**

printf() 只会看到双精度数，printf 的 %f 格式总是得到 double，所以在 printf() 中使用 %f 跟 %lf 的输出显示效果是一样的。但是对于变量来说，double 类型比 float 类型的精度要高。double 精度更高，是指它存储的小数位数更多，但是输出默认都是 6 位小数，如果你想输出更多小数，可以自己控制，比如 %.10lf 就输出 10 位小数。

所以一般情况下 double 类型的占位符可以用 %lf。

**size_t**
在C语言标准库函数原型使用的很多，数值范围一般是要大于int和unsigned.但凡不涉及负值范围的表示size取值的，都可以用size_t；比如array[size_t]。  
size_t 在``stddef.h``头文件中定义。
在其他常见的宏定义以及函数中常用到有：
- sizeof运算符返回的结果是size_t类型；
- void *malloc(size_t size)...

## 字符串
比较特殊一点，专门写
怎么声明和操作字符串：
https://www.runoob.com/cprogramming/c-strings.html

声明字符串
```C
char [] s; // 在stack里，s指向数组第一个字符
char *s; // 在data segment里，s指向数组第一个字符
```
两种方式有细微差别
1. If we create a string as a ``char[]``, we can modify its characters because its memory lives in our stack space. 
We cannot set a ``char[]`` equal to another value, **because it is not a pointer; it refers to the block of memory reserved for the original array**. 
2. If we create a string as a ``char *``, we cannot modify its characters because its memory lives in the data segment. We can set a ``char *``equal to another value, **because it is a  reassign-able pointer.**
	- ``sizeof()`` 永远返回8(size of pointer) 

字符串怎么做参数：
（TODO）

string operation:
![](https://i.imgur.com/sKFrjIk.png)



# 运算符
``sizeof()``  
``typeof()``

# 函数
- 自己定义的：略
- 内置函数：
- 还有linux函数和系统调用的接口(例如``fork()``)(???不知道我理解的对不对)

```C
stract() // 连接字符串
memcpy() // 复制内存到另一个位置
```

## 系统调用
https://www.ibm.com/developerworks/cn/linux/kernel/syscall/part1/index.html
**What**
**Linux内核中设置了一组用于实现各种系统功能的子程序，称为系统调用**。用户可以通过系统调用命令在自己的应用程序中调用它们。从某种角度来看，系统调用和普通的函数调用非常相似。区别仅仅在于，系统调用由操作系统核心提供，运行于核心态；而普通的函数调用由函数库或用户自己提供，运行于用户态。二者在使用方式上也有相似之处，在下面将会提到。

**Why**
**系统调用是实现你的想法的简洁有效的途径。**  
***很多已经被我们习以为常的C语言标准函数，在Linux平台上的实现都是靠系统调用完成的**。（很多库中使用了系统调用，意味着很多时候我们不用自己显式的使用）

**How**
一般的，进程是不能访问内核的。它不能访问内核所占内存空间也不能调用内核函数。CPU硬件决定了这些（这就是为什么它被称作"保护模式"）。系统调用是这些规则的一个例外。**其原理是进程先用适当的值填充寄存器，然后调用一个特殊的指令，这个指令会跳到一个事先定义的内核中的一个位置**（当然，这个位置是用户进程可读但是不可写的）。在Intel CPU中，这个由中断0x80实现。硬件知道一旦你跳到这个位置，你就不是在限制模式下运行的用户，而是作为操作系统的内核--所以你就可以为所欲为。

**进程可以跳转到的内核位置叫做sysem_call。这个过程检查系统调用号，这个号码告诉内核进程请求哪种服务。**然后，它查看系统调用表(sys_call_table)找到所调用的内核函数入口地址。接着，就调用函数，等返回后，做一些系统检查，最后返回到进程（或到其他进程，如果这个进程时间用尽）。如果你希望读这段代码，它在<内核源码目录>/kernel/entry.S，Entry(system_call)的下一行。

``_syscall*()``:
**宏**  
它们的作用是形成相应的系统调用函数原型，供我们在程序中调用。我们展开一下就可以直接用啦。
```C
#include<linux/unistd.h> /*定义宏_syscall1*/
#include<time.h>     /*定义类型time_t*/
_syscall1(time_t,time,time_t *,tloc)    /*宏，展开后得到time()函数的原型*/
main()
{
        time_t the_time;
        the_time=time((time_t *)0); /*调用time系统调用*/
        printf("The time is %ld\n",the_time);
}
```

## 函数参数
- 值传递：
形参是实参的拷贝，改变形参的值并不会影响外部实参的值。从被调用函数的角度来说，值传递是单向的（实参->形参），参数的值只能传入，不能传出。当函数内部需要修改参数，并且不希望这个改变影响调用者时，采用值传递。

- 指针传递：
形参为指向实参地址的指针，当对形参的指向操作时，就相当于对实参本身进行的操作

- 引用传递：（传地址）
形参相当于是实参的“别名”，对形参的操作其实就是对实参的操作，在引用传递过程中，被调函数的形式参数虽然也作为局部变量在栈中开辟了内存空间，但是这时存放的是由主调函数放进来的实参变量的地址。**被调函数对形参的任何操作都被处理成间接寻址，即通过栈中存放的地址访问主调函数中的实参变量**。正因为如此，被调函数对形参做的任何操作都影响了主调函数中的实参变量

# C 作用域规则
- 在函数或块内部的局部变量
- 在所有函数外部的全局变量
- 在形式参数的函数参数定义中

**作用域的区别**
**初始化的区别**
- 当局部变量被定义时，系统不会对其初始化
- 定义全局变量时，系统会自动对其初始化

**内存中的区别**
https://www.runoob.com/w3cnote/cpp-static-usage.html

# 数组
## 基本操作
```C
double balance[10];
double balance[5] = {1000.0, 2.0, 3.4, 7.0, 50.0};
double balance[] = {1000.0, 2.0, 3.4, 7.0, 50.0};

balance[4] = 50.0;  // 赋值
double salary = balance[9];  // 访问
```

## C 传递数组给函数
如果数组作为参数，其实传递的是指针变量  
所以有一下三种把数组作为参数的方式
**数组名是一个指向数组中第一个元素的常量指针
**
```
// 形式参数是一个指针（您可以在下一章中学习到有关指针的知识）：
void myFunction(int *param)
{
	...
}

// 方式 2
形式参数是一个已定义大小的数组：
void myFunction(int param[10])
{
	...	
}

// 方式 3
形式参数是一个未定义大小的数组：
void myFunction(int param[])
{
	...
}
```

Q: 为什么传进去数组指针``param``以后地址变了？？？但是``param[0]``地址没变
A: 

## 从函数返回数组
https://www.runoob.com/cprogramming/c-return-arrays-from-function.html
- 声明返回指针变量的函数
- 待返回的函数需要声明成``static``

> 随机数小知识
> srand((unsigned)time(NULL))是初始化随机函数种子：
 1、是拿当前系统时间作为种子，由于时间是变化的，种子变化，可以产生不相同的随机数。计算机中的随机数实际上都不是真正的随机数，如果两次给的种子一样，是会生成同样的随机序列的。 所以，一般都会以当前的时间作为种子来生成随机数，这样更加的随机。
 2、使用时，参数可以是unsigned型的任意数据，比如srand（10）；
 3、如果不使用srand，用rand（）产生的随机数，在多次运行，结果是一样的。

# 枚举
用的时候再说

# 指针
```C
#include <stdio.h>

int main() {
    int var = 20;   /* 实际变量的声明 */
 	/* 指针变量的声明,在变量声明的时候，
	如果没有确切的地址可以赋值，
	为指针变量赋一个 NULL 值是一个良好的编程习惯。 */
    int *ip = NULL;       
    int addr;

    ip = &var;  /* 在指针变量中存储 var 的地址 */
    addr = &var;  /* 这里发生了类型转换，&var 是一个pointer */

    printf("Value of var variable: %d\n", var);
    printf("Value of addr variable: %p\n", addr);
    printf("Address of var variable: %p\n", &var);

    /* 在指针变量中存储的地址 */
    printf("Value stored in ip variable: %p\n", ip);
    printf("Address of ip variable: %p\n", &ip);

    /* 使用指针访问值 */
    printf("Value of *ip variable: %d\n", *ip);
    printf("Value of the address of var points to: %d\n", *&var);

    return 0;
}
```

## 指针的算数运算
应用：数组的遍历
```C
int *ptr;
ptr++;  // 每次移动sizeof(int)
```

## 函数指针
函数指针是指向函数的指针变量。
```
// 函数是怎么被存储的
// TODO： https://www.cnblogs.com/clover-toeic/p/3757091.html
```

使用函数指针意味着C语言可以像Python，JS一样使用callback，只需要把函数指针作为参数传到函数中

# 函数调用过程
https://www.cnblogs.com/clover-toeic/p/3755401.html

**寄存器**
函数调用过程通常使用**堆栈**实现，每个用户态进程对应一个调用栈结构(call stack)。编译器使用堆栈传递**函数参数、保存返回地址、临时保存寄存器原有值(即函数调用的上下文)**以备恢复以及存储本地局部变量。

寄存器是处理器加工数据或运行程序的重要载体，用于存放程序执行中用到的数据和指令。因此**函数调用栈的实现与处理器寄存器组密切相关**。
在x86处理器中：
- EIP(Instruction Pointer)是指令寄存器，指向处理器下条等待执行的指令地址(代码段内的偏移量)，每次执行完相应汇编指令EIP值就会增加。
- ESP(Stack Pointer)是堆栈指针寄存器，存放执行函数对应栈帧的栈顶地址(也是系统栈的顶部)，且始终指向栈顶
- EBP(Base Pointer)是栈帧基址指针寄存器，存放执行函数对应栈帧的栈底地址，用于C运行库访问栈中的局部变量和参数。

**栈帧结构**

函数调用堆栈中会有多个函数的信息。**每个未完成运行的函数占用一个独立的连续区域，称作栈帧(Stack Frame)**。栈帧存放着函数参数，局部变量及恢复前一栈帧所需要的数据等。（**栈帧是堆栈操作（压入/弹出）的最小单元**）

栈帧的**边界由栈帧基地址指针EBP和堆栈指针ESP界定**(指针存放在相应寄存器中)。EBP指向当前栈帧底部(高地址)，在当前栈帧内位置固定；ESP指向当前栈帧顶部(低地址)，当程序执行时ESP会随着数据的入栈和出栈而移动。因此函数中对大部分数据的访问都基于EBP进行。（没记错的话windows和linux都是从大端往小存储的）

图为主调函数调用被调函数的过程：
![](https://images0.cnblogs.com/i/569008/201405/271644419475745.jpg)
- 主调函数压入参数
- 压入EIP指针保存主调函数返回地址（同时也是下一条待执行指令地址）
- 进入被调函数，被调函数将主调函数的帧基指针EBP入栈，并将主调函数的栈顶指针ESP值赋给被调函数的EBP(作为被调函数的栈底)，接着改变ESP值来为函数局部变量预留空间
- 本级调用结束后，将EBP指针值赋给ESP，使ESP再次指向被调函数栈底以释放局部变量
- 再将已压栈的主调函数帧基指针弹出到EBP，并弹出返回地址到EIP。ESP继续上移越过参数，最终回到函数调用前的状态，即恢复原来主调函数的栈帧。如此递归便形成函数调用栈。

>  **EBP指针在当前函数运行过程中(未调用其他函数时)保持不变。在函数调用前，ESP指针指向栈顶地址，也是栈底地址(和EBP同样地址)。**在函数完成现场保护之类的初始化工作后，ESP会始终指向当前函数栈帧的栈顶，此时，若当前函数又调用另一个函数，则会将此时的EBP视为旧EBP压栈，而与新调用函数有关的内容会从当前ESP所指向位置开始压栈。

Q: 解释传值和传引用的区别
A: 函数调用以值传递时，传入的实参与被调函数内操作的形参两者存储地址不同，因此被调函数无法直接修改主调函数实参值(对形参的操作相当于修改实参的副本)。为达到修改目的，需要向被调函数传递实参变量的指针(即变量的地址)。

# 内存管理
静态分配内存很简单，声明一下就自动分配好了，如何动态管理内存？
当动态分配内存时，您有完全控制权，可以传递任何大小的值。而那些预先定义了大小的数组，一旦定义则无法改变大小。

具体应用就是我们声明一个指针，然后给这个指针手动分配大小。

```C
// 在内存中动态地分配 num 个长度为 size 的连续空间，并将每一个字节都初始化为 0。返回分配空间起始地址的指针。
void *calloc(int num, int size);

// 该函数释放 address 所指向的内存块,释放的是动态分配的内存空间。
void free(void *address);

// 堆区分配一块指定大小的内存空间，用来存放数据。这块内存空间在函数执行完成后不会被初始化(它们的值是未知的)。返回分配空间起始地址的指针。
void *malloc(int num);

// 该函数重新分配内存，把内存扩展到 newsize
void *realloc(void *address, int newsize);

// void * 类型表示未确定类型的指针。C、C++ 规定 void * 类型可以通过类型转换强制转换为任何其它类型的指针。
```

# 函数
## ``error()``
## ``strtol()``
参考： http://www.runoob.com/cprogramming/c-function-strtol.html
```C
#include <stdlib.h>

long int strtol(const char *nptr, char **endptr, int base);
```

**描述**
C 库函数 ``long int strtol(const char *str, char **endptr, int base)`` 把参数 str 所指向的字符串根据给定的 base 转换为一个长整数（类型为 long int 型），base 必须介于 2 和 36（包含）之间，或者是特殊值 0。

**参数**
- str -- 要转换为长整数的字符串。
- endptr -- 对类型为 char* 的对象的引用，其值由函数设置为 str 中数值后的下一个字符。
- base -- 基数，必须介于 2 和 36（包含）之间，或者是特殊值 0。

> ``int a; int* a; int** a; int (*a)[]; int (*a)(int)``
> https://blog.csdn.net/wang13342322203/article/details/85228415
> 
- a) int a;表示一个内存空间，这个空间用来存放一个整数（int）；
- b) int* a;表示一个内存空间，这个空间用来存放一个指针，这个指针指向一个存放整数的空间，即a)中提到的空间；
- c) int** a;表示一个内存空间，这个空间用来存放一个指针，这个指针指向一个存放指针的空间，并且指向的这个空间中的指针，指向一个整数。也简单的说，指向了一个b)中提到的空间；
- d) int (*a)[4];表示一个内存空间，这个空间用来存放一个指针，这个指针指向一个长度为4、类型为int的数组；和int** a的区别在于，++、+=1之后的结果不一样，其他用法基本相同。
- 以上四种类型见上图表示。
- e) int (*a)(int);表示一个内存空间，这个空间用来存放一个指针，这个指针指向一个函数，这个函数有一个类型为int的参数，并且函数的返回类型也是int。
- f)int *p[]和int (*p)[]; 前者是指针数组，后者是指向数组的指针。更详细地说。