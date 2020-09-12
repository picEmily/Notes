 # 场景分析

**海量数据，简单状态**

1. 给40亿个不重复的unsigned int的整数，没排过序的，然后再给一个数，如何快速判断这个数是否在那40亿个数当中
2. 使用位图法判断整形数组是否存在重复
3. 使用位图法进行整形数组排序
4. 在2.5亿个整数中找出不重复的整数，注，内存不足以容纳这2.5亿个整数   

# 位图是什么

在STL中有一个bitset容器，其实就是位图法，引用bitset介绍：

A bitset is a special container class that is designed to store bits (elements with only two possible values: 0 or 1,`true` or `false`, ...).The class is very similar to a regular array, but optimizing for space allocation: each element occupies only one bit (which is eight times less than the smallest elemental type in C++: `char`).Each element (each bit) can be accessed individually: for example, for a given bitset named `mybitset`, the expression `mybitset[3]` accesses its fourth bit, just like a regular array accesses its elements.

> 位图就是一个特殊的容器，用来存放bits（每个bits可以表示两种状态0，1）。和普通的数组比起来优化了空间分配，**每个元素只占用1bit**，且每个元素也可以被独立的随机访问。
>
> 从描述中可以知道：占用空间很小，说白了就是个数组

例子：用位图存一个 ``int[1,2,3,5,7,15]``

| 15   | 14   | 13   | 12   | 11   | 10   | 9    | 8    | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| 1    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 1    | 0    | 1    | 1    | 1    | 1    | 1    | 0    |

原来的数组用了6 * 4 Bytes

现在用位图只用了2 Bytes

# 题目解答

1. 
   1. 遍历数组，存入位图（4billion bits = 4G bits）
   2. 判断数是否在位图中（随机访问，不用遍历，O(1)）
2.  
   1. 遍历数组，存入位图
   2. 遍历的过程中能发现是否有重复的
3.  
   1. 遍历数组，存入位图
   2. 把存在的数顺序输出就好了
4.  
   1. 采用2-Bitmap（每个数分配2bit，00表示不存在，01表示出现一次，10表示多次，11无意义）。
   2. 其实，这里可以使用两个普 通的Bitmap，即第一个Bitmap存储的是整数是否出现，如果再次出现，则在第二个Bitmap中设置即可。这样的话，就可以使用简单的1- Bitmap了。