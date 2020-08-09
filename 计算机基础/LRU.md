# LRU
**Least Recently Used**:  
一种内存管理策略，对加入到内存中的文件进行选择。LRU是保留常使用的数据，淘汰不常使用的数据。原因是经常被访问的数据有更大的几率以后也经常被访问。
其他策包括**FIFO**，**LFU**

**基本实现思路是**
- 每次被访问的数据被放到栈顶
- 当栈满了以后，淘汰栈底元素

# 设计
## 问题描述
为最近最少使用（LRU）缓存策略设计一个数据结构，它应该支持以下操作：获取数据和写入数据。

``get(key)`` 获取数据：如果缓存中存在key，则获取其数据值（通常是正数），否则返回-1。
``set(key, value)`` 写入数据：如果key还没有在缓存中，则写入其数据值。当缓存达到上限，它应该在写入新数据之前删除最近最少使用的数据用来腾出空闲位置。

## 解题思路
由于有大量插入删除操作，linkedlist的复杂度最低（如果在头尾的话复杂度为1）
但是其查找操作的复杂度是O(N)

```python
class LinkedNode:
    
    def __init__(self, key=None, value=None, next=None):
        self.key = key
        self.value = value
        self.next = next

class LRUCache:

    # @param capacity, an integer
    def __init__(self, capacity):
        # 存所有keys (key, node), 存上一个node的key是为了避免double linkedlist
        self.key_to_prev = {}
        # 尾部表示最近使用
        # 此为标准建表流程
        self.dummy = LinkedNode()
        self.tail = self.dummy
        self.capacity = capacity
    
    def push_back(self, node):
        # 往尾部添加新的节点
        self.key_to_prev[node.key] = self.tail
        self.tail.next = node
        self.tail = node
    
    def pop_front(self):
        # 删除头部
        head = self.dummy.next
        del self.key_to_prev[head.key]
        self.dummy.next = head.next
        self.key_to_prev[head.next.key] = self.dummy
        
    # change "prev->node->next...->tail"
    # to "prev->next->...->tail->node"
    def kick(self, prev):    
        # 将数据移动至尾部，尾部表示最近使用
        node = prev.next
        if node == self.tail:
            return
        prev.next = node.next
        if node.next is not None:
            self.key_to_prev[node.next.key] = prev
            node.next = None
        self.push_back(node)

    # @return an integer
    def get(self, key):		#获取数据
        if key not in self.key_to_prev:
            return -1
        self.kick(self.key_to_prev[key])
        return self.key_to_prev[key].next.value

    # @param key, an integer
    # @param value, an integer
    # @return nothing
    def set(self, key, value):     #数据放入缓存
        if key in self.key_to_prev:	   
            self.kick(self.key_to_prev[key])
            self.key_to_prev[key].next.value = value
        else:
            self.push_back(LinkedNode(key, value))  
            #如果key不存在，则存入新节点
            if len(self.key_to_prev) > self.capacity:
                #如果缓存超出上限，删除头部
                self.pop_front()		
```