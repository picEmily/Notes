# Memcheck: memory leak VS memory errors
https://web.stanford.edu/class/archive/cs/cs107/cs107.1202/resources/valgrind
- memory leak
- memory errors

 >When a program **dynamically allocates memory** and **forgets to later free it**, it creates a leak. A memory leak generally **won't** cause a program to misbehave, crash, or give wrong answers, and is not an urgent situation. 
 >A memory error, on the other hand, is a red alert. **Reading uninitialized memory, writing past the end of a piece of memory, accessing freed memory**, and other memory errors can have significant consequences.

**Note:**
内存相关的错误可能因为各种原因导致**难以重现**！所以要尽早memcheck。给的例子是
```C
char *copy = malloc(strlen(buffer));
strcpy(copy, buffer);
```
an instance of the classic strlen + 1 bug, The code doesn't allocate enough space for the '\0' character.

但是可能实际不会出错，因为：
Despite the code being clearly wrong, it often may appear to "work" because malloc commonly rounds up the requested size to the nearest multiple of 4 or 8 and that extra space may cover the shortfall. 

# Analysis of valgrind info
## error
- ``Invalid read/write of size X`` The program was observed to read/write X bytes of memory that was invalid. Common causes include accessing beyond the end of a heap block, accessing memory that has been freed, or accessing into an unallocated region such as from use of a uninitialized pointer.
- ``Use of uninitialised value`` or ``Conditional jump or move depends on uninitialised value(s)`` The program read the value of a memory location that was **not previously written to**, i.e. uses random junk. The second more specifically indicates the read occurred in the test expression in an if/for/while. Make sure to initialize all of your variables! **Remember that just declaring a variable doesn't put anything in its contents**--if you want an int to be 0 or a pointer to be NULL, you must explicitly state so. Note that Valgrind will silently allow a program to propagate an uninitialized value along from variable to variable; the complaint will only come when(if) it eventually uses the value which may be far removed from the root of the error. When tracking down an uninitialized value, run Valgrind with the additional flag **--track-origins=yes** and it will report the entire history of the value back to the origin which can be very helpful.

```C
// Use of uninitialised value of size 8
char *uninitializedPtr;

printf("strlen(uninitializedPtr) = %zu\n", strlen(uninitializedPtr));

// Conditional jump or move depends on uninitialised value(s) 
char stackArray[10];
strncpy(stackArray, "Stanford", 3);
```
- ``Source and destination overlap in memcpy()`` The program attempted to copy data from one location to another and the range to be read intersects with the range to be written. Transferring data between overlapping regions using memcpy can garble the result; memmove is the correct function to use in such a situation.
- ``Invalid free()`` The program attempted to free a non-heap address or free the same block more than once.
- ``Bad permissions for mapped region at address 0x4009F4``。``char *stringConstant = "Hello, world!";``声明的字符串是read only的，所以不可以再改变其值。

```C
char *stringConstant = "Hello, world!";
strcpy(stringConstant, "Stanford");
```

## leak
### example:

```C
#include<stdlib.h>
#include<stdio.h>
#include<time.h>

/* This program malloc heap but not free it */

const int ARR_SIZE = 1000;

int main() {
    // create an array of ARR_SIZE ints
    int *intArray = malloc(sizeof(int) * ARR_SIZE);

    // populate them
    for (int i=0; i < ARR_SIZE; i++) {
        intArray[i] = i;
    }

    // print one out
    // first, seed the random number generator
    srand(time(NULL));
    int randNum = rand() % ARR_SIZE;

    printf("intArray[%d]: %d\n", randNum, intArray[randNum]);

    // end without freeing!
    return 0;
}
```

> It's pretty easy to tell when there's a leak: **the alloc/free counts don't match up and you get a LEAK SUMMARY section at the end.** (note that it says 2 allocs even though we only call malloc once. Why? Because srand/time allocate memory in their implementations, but they free it as well!). **Valgrind also gives a little data about each leak** -- how many bytes, how many times it happened, and where in the code the original allocation was made. Multiple leaks attributed to the same cause are coalesced into one entry that summarize the total number of bytes across multiple blocks. Here, the program memoryLeak.c requests memory from the heap and then ends without freeing the memory. This is a memory leak, and valgrind correctly finds the leak: "definitely lost: 4,000 bytes in 1 blocks"

### Valgrind categorizes leaks
- definitely lost: heap-allocated memory that was never freed to which the program no longer has a pointer. Valgrind knows that you once had the pointer, but have since lost track of it. This memory is definitely orphaned.
- indirectly lost: heap-allocated memory that was never freed to which the only pointers to it also are lost. For example, if you orphan a linked list, the first node would be definitely lost, the subsequent nodes would be indirectly lost.
- possibly lost: heap-allocated memory that was never freed to which valgrind cannot be sure whether there is a pointer or not.
- still reachable: heap-allocated memory that was never freed to which the program still has a pointer at exit.

**Notes:**
- leak是因为没有free memory。有很多原因导致没有free：忘了，找不到指针了
- libary functions有可能用``malloc()``，例如读文件不关的话也会造成leak