Introducing ARM assembly language
http://www.toves.org/books/arm/

cheat sheet
# 背景知识
- **machine language**:
	- 0和1
	- 计算机读
	- machine language的设计叫做指令集(ISA: **instruction set architecture**)
- **assembly language**:
	- 指令
	- 人读
- **assembler**:把assembly language翻译成machine language

不同的指令集
- win电脑：x86（IA32）
- PS3，XBOX：PowerPC
- ARM's ISA

# Registers
- 16个32bits register
- **opcode**：MOV等，（区别condition codes）
- **immediate**: #1
- 	要求：Any immediate value must be rotated by an even number of places to reach an eight-bit value. （可以旋转成8bits number）
- flags: 
	- 	Z: Zero flag
	- 	C: Carry flag
	- 	N: Negative flag
	- 	V: Overflow flag

Q: 什么时候会用到flag：
A: 指令``S``结尾，flags会被更新。另外还有``TST``, ``TEQ``, ``CMP``, and ``CMN``也可以更新flags

branch：check flags and jump
B：Branch
BNE：Branch Not Equal

shifting
- LSL	logical shift left
- LSR	logical shift right
- ASR	arithmetic shift right
- ROR	rotate right

Q:算数和逻辑有什么区别？
A:

# Cheat Sheet
## ARM's basic arithmetic instructions
这里的都是opcode，除了``TST``, ``TEQ``, ``CMP``, and ``CMN``之外都可以加上``S``。这四个本身隐式地更新flags。
```
0.	AND regd, rega, argb	   	regd ← rega & argb
1.	EOR regd, rega, argb		regd ← rega ^ argb
2.	SUB regd, rega, argb		regd ← rega − argb
3.	RSB regd, rega, argb		regd ← argb - rega
4.	ADD regd, rega, argb		regd ← rega + argb
5.	ADC regd, rega, argb		regd ← rega + argb + carry
6.	SBC regd, rega, argb		regd ← rega − argb − !carry
7.	RSC regd, rega, argb		regd ← argb − rega − !carry
8.	TST rega, argb		set flags for rega & argb
9.	TEQ rega, argb		set flags for rega ^ argb
10.	CMP rega, argb		set flags for rega − argb
11.	CMN rega, argb		set flags for rega + argb
12.	ORR regd, rega, argb		regd ← rega | argb
13.	MOV regd, arg		regd ← arg
14.	BIC regd, rega, argb		regd ← rega & ~argb
15.	MVN regd, arg		regd ← ~argb 
```

## ARM's condition codes
ARM指令可以和condition codes结合，这样只有在某些flags的组合下才能执行。condition codes一般在opcode的结尾，但是之前需要有更新flags的指令

```
0.	EQ	   	equal	   	Z
1.	NE		not equal		!Z
2.	CS or HS		carry set / unsigned higher or same		C
3.	CC or LO		carry clear / unsigned lower		!C
4.	MI		minus / negative		N
5.	PL		plus / positive or zero		!N
6.	VS		overflow set		V
7.	VC		overflow clear		!V
8.	HI		unsigned higher		C && !Z
9.	LS		unsigned lower or same		!C || Z
10.	GE		signed greater than or equal		N == V
11.	LT		signed less than		N != V
12.	GT		signed greater than		!Z && (N == V)
13.	LE		signed greater than or equal		Z || (N != V)
14.	AL or omitted		always		true
```
## Memory
```
STR r1, [r2]		;r1的数据存到r2存的地址里面
LDR r1, [r2]		;取r2存的地址的数据，存到r1
```

ten addressing modes
加括弧，意思是地址内的值
```
[Rn, #±imm]	Immediate offset
Address accessed is imm more/less than the address found in Rn. Rn does not change.

[Rn]	Register
Address accessed is value found in Rn. This is just shorthand for [Rn, #0].

[Rn, ±Rm, shift]	Scaled register offset
Address accessed is sum/difference of the value in Rn and the value in Rm shifted as specified. Rn and Rm do not change values.

[Rn, ±Rm]	Register offset
Address accessed is sum/difference of the value in Rn and the value in Rm. Rn and Rm do not change values. This is just shorthand for [Rn, ±Rm, LSL #0].

[Rn, #±imm]!	Immediate pre-indexed
Address accessed is as with immediate offset mode, but Rn's value updates to become the address accessed.

[Rn, ±Rm, shift]!	Scaled register pre-indexed
Address accessed is as with scaled register offset mode, but Rn's value updates to become the address accessed.

[Rn, ±Rm]!	Register pre-indexed
Address accessed is as with register offset mode, but Rn's value updates to become the address accessed.

[Rn], #±imm	Immediate post-indexed
Address accessed is value found in Rn, and then Rn's value is increased/decreased by imm.

[Rn], ±Rm, shift	Scaled register post-indexed
Address accessed is value found in Rn, and then Rn's value is increased/decreased by Rm shifted according to shift.

[Rn], ±Rm	Register post-indexed
Address accessed is value found in Rn, and then Rn's value is increased/decreased by Rm. This is just shorthand for [Rn], ±Rm, LSL #0.
```

directives: 大概就是存一个数组，指定一个别名
- DCD：Define Constant Double-Words (32bits?) 此处存疑
- DCB：Define Constant Bytes (8bits)

```
primes  DCD   2, 3, 5, 7, 11, 13, 17， 19	；指定数组 primes	
ADD R0, PC, #primes  						; load address of primes[0] into R0
        LDR R1, [R0, #16]    				; load primes[4] into R1

greet   DCB   "hello world\n", 0
array   % 120  ; reserve 120 bytes of memory, which can hold 30 ints
```

连续loads
```
LDMIA, STMIA	Increment after
We start loading from the named address and into increasing addresses.

LDMIB, STMIB	Increment before
We start loading from four more than the named address and into increasing addresses.

LDMDA, STMDA	Decrement after
We start loading from the named address and into decreasing addresses.

LDMDB, STMDB	Decrement before
We start loading from four less than the named address and into decreasing addresses.
```

# Stack Frame
- ``PC``: ``R15``
- ``LR``: ``R14`` 返回地址或异常返回地址
- ``SP``: ``R13`` 栈顶指针
- ``FP``: ``R11`` 栈底指针
- ``R12``：``SP`` push/pop through ``R12``

# 代码分析
```C
int global;

void part_a(void)
{
    int num = global;

    num = -num;
    num = num*10;
    num =  (num & ~(2 << 3)) * (((12 - 15)/4) + num);
    global = num;
}

void part_b(void)
{
    int num = global;

    if (num < 5) {
        num++;
    }
    global = num;
}

void part_c(void)
{
    int delay = 0x3f00;
    while (--delay != 0) ;
}

void part_d(void)
{
    int *ptr = &global;
    char *cptr = (char *)ptr;
    int n = global;

    *ptr = 107;      // compare to next line
    *(char *)ptr = 107;

    ptr[5] = 13;     // compare to next line
    cptr[5] = 13;

    n = *(ptr + n);  // compare to next line
    n = ptr[n];

    global = n;
}
```
```
part_a:
  ldr r1, .L2
  ldr r3, [r1]
  rsb r3, r3, #0
  add r3, r3, r3, lsl #2
  mov r2, r3, asl #1
  bic r3, r2, #16
  mul r3, r2, r3
  str r3, [r1]
  bx lr
.L2:
  .word global
part_b:
  ldr r3, .L6
  ldr r3, [r3]
  cmp r3, #4
  addle r3, r3, #1
  ldr r2, .L6
  str r3, [r2]
  bx lr
.L6:
  .word global
part_c:
  mov r3, #16128
.L9:
  subs r3, r3, #1
  bne .L9
  bx lr
part_d:
  ldr r3, .L11
  ldr r1, [r3]
  mov r2, #107
  str r2, [r3]
  strb r2, [r3]
  mov r2, #13
  str r2, [r3, #20]
  strb r2, [r3, #5]
  ldr r2, [r3, r1, asl #2]
  ldr r2, [r3, r2, asl #2]
  str r2, [r3]
  bx lr
.L11:
  .word global
```
part_a
- 没有取负号指令
	- ``rsb r3, r3, #0``意思是``r3 = 0-r3``
- 乘法通过shift和add实现

part_b
- 这里的if分支内的语句很短，所以没有额外的branch代码
- ``r3-4 >= 0``的时候执行``ADD``

part_c
- 没啥好说的，就是``bne``条件跳转

part_d
- 大量``ldr``，``str``操作
- ``strb``代表只看一个字节