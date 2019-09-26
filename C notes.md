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

