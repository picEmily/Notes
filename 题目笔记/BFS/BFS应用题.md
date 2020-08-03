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