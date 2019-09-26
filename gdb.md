# GDB and Debugging
https://web.stanford.edu/class/archive/cs/cs107/cs107.1202/resources/gdb

- first use ``-g -Og`` flag in gcc
- then ``gdb [excutable file name]``
- then it will show prompt

## in the prompt
### run
run (r)
``run [argvs]``: run the program with arguments

### Breakpoints
break (b)
可以是 function name 或者 line num
```
(gdb) break main
Breakpoint 1 at 0x400a6e: file myprogram.c, line 44.

(gdb) break myprogram.c:47
Breakpoint 2 at 0x400a8c: file myprogram.c, line 47.

(gdb) delete 2

(gdb) break 2 if i == count - 1

(gdb) continue (c)  // to the next breakpoint
(gdb) finish  // to the end
(gdb) next (n)/ step (s)  // run a single line
```

查看variables
```
(gdb) print [variable name]

(gdb) up
(gdb) down
```
prints out the arguments (parameters) to the current function you're in:

```
(gdb) info args 
```

## Stack frame
显示函数调用栈
``backtrace``


