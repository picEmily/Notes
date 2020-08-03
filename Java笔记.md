# Java beginning
https://www.youtube.com/watch?v=eIrMbAQSU34&list=PLTjRvDozrdlxCs_3gaqd120LcGxmfe

## java editions:
- se: standard
- ee: large program
- me: for monbile
- java card

## Journey(重要：学习路线)
### Fundamentals
- type
- control flow
- clean code
- debug
- package for deployment

### OOP
### Core APIs
standard library
### Advanced
- stream
- tread
- database programming

# Environment
- jdk download
	- compiler, run time environment
- ide

# Anatomy
##functions
basic structure
- return type
- every java program must have ``main()``
- class is the container of one or more functions
	- ``class Main {}``
	- inside class, functions are called methods
- **access modifier** before classes and methods: ``public``
- 驼峰法命名，类名需要首字母大写

## The first Java app
> **package**: group related packages (a name space for classes)

project structure
- in the src dir: package-class-field-method(.java extension)
- the ``main()`` method should always be static
- ``c``:class
- ``f``:field(就是我理解的attribute)
- ``m``:method 
## How Java code executed
- Compilation: 
	- **Source code(.java) --> Java compiler --> Java Byte code(.class)**
- Execution:
	- ``javac Main.java``: Compile source code to get ``Main.class``. This will be in the ``out`` folder
	- if we have JRE, we can run .class file in any system. **JVM takes java byte code to native code that os can understand**
	- ``java [package name].[class name]``: invoke JVM

# Type
- Primitive(8):
	- byte, short, int, long
	- float, double
	- char
	- boolean
- **Reference:** objects
	- We should **allocate memory**
	- They have methods
	- from ``java.lang``(automatically imported): ``java.lang.Integer``
	- from ``java.util``: ``java.util.Date``
	- from ... 还有很多对象

## 区别
memory locations:
- primitive variables: **copy by value**
- reference variables: 对象的名字只是一个存储实际存储地址的变量。普通的等号只是对象的浅复制，意味着他们指向同一个地址。

> 注意: long 需要在数字后面加上L，例如12332141231451L（默认是int）
> float 需要在数字后面加上F，例如3.14F（默认是double）

strings:
- strings are immutable: 我们用各种method会返回一个新的string
- ``String msg = new String("Hello World")``
等同于 ``String msg = "Hello World"``
- ``+`` 是可以用的（我估计是被operation overload过）
- 常用：``indexOf()``，``replace()``

arrays
- ``int[] numbers = new int[5];``
- ``int[] numbers = {1,2,3,4,5}``
- ``numbers[0]; // index``
- ``System.out.println(Arrays.toString(numbers));`` (``Arrays.toString()``是overloading的一个很好的例子，implemented in multiple types) // 打印二维数组需要用``Arrays.deepToString()``

constant
- ``final``关键字
- - 变量名所有字母大写

explicit casting
(double)10

implicit casting(隐式转换/自动转换)
byte > short > int > long > float > double
```java
// 整型转换成整型
short x = 1;
int y = x + 2;

// 整型转换成浮点型
double x = 1.1;
doubel y = x + 2 // 2 is actually 2.0
```

How to casting string and numbers
using wrapper classes 
``Integer.parseInt("1") // takes a string and returns an int``

## Math class
```java
Math.round()
Math.ceil()
Math.floor()
Math.max()
Math.random()
```

## Formatting numbers
how to represent 10%, $10, etc. 
```java
// 抽象方法和工厂
// NumberFormat is abstract class
// we can't use new to create a instance
// we have to use the factory method
NumberFormat currency = NumberFormat.getCurrencyinstance();
String ret = currency.format(10.5);
```

## Reading input
```java
Scanner scanner = new Scanner(system.in); // from terminal
byte age = scanner.nextByte(); // 会读取一个Byte
String name = scanner.next(); // 读取字符串
```