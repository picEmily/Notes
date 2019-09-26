# gcc
https://blog.csdn.net/u011192270/article/details/50224267
GNU Compiler Collection" (gcc)
gcc会完成： 预处理，编译，汇编，链接

gcc的flag：
TODO
- ``-v``: verbose

# Makefile
ref: 
https://seisman.github.io/how-to-write-makefile/overview.html

https://web.stanford.edu/class/archive/cs/cs107/cs107.1202/resources/make

要点整理：

## 编译和链接：
无论是C、C++、还是pas，首先要把源文件编译成中间代码文件，在Windows下也就是 .obj 文件，UNIX下是 .o 文件，即 Object File，这个动作叫做**编译（compile）**。然后再把大量的Object File合成执行文件，这个动作叫作**链接（link）**。   
     
- 编译时，编译器需要的是语法的正确，函数与变量的声明的正确。只要所有的语法正确，编译器就可以编译出中间目标文件。一般来说，每个源文件都应该对应于一个中间目标文件（O文件或是OBJ文件）。 
- 链接时，通常是你需要告诉编译器头文件的所在位置（头文件中应该只是声明，而定义应该放在C/C++文件中）。
主要是链接函数和全局变量，所以，我们可以使用这些中间目标文件（O文件或是OBJ文件）来链接我们的应用程序。链接器并不管函数所在的源文件，只管函数的中间目标文件（Object File），在大多数时候，由于源文件太多，编译生成的中间目标文件太多，而在链接时需要明显地指出中间目标文件名，这对于编译很不方便，所以，我们要给中间目标文件打个包，在Windows下这种包叫“库文件”（Library File)，也就是 .lib 文件，在UNIX下，是Archive File，也就是 .a 文件。

总结一下，源文件首先会生成中间目标文件，再由中间目标文件生成执行文件。在编译时，编译器只检测程序语法，和函数、变量是否被声明。如果函数未被声明，编译器会给出一个警告，但可以生成Object File。而在链接程序时，链接器会在所有的Object File中找寻函数的实现，如果找不到，那到就会报链接错误码（Linker Error），在VC下，这种错误一般是：Link 2001错误，意思说是说，链接器未能找到函数的实现。你需要指定函数的ObjectFile.

## Makefile
make命令执行时，需要一个 Makefile 文件，以**告诉make命令需要怎么样的去编译和链接程序。**
(通过编辑 Makefile 文件，可以简化编译的过程，比如只编译修改过的文件)

### Makefile规则
**Macros:**
- 定义一些常数, 例如： ``CC = gcc``; 引用常数的时候使用``$(CC)``即可
- 几个特殊的build-in macros: 
``$@``，``$^``，``$<``代表的意义分别是： 
$@--name of the current target ，$^--its list of dependencies，$<--第一个依赖文件。

**Targets**
```
target-name : dependencies
    action
```

1. make会在当前目录下找名字叫“Makefile”或“makefile”的文件。
如果找到，它会找文件中的第一个目标文件（target）,作为生成的文件。
2. 如果targe不存在，或是edit所依赖的后面的 dependencies文件的文件修改时间要比target这个文件新，那么，他就会执行后面所定义的action命令来生成target文件。
3. 如果target所依赖的.o文件也存在，那么make会在当前文件中找目标为.o文件的依赖性，如果找到则再根据那一个规则生成.o文件。（这有点像一个堆栈的过程）

Makefile 可以自动推导依赖关系