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