# Heap相关知识
## CRUD时间复杂度

# TopK/BtmK
## 题目描述
612 544 
在一个数组中找到前K大数/在一个数组中找出前K小数

## 题目分析
这一题是一个 PriorityQueue的题
补充一下python中PriorityQueue怎么实现
https://docs.python.org/3.0/library/heapq.html

Python 中内置的 ``heapq`` 库和 ``queue.priorityqueue`` 分别提供了堆和优先队列结构，其中优先队列 queue.PriorityQueue 是基于 heapq 实现的，因此重点看heapq
- heapq提供的api能直接再Python List上使用
- heapq只提供的是小堆
- heapq想要实现大堆，每个元素取负 http://stackoverflow.com/questions/14189540/python-topn-max-heap-use-heapq-or-self-implement

```python
heapq.heappush(heap, item) #Push the value item onto the heap, maintaining the heap invariant.

heapq.heappop(heap) #Pop and return the smallest item from the heap, maintaining the heap invariant. If the heap is empty, IndexError is raised. To access the smallest item without popping it, use heap[0].

heapq.heappushpop(heap, item) #先把item加入到堆中，然后再pop，比heappush()再heappop()要快得多

heapq.heapreplace(heap, item) #先pop，然后再把item加入到堆中，比heappop()再heappush()要快得多

heapq.heapify(x) #将列表x进行堆调整，默认的是小顶堆

heapq.merge(*iterables) #将多个列表合并，并进行堆调整，返回的是合并后的列表的迭代器

heapq.nlargest(n, iterable, key=None) #返回最大的n个元素（Top-K问题）

heapq.nsmallest(n, iterable, key=None) #返回最小的n个元素（Top-K问题）
```

```python
# use heapq to implement priorityqueue
```

## 题目解答
### TOPK
```python
import heapq
class Solution:
    """
    @param nums: an integer array
    @param k: An integer
    @return: the top k largest numbers in array
    """
    def topk(self, nums, k):
        heap = []
        result = []
        
        for n in nums:
            if len(heap) < k:
                heapq.heappush(heap, n)
            else:
                if n <= heap[0]:
                    pass
                else:
                    heapq.heapreplace(heap, n)
        
        while k > 0:
            result.append(heapq.heappop(heap))
            k -= 1
        result.reverse()
        return result
```

### BTMK
这个解答似乎有些许问题
- 使用小堆做BtmK，会构建一个无比庞大的heapq
- 正确的做法是BtmK用大堆，TopK用小堆

```python
"""
Definition for a point.
class Point:
    def __init__(self, a=0, b=0):
        self.x = a
        self.y = b
"""

import heapq

class Solution:
    """
    @param points: a list of points
    @param origin: a point
    @param k: An integer
    @return: the k closest points
    """
    def kClosest(self, points, origin, k):
        # this is the application of PriorityQueue!
        
        # PriorityQueue is based on heap
        self.heap = []
        for point in points:
            dist = self.getDistance(point, origin)
            # build smallheap
            heapq.heappush(self.heap, (dist, point.x, point.y))

        ret = []
        while k > 0:
            _, x, y = heapq.heappop(self.heap)
            ret.append(Point(x, y))
            k -= 1

        return ret

    def getDistance(self, a, b):
        return (a.x - b.x) ** 2 + (a.y - b.y) ** 2
```

```python
# 正确做法
"""
Definition for a point.
class Point:
    def __init__(self, a=0, b=0):
        self.x = a
        self.y = b
"""

import heapq

class Solution:
    """
    @param points: a list of points
    @param origin: a point
    @param k: An integer
    @return: the k closest points
    """
    def kClosest(self, points, origin, k):
        # this is the application of PriorityQueue!
        
        # PriorityQueue is based on heap
        self.heap = []
        for point in points:
            dist = self.getDistance(point, origin)
            # build bigheap(we use negative values, thus bigheap)
            # sort by dist, then x, then y
            if len(self.heap) < k:
                heapq.heappush(self.heap, (-dist, -point.x, -point.y))
            else:
                if (-dist, -point.x, -point.y) > self.heap[0]:
                    heapq.heapreplace(self.heap, (-dist, -point.x, -point.y))
            # print(self.heap)
                
        result = []
        while k > 0:
            _, x, y = heapq.heappop(self.heap)
            result.append(Point(-x, -y))
            k -= 1
        result.reverse()

        return result

    def getDistance(self, a, b):
        return (a.x - b.x) ** 2 + (a.y - b.y) ** 2
```

# 合并k个排序链表
## 题目描述
104 合并k个排序链表，并且返回合并后的排序链表。尝试分析和描述其复杂度。
```
样例 1:
	输入:   [2->4->null,null,-1->null]
	输出:  -1->2->4->null

样例 2:
	输入: [2->6->null,5->null,7->null]
	输出:  2->5->6->7->null
```

## 题目分析
- 基本思路：归并排序(但是每次只能merge两条)
- 利用heap

## 题目解答
### heap 做法

本质上相当于heap sort

```python

"""
Definition of ListNode
class ListNode(object):

    def __init__(self, val, next=None):
        self.val = val
        self.next = next
"""

import heapq


# overwrite the compare function 
# so that we can directly put ListNode into heapq

# 这个是python的动态特性吧
ListNode.__lt__ = lambda x, y: (x.val < y.val)


class Solution:
    """
    @param lists: a list of ListNode
    @return: The head of one sorted list.
    """
    def mergeKLists(self, lists):
        if not lists:
            return None
        
        dummy = ListNode(0)
        tail = dummy
        heap = []
        for head in lists:
            if head:
                heapq.heappush(heap, head)
                
        while heap:
            head = heapq.heappop(heap)
            tail.next = head
            tail = head
            if head.next:
                heapq.heappush(heap, head.next)
                    
        return dummy.next
```

### 普通merge做法
- 一次只能merge两个
- 用递归来merge多个（内部实现是两两merge）
- dummy的用法是：就相当于head，但是这里面没有指针，所以它是个node，但是我们要的结果其实是``dummy.next``

```python
"""
Definition of ListNode
class ListNode(object):

    def __init__(self, val, next=None):
        self.val = val
        self.next = next
"""
class Solution:
    """
    @param lists: a list of ListNode
    @return: The head of one sorted list.
    """
    def mergeKLists(self, lists):
        return self.merge_range(lists, 0, len(lists) - 1)
        
    def merge_two(self, l1, l2):
        # core of merge lists
        
		# we won't use dummy directly
        # dummy.next is the head of result we want to return
        tail = dummy = ListNode(0)
        while l1 and l2:
            if l1.val < l2.val:
                tail.next = ListNode(l1.val)
                tail = tail.next
                l1 = l1.next
            else:
                tail.next = ListNode(l2.val)
                tail = tail.next
                l2 = l2.next
            
        if l1:
            tail.next = l1
        if l2:
            tail.next = l2
        
        return dummy.next
        
    def merge_range(self, lists, start, end):
        if start == end:
            # base case for the recursion
            return lists[start]
        
        mid = start + (end - start) // 2
        left = self.merge_range(lists, start, mid)
        right = self.merge_range(lists, mid+1, end)
        
        return self.merge_two(left, right)
```

# 丑数

## 题目描述
设计一个算法，找出只含素因子2，3，5 的第 n 小的数。（还包括1这个特殊情况）

符合条件的数如：1, 2, 3, 4, 5, 6, 8, 9, 10, 12...

要求时间复杂度为 O(nlogn) 或者 O(n)。

## 题目分析
第n小，利用heap，建立一个heap并pop n次就是所需结果  O(nlogn)

## 题目解答

```python
import heapq
class Solution:
    """
    @param n: An integer
    @return: return a  integer as description.
    """
    def nthUglyNumber(self, n):
        # 还是利用heap这种数据结构的特性，顶端是最小(大)数
        heap = [1]
        visited = set([1])
        
        for i in range(n):
            # pop 第n次，也就是第n小的数
            smallest = heapq.heappop(heap)
            for factor in [2,3,5]:
                if factor * smallest not in visited:
                    heapq.heappush(heap, factor * smallest)
                    visited.add(factor * smallest)
        return smallest
```