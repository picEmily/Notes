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

## examine

https://web.stanford.edu/class/archive/cs/cs107/cs107.1202/lab4/

The examine command, x (click here for documentation) is a helpful command to examine the contents of memory independent of the type of data at a memory location. It's like print, but for generic memory rather than a specific type of variable. For instance, you can use x to print out a certain number of bytes starting at a given address. If you have a pointer ptr, for instance, you could print out the 8 bytes starting at the address it contains in hex by executing x/8bx ptr. The optional parameters after the slash specify what you would like to print. The first one (e.g. 8 or 2) lets you specify how many you would like to examine, the second (e.g. b or w) specifies whether you would like to print out bytes, words (a word is 4 bytes), etc., and the third (e.g. x) specifies how you would like to print them out (e.g. x for hex, d for decimal). Check out the documentation link for a full summary. 

```C
int n1 = 0xffffffff
int *ptr = &n1;
int nums[] = {0x12345678, 0x00000000}

(gdb) x/4bx ptr  // 0xff 0xff 0xff 0xff
(gdb) x/2bx ptr  // 0xff 0xff
(gdb) x/1wx ptr  // 0xffffffff
(gdb) x/8bx nums  // 0x12 0x34 0x56 0x78 0x00 0x00 0x00 0x00

```

## array
- if it is a declared array:

```C
int nums[3] = {0, 1 ,2};

// (gdb) p nums
// {0, 1, 2}
```
- if it is a pointer, or parameter passed in a fn
``p ele[1]@count`` means print from ele[1] and print 5 elements in ele

```
void fn(int *nums) {
	...
	// (gdb) p nums  // 0x12345678
	// (gdb) p *nums  // 0
	// (gdb) p nums[0]@2  // {0, 1}
}
```
