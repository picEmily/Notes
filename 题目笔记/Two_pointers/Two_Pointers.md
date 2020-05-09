# 两指针
有两种用法，相同方向或者不同方向
- 快慢指针（相同方向，通过速度差解题）
	- 链表类
- left，right指针（两边同时向中间移动，中间同时向两边移动）

# 两数之和 two sum
## 题目描述
没有排序的数组
给一个数组和一个target，返回index满足两数之和为target

## 题目分析
两指针在这一题适合排序数组，但是那样就会打乱index，所以不适合这一题，还是用map

## 题目解答
```python
def twoSum(self, nums: List[int], target: int) -> List[int]:
	# hashmap 法
	m = {}
	size = len(nums)
	ret = []
	for i in range(size):
	    if target-nums[i] in m:
	        ret.append(m[target-nums[i]])
	        ret.append(i)
	        break
	    else:
	        m[nums[i]] = i
	return ret
```

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
			# 要么left，right都不指向零
			# 要么left指向0，right不指向零，那么此时swap会把0换到靠右的right指针处
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

# 排序数组 two sum
## 题目描述
给定一个已经 按升序排列 的数组，找到两个数使他们加起来的和等于特定数。
函数应该返回这两个数的下标，index1必须小于index2。注意返回的值不是 0-based。
Example
```
例1:
输入: nums = [2, 7, 11, 15], target = 9 
输出: [1, 2]
例2:
输入: nums = [2,3], target = 5
输出: [1, 2]
```
Notice
你可以假设每个输入刚好只有一个答案

## 题目分析
没啥难度
两根指针从头尾同时开始移动，O(N)

## 题目解答
```python
class Solution:
    """
    @param nums: an array of Integer
    @param target: target = nums[index1] + nums[index2]
    @return: [index1 + 1, index2 + 1] (index1 < index2)
    """
    def twoSum(self, nums, target):
        # two loops
		# 复杂度太高了，不好
        if not nums or len(nums) <= 1:
            return []

        
        size = len(nums)
        
        for p1 in range(size - 1):
            for p2 in range(p1+1, size):
                if nums[p1] + nums[p2] == target:
                    return [p1+1, p2+1]
                if nums[p1] + nums[p2] > target:
                    continue
        return []
        
        def twoSum(self, nums, target):
        # Jiuzhang solution
        l, r = 0, len(nums)-1
        while l < r:
            value = nums[l] + nums[r]
            if value == target:
                return [l+1, r+1]
            elif value < target:
                l += 1
            else:
                r -= 1
        return []
```


# [名字]
## 题目描述
给定一个有n个对象（包括k种不同的颜色，并按照1到k进行编号）的数组，将对象进行分类使相同颜色的对象相邻，并按照1,2，...k的顺序进行排序。
```
输入: 
[3,2,2,1,4] 
4
输出: 
[1,2,2,3,4]
```
## 题目分析
1 using counting sort 
2 无脑用快排序，或者merge sort

## 题目解答
```python
class Solution:
    """
    @param colors: A list of integer
    @param k: An integer
    @return: nothing
    """
    def sortColors2(self, colors, k):
        # 没记错的话应该叫桶排序(颜色排序，计数排序) O(N)算法
        m = {}
        for i in range(1,k+1):
            m[i] = 0
        
        for i in range(0, len(colors)):
            m[colors[i]] += 1
            
        idx = 0
        while idx < len(colors):
            for i in range(1, k+1):
                for j in range(idx, idx + m[i]):
                    colors[j] = i
                idx += m[i]
```
jiuzhang solution
counting用一个大小为k的数组来存，而不是用map
```python
class Solution:
    """
    @param colors: A list of integer
    @param k: An integer
    @return: nothing
    """
    def sortColors2(self, colors, k):
        # self.countingSort(colors, k) #çº¿æ§æ¶é´å¤æåº¦ï¼çè®ºä¸å¿«ä¸ç¹ï¼ä½æ¯èè´¹ç©ºé´
        self.sort(colors, 1, k, 0, len(colors) - 1)
    
    def counttingSort(self, colors, k):    
        # counting sort 
        temp = list(colors)
        size = len(colors)
        bucket = [0] * k
        
        # 1 ç»è®¡æ¯ä¸ªæ°å­çä¸ªæ°
        for i in range(size):
            bucketIndex = temp[i] - 1
            bucket[bucketIndex] += 1
        
        # 2 ç»è®¡æ¯ä¸ªæ°å­åºè¯¥æå¨ä½ç½®
        sum = 0
        for i in range(k):
            
            bucket[i] = sum + bucket[i]
            sum = bucket[i]
        print(bucket)
        
        # 3 éåcolors å¡«è¿ç»æ
        for i in range(size):
            num = temp[i]
            pos = bucket[num-1] - 1
            bucket[num-1] -= 1
            colors[pos] = num
            
        # merge or quick sort 
    def sort(self, colors, color_from, color_to, index_from, index_to):
        # color from 1 ~ k index from 0 ~ len(color)-1
        # ç­æ¡åquickSortå¾åå
        
        if color_from >= color_to or index_from >= index_to:
            return 
        
        color = (color_from + color_to) // 2
        left, right = index_from, index_to
        while left <= right:
            while left <= right and colors[left] <= color:
                left += 1
            while left <= right and colors[right] > color: # why > ?????????????
                right -= 1
            if left <= right: 
                colors[left], colors[right] = colors[right], colors[left]
                left += 1 
                right -= 1
        
        self.sort(colors, color_from, color, index_from, right)
        self.sort(colors, color+1, color_to, left, index_to) # why color+1 ????????
```
# 3sum
## 题目描述
给出一个有n个整数的数组S，在S中找到三个整数a, b, c，找到所有使得a + b + c = 0的三元组。

条件：最最一般的情况
- 假设数组可能有重复数字
- 没有结果则返回[]
- 返回所有可能结果

## 题目分析
3 sum 背下来就好
第一个数字遍历
第二三个数字用two sum的方法来做

## 题目解答
```python
class Solution:
    """
    @param numbers: Give an array numbers of n integer
    @return: Find all unique triplets in the array which gives the sum of zero.
    """
    def threeSum(self, nums):
        nums.sort()
        results = []
        length = len(nums)
        for i in range(0, length - 2):
            if i and nums[i] == nums[i - 1]:
                # omit duplicate numbers
                continue
            self.find_two_sum(nums, i + 1, length - 1, -nums[i], results)
        return results
        
    def find_two_sum(self, nums, left, right, target, results):
        while left < right:
            if nums[left] + nums[right] == target:
                results.append([-target, nums[left], nums[right]])
                right -= 1
                left += 1
                while left < right and nums[left] == nums[left - 1]:
                    # omit duplicate numbers
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif nums[left] + nums[right] > target:
                right -= 1
            else:
                left += 1
```

# Partition Array 数组划分
## 题目描述
给出一个整数数组 nums 和一个整数 k。划分数组（即移动数组 nums 中的元素），使得：

所有小于k的元素移到左边
所有大于等于k的元素移到右边
返回数组划分的位置，即数组中第一个位置 i，满足 nums[i] 大于等于 k。

## 题目分析
这就是快排的基本型
背下来就好
单纯的一次partition是O(N)时间复杂度和O(1)空间复杂度的
``return start`` 得到pivot的位置

## 题目解答
```python
class Solution:
    """
    @param nums: The integer array you should partition
    @param k: As description
    @return: The index after partition
    """
    def partitionArray(self, nums, k):
        start, end = 0, len(nums) - 1
        while start <= end:
            while start <= end and nums[start] < k:
                start += 1
            while start <= end and nums[end] >= k:
                end -= 1
            if start <= end:
                nums[start], nums[end] = nums[end], nums[start]
                start += 1
                end -= 1
        return start
```

# 第K大元素
## 题目描述
给一个数组
要求时间复杂度为O(n)，空间复杂度为O(1)

## 题目分析
数组是未排序的，也就是说只能遍历一次，而且又不能专门拿个东西存

又是partition的应用了，就是经过多次partition后让pivot成为第len(A) - k个数字（第k大）

topK问题用堆来实现

## 题目解答
```python
class Solution:
    # @param k & A a integer and an array
    # @return ans a integer
    def kthLargestElement(self, k, A):
        if not A or k < 1 or k > len(A):
            return None
        # len(A) - k 表示第len(A) - k 小的数字
        return self.partition(A, 0, len(A) - 1, len(A) - k)
        
    def partition(self, nums, start, end, k):
        """
        During the process, it's guaranteed start <= k <= end
        """
        # 每进行完一次partition，都能得到由pivot分开的两组数
        # start == end是pivot是第k个数的条件
        if start == end:
            return nums[k]
            
        left, right = start, end
        pivot = nums[(start + end) // 2]
        while left <= right:
            while left <= right and nums[left] < pivot:
                left += 1
            while left <= right and nums[right] > pivot:
                right -= 1
            if left <= right:
                nums[left], nums[right] = nums[right], nums[left]
                left, right = left + 1, right - 1
                
        # left is not bigger than right
        if k <= right:
            return self.partition(nums, start, right, k)
        if k >= left:
            return self.partition(nums, left, end, k)
        
        return nums[k]
```