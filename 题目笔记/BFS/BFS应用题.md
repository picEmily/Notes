# 骑士的最短路线
## 题目描述
611 骑士的最短路线
给定骑士在棋盘上的 初始 位置(一个2进制矩阵 0 表示空 1 表示有障碍物)，找到到达 终点 的最短路线，返回路线的长度。如果骑士不能到达则返回 -1 。

输入:
[[0,0,0],
 [0,0,0],
 [0,0,0]]
source = [2, 0] destination = [2, 2] 
输出: 2
解释:
[2,0]->[0,1]->[2,2]

## 题目分析
都要求最短路线了必定是bfs应用啊
此题只用求最短是多少，模仿level traversal，记录一下遍历了几层就好

另外其他的应用类似Linkedin的几度人际关系

## 题目解答
```python
"""
Definition for a point.
class Point:
    def __init__(self, a=0, b=0):
        self.x = a
        self.y = b
"""

class Solution:
    """
    @param grid: a chessboard included 0 (false) and 1 (true)
    @param source: a point
    @param destination: a point
    @return: the shortest path 
    """
    def shortestPath(self, grid, source, destination):
        queue = collections.deque()
        queue.append((source.x, source.y))
        
        cnt = -1
        while queue:
            cnt += 1
            l = len(queue)
            for _ in range(l):
                node = queue.popleft()
                if node[0] == destination.x and node[1] == destination.y:
                    return cnt
                
                for dir in ((1,2),(-1,2),(1,-2),(-1,-2),(2,1),(2,-1),(-2,-1),(-2,1)):
                    candidate = (node[0]+dir[0], node[1]+dir[1])
                    if self.is_valid(candidate, grid):
                        queue.append(candidate)
        
        return -1
        
    def is_valid(self, node, grid):
        m = len(grid)
        n = len(grid[1])
        if 0 <= node[0] < m and 0 <= node[1] < n and grid[node[0]][node[1]] == 0:
            return True
        
        return False
```



# 无向图中的最短路径

## 题目描述

### **描述**

814

给定一个无向图, 图中所有边的长度为1, 再选定图中的两个节点, 返回这两个节点之间最短的路径的长度.

```
输入: graph = {1,2,4#2,1,4#3,5#4,1,2#5,3}, node1 = 3, node2 = 5
输出: 1

解释: 
  1------2  3
   \     |  | 
    \    |  |
     \   |  |
      \  |  |
        4   5
```

## 题目分析

- Bfs 依旧类似linkedin找人脉的n度关系，记录一个level，用层序遍历的思想
- 两种思路，一个起点开始bfs，两个起点开始bfs
  - 双向肯定效果更好，但是写起来复杂一点
- 这里是无向图，老老实实记录visited set。树这种有向的可以不用记。

## 题目解答

```python
# 一个起点开始bfs
class Solution:
    """
    @param graph: a list of Undirected graph node
    @param A: nodeA
    @param B: nodeB
    @return:  the length of the shortest path
    """
    def shortestPath(self, graph, A, B):
        queue = []
        visited = set()
        
        queue.append(A)
        
        
        level = -1
        while queue:
            # print([q.label for q in queue])
            length = len(queue)
            level += 1
            for _ in range(length):
                node = queue.pop(0)
                visited.add(node)
                if node == B:
                    return level
                
                for n in node.neighbors:
                    if n in visited:
                        continue
                    queue.append(n)
        return -1
```



```python
# 双向bfs
# 抄的，大概就是这个思路吧
from collections import deque
class Solution:
    """
    @param graph: a list of Undirected graph node
    @param A: nodeA
    @param B: nodeB
    @return:  the length of the shortest path
    """
    def shortestPath(self, graph, A, B):
        if A == B:
            return 0
        
        queuel = deque([A])
        queuer = deque([B])
        visited = set([A, B])
        dl = 0
        dr = 0
        
        while queuel and queuer:
            dl += 1
            for _ in range(len(queuel)):
                nodel = queuel.popleft()
                for neibl in nodel.neighbors:
                    if neibl in queuer:
                        return dl + dr
                    if neibl not in visited:
                        queuel.append(neibl)
                        visited.add(neibl)
            
            dr += 1
            for _ in range(len(queuer)):
                noder = queuer.popleft()
                for neibr in noder.neighbors:
                    if neibr in queuel:
                        return dl + dr
                    if neibr not in visited:
                        queuer.append(neibr)
                        visited.add(neibr)
        
        return -1
```