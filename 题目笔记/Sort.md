# 排序
## 题目描述
O(nlogn) 排序算法：
- quick sort
- merge sort
- heap sort

## 题目分析
没啥分析的，背下来就好了

## 题目解答
**quick sort**
要点写在注释里面

```python
class Solution:
    # @param {int[]} A an integer array
    # @return nothing
    def sortIntegers2(self, A):
        # Write your code here
        self.quickSort(A, 0, len(A) - 1)
    
    def quickSort(self, A, start, end):
        if start >= end:
            return
        
        left, right = start, end

        # key point 1: pivot is the value, not the index
        pivot = A[(start + end) // 2];

        # key point 2: every time you compare left & right, it should be 
        # left <= right not left < right
		# bad case for left < right: [1,2]

        while left <= right:
            while left <= right and A[left] < pivot:
                left += 1
            
            while left <= right and A[right] > pivot:
                right -= 1
            
            if left <= right:
                A[left], A[right] = A[right], A[left]
                
                left += 1
                right -= 1
        
        self.quickSort(A, start, right)
        self.quickSort(A, left, end)
```

**merge sort 归并排序**
```python
class mergeSort(object):
    def __init__(self,nums):
        self.A = nums
        size = len(self.A)
        self.temp = [0 for _ in range(size)]
        self.sort(0,size-1)

        
    def sort(self,start,end):
        if start >= end:
            return 
        mid = start + (end-start)/2
        self.sort(start,mid)
        self.sort(mid+1,end)
        self.merge(start,end)
        
    def merge(self,start,end):
        mid = start + (end-start)/2
        l,r = start,mid+1
        index = start
        while l<=mid and r<=end:
            if self.A[l] < self.A[r]:
                self.temp[index] = self.A[l]
                index += 1
                l += 1
            else:
                self.temp[index] = self.A[r]
                index += 1
                r += 1
        while l<=mid:
            self.temp[index] = self.A[l]
            index += 1
            l += 1
        while r<=end:
            self.temp[index] = self.A[r]
            index += 1
            r += 1
        for i in range(start,end+1):
            self.A[i] = self.temp[i]
```

## 堆排序
- heapify: O(N)
- insert/remove: O(logN)
- heapsort: O(NlogN)

原位排序，无额外空间复杂度. 从小到大排序用**大根堆**
1. 创建一个堆 H[0……n-1]；
1. 把堆首（最大值）和堆尾互换；
1. 把堆的尺寸缩小 1，并调用 shift_down(0)，目的是把新的数组顶端数据调整到相应位置；
1. 重复步骤 2，直到堆的尺寸为 1。

```python
class Solution():
	def heapify(self, nums):
		for i in range(len(nums) // 2, -1, -1):
			self.siftdown(nums, i)

	def siftdown(self, nums, index):
		n = len(nums)
		while index < n:
			min_index = index	
			left = index * 2 + 1
			right = index * 2 + 2
			if left < n and nums[left] > nums[min_index]:
				min_index = left	
			if left < n and nums[right] > nums[min_index]:
				min_index = right
			
			if index == min_index:
				break
			nums[index], nums[min_index] = nums[min_index], nums[index]
			index = min_index

	def heap_sort(self, nums):
		self.heapify(nums):
		length = len(nums)
		for i in range(length-1):
			# 1. 收尾交换
			nums[0], nums[length-i] = nums[length-i], nums[0]
			# 2. siftdown,末尾的大数已经排好序不用管了
			self.siftdown(nums[-(length-i)], 1)
		
		return nums
```