# Permutation 全排列
## 题目描述
15
给定一个数字列表，返回其所有可能的排列。

## 题目分析
求出所有路径问题
看成图的话，某个节点的neighbor是unvisited所有元素

背下来就好啦~
官方答案的话不是用的set，而是维护了一个visited数组，每一位代表一个数

## 题目解答
```python
class Solution:
    """
    @param: nums: A list of integers.
    @return: A list of permutations.
    """
    def permute(self, nums):
        result = []
        unvisited = set([n for n in nums])
        # for n in nums:
        #     unvisited.add(n)
        self.dfs(nums, result, [], unvisited)
        return result
        
    def dfs(self, nums, result, path, unvisited):
        if len(path) == len(nums):
            result.append(list(path))
            return
    
        for ele in unvisited:
            path.append(ele)
            unvisited.remove(ele)
            self.dfs(nums, result, path, unvisited)
            path.pop()
            unvisited.add(ele)
```

# 分割字符串Split String
## 题目描述
608
给一个字符串,你可以选择在一个字符或两个相邻字符之后拆分字符串,使字符串由仅一个字符或两个字符组成,输出所有可能的结果

```
输入： "12345"
输出： [["1","23","45"],["12","3","45"],
["12","34","5"],["1","2","3","45"],
["1","2","34","5"],["1","23","4","5"],
["12","3","4","5"],["1","2","3","4","5"]]
```

## 题目分析
标准的dfs全排列问题，全排列就要用到backtrace
和官方答案有一点点修改是：官方答案会修改原字符串s，我用一个start来记录坐标，避免修改原字符串

几个要素：
- 全排列，所以有``result: List[List[str]]``， ``path: List[str]``, result 储存了 path
- 找到出口，对应这一题就是字符串已经遍历完了
- backtrace的步骤：append, dfs, pop

## 题目解答
```python
class Solution:
    """
    @param: : a string to be split
    @return: all possible split string array
    """

    def splitString(self, s):
        result = []
        self.dfs(s, 0, result, [])
        return result
    
    def dfs(self, s, start, result, path):
        if start >= len(s):
            # 退出的条件
            result.append(list(path))
            return
            
        for i in range(1,3):
            # standart backtrack
            if start+i <= len(s):
                path.append(str(s[start:start+i]))
                self.dfs(s, start+i, result, path)
                path.pop()
```


# 电话号码的字母组合  · Letter Combinations of a Phone Number
## 题目描述
给一个不包含'0'和'1'的数字字符串，每个数字代表一个字母，请返回其所有可能的字母组合。

下图的手机按键图，就表示了每个数字可以代表的字母。
```
KEYBOARD = {
    '2': 'abc',
    '3': 'def',
    '4': 'ghi',
    '5': 'jkl',
    '6': 'mno',
    '7': 'pqrs',
    '8': 'tuv',
    '9': 'wxyz',
}
```

## 题目分析
其实还是通过backtrace把所有可能的情况都遍历一遍

## 题目解答
```
class Solution:
    """
    @param digits: A digital string
    @return: all posible letter combinations
    """
    

    
    def letterCombinations(self, digits):
        if len(digits) == 0:
            return []
        self.KEYBOARD = {
            '2': 'abc',
            '3': 'def',
            '4': 'ghi',
            '5': 'jkl',
            '6': 'mno',
            '7': 'pqrs',
            '8': 'tuv',
            '9': 'wxyz',
        }
        result = []
        self.dfs(digits, result, '', 0)
        return result
    
    def dfs(self, digits, result, path, start):
        # 还是标准的全排列：利用backtrace
        if start >= len(digits):
            # exit
            result.append(path)
            return
        
        for ch in self.KEYBOARD[digits[start]]:

            path += ch
            self.dfs(digits, result, path, start+1)
            path = path[:-1]
        
        
```


# 数字组合2
## 题目描述
153
给定一个数组 num 和一个整数 target. 找到 num 中所有的数字之和为 target 的组合.

假设：
- 在同一个组合中, num 中的每一个数字仅能被使用一次.
- 所有数值 (包括 target ) 都是正整数.
- 返回的每一个组合内的数字必须是非降序的.
- 返回的所有组合之间可以是任意顺序.
- 解集不能包含重复的组合.

## 题目分析
有顺序要求，所以一开始先sort
其他的就是很标准的全排列问题，和前两题类似

## 题目解答
```python
class Solution:
    """
    @param num: Given the candidate numbers
    @param target: Given the target number
    @return: All the combinations that sum to target
    """
    def combinationSum2(self, num, target):
        num.sort()
        result = []
        self.dfs(num, target, result, [], 0, 0)
        return result
    
    def dfs(self, num, target, result, path, path_sum, start):
        
        if path_sum == target:
            # 正确的添加path的条件
            result.append(list(path))
            return
        
        if start >= len(num) or path_sum > target:
            # start超过了数组长度或者和已经过大，则退出
            return 
        
        for i in range(start, len(num)):
            if i > start and num[i] == num[i-1]:
                # 去重条件，我想了好一会儿
                # i>start 表示i==start时候不去检查是否和上一个一样
                # 不然类似 [1,1,2]的结果都会被排除掉
                continue
            path.append(num[i])
            path_sum += num[i]
            self.dfs(num, target, result, path, path_sum, i + 1)
            path.pop()
            path_sum -= num[i]
     
```


# 数字组合1
## 题目描述
## 题目分析
和数字组合2几乎一摸一样，唯一区别在于可以重复使用里面的数字

改动的地方只有``self.dfs()`` i+1 变成了 i
## 题目解答
```python
class Solution:
    """
    @param num: Given the candidate numbers
    @param target: Given the target number
    @return: All the combinations that sum to target
    """
    def combinationSum(self, candidates, target):
        candidates.sort()
        result = []
        self.dfs(candidates, target, result, [], 0, 0)
        return result
    
    def dfs(self, candidates, target, result, path, path_sum, start):
        
        if path_sum == target:
            # 正确的添加path的条件
            result.append(list(path))
            return
        
        if start >= len(candidates) or path_sum > target:
            # start超过了数组长度或者和已经过大，则退出
            return 
        
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i-1]:
                continue
            path.append(candidates[i])
            path_sum += candidates[i]
            # 唯一改动的行
            self.dfs(candidates, target, result, path, path_sum, i)
            path.pop()
            path_sum -= candidates[i]
     
```

# N Queen
## 题目描述
33
n皇后问题是将n个皇后放置在n*n的棋盘上，皇后彼此之间不能相互攻击(任意两个皇后不能位于同一行，同一列，同一斜线)。

给定一个整数n，返回所有不同的n皇后问题的解决方案。

每个解决方案包含一个明确的n皇后放置布局，其中“Q”和“.”分别表示一个女王和一个空位置。

```
输入:4
输出:
[
  // Solution 1
  [".Q..",
   "...Q",
   "Q...",
   "..Q."
  ],
  // Solution 2
  ["..Q.",
   "Q...",
   "...Q",
   ".Q.."
  ]
]
```

## 题目分析
太经典了
没啥解释的，DFS就完了

一点小困难是 ``is_valid()``稍微复杂

> python 中字符串替换某个字符
> python 字符串是 **不可变类型**，所以一下操作不可行
```python
# 不可行的操作
s = 'foo'
s[0] = 'b'
```
> 替换某个字符的方法：转换成列表
```python
s = 'foo'
s_list = list(s)
s_list[0] = 'b'
s = ''.join(s_list)
```

## 题目解答
```python
class Solution:
    """
    @param: n: The number of queens
    @return: All distinct solutions
    """
    def solveNQueens(self, n):
        result = []
        self.dfs(n, result, [])
        return result
        
    
    def dfs(self, n, result, path):
        """
        params:
            path: List[int] [1,3,0,2] shows the position of Q in each line
        """
        if len(path) == n:
            # exit
            path = self.serialize(path, n)
            result.append(list(path))
            return
        
        for i in range(n):
            if self.is_valid(path, i):
                # backtrace
                path.append(i)
                self.dfs(n, result, path)
                path.pop()
        
    def is_valid(self, path, new):
        # 一定能保证不出现在同一行，只需要看是否出现在同一列和斜线上
        idx = len(path)
        for i in range(idx):
            if new == path[i]:
                # 不出现在同一列
                return False
            if new == path[i] + (idx-i) or new == path[i] - (idx-i):
                # 不出现在斜线上
                return False
        return True
    
    def serialize(self, a, n):
        length = len(a)
        result = []
        for i in range(length):
            idx = a[i]
            s = list('.'*n)
            s[idx] = 'Q'
            s = ''.join(s)
            result.append(s)    
        return result
```

# 子集2
## 题目描述
给定一个可能具有重复数字的列表，返回其所有可能的子集。

## 题目分析
一看就是全排列
重点还是在于
- 怎么样组织这个全排列，是否用循环/用一个怎样的循环
- 去重的条件

本题中for loop表示的情况就是我们不把i以前的数字添加到path中了

## 题目解答
```python
class Solution:
    """
    @param nums: A set of numbers.
    @return: A list of lists. All valid subsets.
    """
    def subsetsWithDup(self, nums):
        # 还是全排列回溯，每个字符有出现和不出现两种情况
        nums.sort()
        result = []
        self.dfs(nums, result, [], 0)
        return result
        
    def dfs(self, nums, result, path, start):
        result.append(list(path))
        
        for i in range(start, len(nums)):
            
            if i > start and nums[i] == nums[i - 1]:
                # remove duplicate
                continue
            
            path.append(nums[i])
            self.dfs(nums, result, path, i+1)
            path.pop()

```
假如不怕重复的话可以这样写，体会一下区别
```python
class Solution:
    """
    @param nums: A set of numbers.
    @return: A list of lists. All valid subsets.
    """
    def subsetsWithDup(self, nums):
        result = []
        self.dfs(nums, result, [], 0)
        return result
        
    def dfs(self, nums, result, path, start):
        if start >= len(nums):
            result.append(list(path))
            return
        
        # if add this number
        path.append(nums[start])
        self.dfs(nums, result, path, start+1)
        path.pop()
        # if not add this number
        self.dfs(nums, result, path, start+1)
```

# dfs遍历树: 路径总和
## 题目描述
1357
给定一个二叉树和一个目标和，找到所有从根节点到叶子节点路径总和等于给定目标和的路径。
```
输入: root = {5,4,8,11,#,13,4,7,2,#,#,5,1}, sum = 22
              5
             / \
            4   8
           /   / \
          11  13  4
         /  \    / \
        7    2  5   1
输出: [[5,4,11,2],[5,8,4,5]]
```

## 题目分析
就，找所有路径问题，但是终点是所有叶子节点而不是某个节点

## 题目解答
```python
"""
Definition of TreeNode:
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None
"""

class Solution:
    """
    @param root: a binary tree
    @param sum: the sum
    @return: the scheme
    """
    def pathSum(self, root, sum):
        # 1. 树只用考虑两个邻居，left and right
        # 2. 树不需要考虑visited，因为是单向的图
        result = []
        ret = []
        self.dfs(sum, [root], result)
        for r in result:
            r = [ele.val for ele in r]
            ret.append(list(r))
        return ret
            
    def dfs(self, sum, path, result):
        if path[-1].left is None and path[-1].right is None:
            # 已经遍历到子叶节点，检查和
            if self.get_sum(path) == sum:
                # print([ele.val for ele in path])
                result.append(list(path))
                return 
        
        # neighbor is left and right node
        if path[-1].left:
            path.append(path[-1].left)    
            self.dfs(sum, path, result)
            path.pop()
        if path[-1].right:
            path.append(path[-1].right)
            self.dfs(sum, path, result)
            path.pop()
        
            
    def get_sum(self, nums):
        ret = 0
        for n in nums:
            ret += n.val
        return ret
```


# 单词搜索
## 题目描述
123
给出一个二维的字母板和一个单词，寻找字母板网格中是否存在这个单词。
单词可以由按顺序的相邻单元的字母组成，其中相邻单元指的是水平或者垂直方向相邻。每个单元中的字母最多只能使用一次。

```
输入：["ABCE","SFCS","ADEE"]，"ABCCED"
输出：true
解释：
[    
     A B C E
     S F C S 
     A D E E
]
(0,0)A->(0,1)B->(0,2)C->(1,2)C->(2,2)E->(2,1)D
```

## 题目分析
只用找到一个合法答案的dfs题
属于最容易理解的从图中找到一条路径的类别

return值的理解：
我个人写dfs不喜欢return，但是不return更适合做全搜索
这一题只需要回答True或者False，所以return True或者False，避免找到答案了以后还继续搜索

## 题目解答
```python
class Solution:
    """
    @param board: A list of lists of character
    @param word: A string
    @return: A boolean
    """
    direction = set([(0,-1),(0,1),(1,0),(-1,0)])
    def exist(self, board, word):
        # Boundary Condition
        if word == []:
            return True
        m = len(board)
        if m == 0:
            return False
        n = len(board[0])
        if n == 0:
            return False
            
        # Visited Matrix all false
        visited = [[False for j in range(n)] for i in range(m)]
        
        for i in range(m):
            for j in range(n):
                if self.helper(board, word, visited, i, j):
                    return True
        return False
    
    def helper(self, board, word, visited, row, col):
        if word == '':
            return True
        m, n = len(board), len(board[0])
        if row < 0 or row >= m or col < 0 or col >= n:
            return False
        if board[row][col] == word[0] and not visited[row][col]:
            visited[row][col] = True
            for dir in self.direction:
                if self.helper(board, word[1:], visited, row+dir[0], col+dir[1]):
                    return True
            visited[row][col] = False
        
        return False
```


