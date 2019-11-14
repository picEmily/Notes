# C++ 是如何实现set和map的？
Q:
- STL中类似map，set的数据结构一共有几种？各自有什么特性？
- 它们是怎么实现的？

A:
来自TA的回答：可以看到set和map各4种
> The associative containers are:
1. set (+ unordered_set)
2. multiset (+ unordered_multiset)
3. map (+ unordered_map)
4. multimap (+ unordered_multimap)
> 
> The C++ Standard does not require any particular implementation. It only specifies the external methods and behaviors these collections must have (eg. they must support iterators, support insert in logarithmic time, etc.). This means various implementations may implement these collections differently under-the-hood. We will see a possible implementation of vector next Tuesday.

> The most common implementations of the ordered associative containers is using a **Red-Black tree**. CS 106B/X will briefly cover them (though you will not be tested on it). The idea is that they are binary trees which will self-balance when they become unbalanced. Another less common implementation is the AVL tree. My favorite implementation is using a skip list. 

> The unordered associative containers are implemented using a **hash table**. This will be covered in week 9 of CS 106B. I believe CS 106X has already covered them.

## set，map(ordered)
### 性质
- 插入，删除效率高：O(logN)
- 无重复元素
- Associate Collections
	- 包含set, multiset, map, multimap
	- Sequence Collections 指的是 vector，deque，list
	- 不能random access，没有idx。只能通过iterator遍历。

### 实现原理
- **基于红黑树**
- 元素以节点的方式存储（因此没有内存的移动）
	- 每次insert之后，以前保存的iterator不会失效(因为没有内存的移动)
- 因为基于红黑树，所以插入删除复杂度O(logN)

### 红黑树的一些基本性质
https://www.cnblogs.com/skywang12345/p/3245399.html
- 根节点是黑色
- 只有红色和黑色的节点
- 叶子节点是黑色
- 红色节点的子节点必须是黑色
- 黑色节点路径相同

红黑树的应用比较广泛，主要是用它来存储有序的数据，它的时间复杂度是O(lgn)，效率非常之高。
例如，Java集合中的TreeSet和TreeMap，C++ STL中的set、map，以及**Linux虚拟内存的管理**，都是通过红黑树去实现的。

**定理： 一棵含有n个节点的红黑树的高度至多为2log(n+1)**

**插入删除的过程**
- 将红黑树当作一颗二叉查找树，将节点插入；
- 然后，将节点着色为**红色**；
- 最后，通过旋转和重新着色等方法来修正该树，使之重新成为一颗红黑树

插入过程可能使得性质4被违背，通过**左旋**和**右旋**来维护这个红黑树。

## unordered_set, unordered_map

### 性质
- 插入，删除效率高：O(1)
- 无重复元素

### 实现原理
- 基于**hash table**
- 具体过程
	- 初始化
	- 超过load factor以后扩容
	- collision 用链表处理

> Python 中的set和map是 unordered，所以是用hash实现的
