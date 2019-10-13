# 两指针
有两种用法，相同方向或者不同方向
- 快慢指针（相同方向，通过速度差解题）
	- 链表类
- left，right指针（两边同时向中间移动，中间同时向两边移动）

# 链表的中点
## 题目描述
228.找链表的中点

## 题目分析
快慢指针经典：
链表的题目
没啥难度，做一遍就会了

## 题目解答
```python
class Solution:
    """
    @param head: the head of linked list.
    @return: a middle node of the linked list
    """
    def middleNode(self, head):
        if not head:
            return None
        
        slow = head
        fast = head.next
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        return slow
```


# 两数之和 III-数据结构设计
## 题目描述
607.设计b并实现一个 TwoSum 类。他需要支持以下操作:add 和 find。
add -把这个数添加到内部的数据结构。
find -是否存在任意一对数字之和等于这个值

## 题目分析
这里利用hashmap add的速度都是O(1)，查询O(N)
维护一个hashmap（python里面就是dict），查询的时候遍历一遍

## 题目解答
```python
class TwoSum:
    """
    @param number: An integer
    @return: nothing
    """
    """
    重点在于设计这个结构
    add，find可以达到平均最小的复杂度
    利用hashmap的快速查询
    """
    def __init__(self):
        # map<number, 这个number被添加的次数>
        self.count = {}
    
    def add(self, number):
        if number in self.count.keys():
            self.count[number] += 1
        else:
            self.count[number] = 1
        
    """
    @param value: An integer
    @return: Find if there exists any pair of numbers which sum is equal to the value.
    """
    def find(self, value):
        for num in self.count.keys():
            v = value - num
            if v in self.count.keys() and \
                (v != num or self.count[v] > 1):
                    return True
        return False
```

# 移动零

## 题目描述
539.给一个数组 nums 写一个函数将 0 移动到数组的最后面，非零元素保持原数组的顺序

## 题目分析
两根指针经典
应用场景是俄罗斯方块里面，把可以消除的行往上平移并消除，其他行按照原顺序向下平移

- a指针指向0，从a开始往后找第一个b指针指向非0，二者指向的数字交换。（这样做的目的是把0一步一步往后面换）
- a继续往后找下一个0，b从新的a开始往后找第一个非0，然后交换（循环往复）
- 当b指向的是最后一个数的时候就完成了
- 特殊情况是全是0，或全非0

## 题目解答
```python
class Solution:
    """
    @param nums: an integer array
    @return: nothing
    """
    def moveZeroes(self, nums):
        self.size = len(nums)
        
        pointer_move = 0
        pointer_not_move = 0
        
        pointer_move = self.find_nxt_0(nums, pointer_move)
        pointer_not_move = self.find_nxt_1(nums, pointer_move)  # pointer_not_move要从pointer_move往后面找
        
        while True:
            nums[pointer_move], nums[pointer_not_move] = nums[pointer_not_move], nums[pointer_move]
            
            # 说明完成的条件
            if pointer_move == self.size - 1 or pointer_not_move == self.size - 1:
                break
            
            pointer_move = self.find_nxt_0(nums, pointer_move)
            pointer_not_move = self.find_nxt_1(nums, pointer_move)
    
    def find_nxt_0(self, nums, pointer):
        if pointer >= self.size - 1:
            return pointer
        
        for i in range(pointer, self.size):
            pointer = i
            if nums[i] == 0:
                break
        
        return pointer
        
    def find_nxt_1(self, nums, pointer):
        if pointer >= self.size - 1:
            return pointer
        
        for i in range(pointer, self.size):
            pointer = i
            if nums[i] != 0:
                break
            
        return pointer
```

答案提供的方法
思路是一样的，但是写的简洁许多
```python
class Solution:
    """
    @param nums: an integer array
    @return: nothing
    """
    def moveZeroes(self, nums):
        left, right = 0, 0
        while right < len(nums):
            if nums[right] != 0:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1
            right += 1

```

# 去除重复元素
## 题目描述
521.
给一个整数数组，去除重复的元素。

你应该做这些事

1. 在原数组上操作
2. 将去除重复之后的元素放在数组的开头
3. 返回去除重复元素之后的元素个数

```
输入:
nums = [1,3,1,4,4,2]
输出:
[1,3,4,2,?,?]
4

解释:
1. 将重复的整数移动到 nums 的尾部 => nums = [1,3,4,2,?,?].
2. 返回 nums 中唯一整数的数量  => 4.
事实上我们并不关心你把什么放在了 ? 处, 只关心没有重复整数的部分.
```

**挑战**
1. O(n)时间复杂度.
2. O(nlogn)时间复杂度但没有额外空间

## 题目分析
挑战提示了我们如果要O(N）的话是需要额外空间的
而且要在原数组上操作，所以立马想到了类似*消除零*那一题的两根指针，一步一步地将重复的数字往后移动。维护一个set记录出现过的数字（时间O(N) + 空间O(N)）

答案的O(nlogn)做法，先sort了...（目的是把重复的元素一定会连在一起，这样省去了维护一个set的空间复杂度），然后遍历一遍。我觉得不好，因为会改变顺序

## 题目解答
```python
class Solution:
    """
    @param nums: an array of integers
    @return: the number of unique integers
    """
    def deduplication(self, nums):
        visited = set()
        left, right = 0, 0

        while right < len(nums):
            if nums[right] not in visited:
                visited.add(nums[right])
                nums[left], nums[right] = nums[right], nums[left]
                left += 1
            right += 1
        
        return left
```

```python
# O(nlogn) time, O(1) extra space
class Solution:
    # @param {int[]} nums an array of integers
    # @return {int} the number of unique integers
    def deduplication(self, nums):
        # Write your code here
        n = len(nums)
        if n == 0:
            return 0
            
        nums.sort()
        result = 1
        for i in range(1, n):
            if nums[i - 1] != nums[i]:
                nums[result] = nums[i]
                result += 1
                
        return result
```

# [名字]
## 题目描述
## 题目分析
## 题目解答

# [名字]
## 题目描述
## 题目分析
## 题目解答

# [名字]
## 题目描述
## 题目分析
## 题目解答

# [名字]
## 题目描述
## 题目分析
## 题目解答

# [名字]
## 题目描述
## 题目分析
## 题目解答