# 拓扑排序
127 拓扑排序
# 题目分析
怎么输出所有可能排序？？
# 题目解答
```python
"""
Definition for a Directed graph node
class DirectedGraphNode:
    def __init__(self, x):
        self.label = x
        self.neighbors = []
"""

class Solution:
    """
    @param graph: A list of Directed graph node
    @return: Any topological order for the given graph.
    """
    def topSort(self, graph):
        node_to_indegree = self.get_indegree(graph)

        # bfs
        order = []
        start_nodes = [n for n in graph if node_to_indegree[n] == 0]
        queue = collections.deque(start_nodes)
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in node.neighbors:
                node_to_indegree[neighbor] -= 1
                if node_to_indegree[neighbor] == 0:
                    queue.append(neighbor)
                
        return order
    
    def get_indegree(self, graph):
        node_to_indegree = {x: 0 for x in graph}

        for node in graph:
            for neighbor in node.neighbors:
                node_to_indegree[neighbor] += 1
                
        return node_to_indegree
```

# 课程表
615 现在你总共有 n 门课需要选，记为 0 到 n - 1.
一些课程在修之前需要先修另外的一些课程，比如要学习课程 0 你需要先学习课程 1 ，表示为[0,1]
给定n门课以及他们的先决条件，判断是否可能完成所有课程？
# 题目分析
拓扑排序 复习拓扑排序

步骤：
- 初始化一个int[] inDegree保存每一个结点的入度。
- 对于图中的每一个结点的子结点，将其子结点的入度加1。
- 选取入度为0的结点开始遍历，并将该节点加入queue。
- 对于遍历过的每个结点，更新其子结点的入度：将子结点的入度减1。
重复步骤3，直到遍历完所有的结点。
- 如果无法遍历完所有的结点，则意味着当前的图不是有向无环图。不存在拓扑排序。

入度：指向这个节点的节点个数
# 题目解答
```python
from collections import deque

class Solution:
    """
    @param: numCourses: a total of n courses
    @param: prerequisites: a list of prerequisite pairs
    @return: true if can finish all courses or false
    """
    def canFinish(self, numCourses, prerequisites):
        # 入度
        degrees = [0 for _ in range(numCourses)]
        
        # edges,指向的边 1->2, 1->3 那么 {1: [2,3]}
        edges = {i : [] for i in range(numCourses)}

        for i, j in prerequisites:
            edges[j].append(i)  # j->i 表示j是i的先修课
            degrees[i] += 1
            
        queue = deque()
        
        # 入度为0的先加入队列，等待弹出
        for i in range(numCourses):
            if degrees[i] == 0:
                queue.append(i)
        
        count = 0
        while queue:
            node = queue.popleft()
            count += 1
            for x in edges[node]:
                degrees[x] -= 1
                if degrees[x] == 0:
                    queue.append(x)
        # 最终其实是如果所有元素的degree都为零，说明可以成功排序
        # 为了少一次遍历，用count记录一下
        
        return count == numCourses
```


# 安排课程
616
你需要去上n门九章的课才能获得offer，这些课被标号为 0 到 n-1 。
有一些课程需要“前置课程”，比如如果你要上课程0，你需要先学课程1，我们用一个匹配来表示他们： [0,1]

给你课程的总数量和一些前置课程的需求，返回你为了学完所有课程所安排的学习顺序。

可能会有多个正确的顺序，你只要返回一种就可以了。如果不可能完成所有课程，返回一个空数组。

```
输入: n = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]] 
输出: [0,1,2,3] or [0,2,1,3]
```

# 题目分析
上一题返回true false，这一题返回一个合法的排序

# 题目解答

```python
from collections import deque
class Solution:
    """
    @param: numCourses: a total of n courses
    @param: prerequisites: a list of prerequisite pairs
    @return: the course order
    """
    def findOrder(self, numCourses, prerequisites):
        degree = [0 for _ in range(numCourses)]
        edges = {i : [] for i in range(numCourses)}
        
        for i, j in prerequisites:
            # i<-j
            degree[i] += 1
            edges[j].append(i)
        
        queue = deque()
        result = []
        
        for x in range(numCourses):
            if degree[x] == 0:
                queue.append(x)
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            for x in edges[node]:
                degree[x] -= 1
                if degree[x] == 0:
                    queue.append(x)
        
        if len(result) == numCourses:
            return result
        return []
```

# 题目描述
判断是否序列 org 能唯一地由 seqs重构得出. org是一个由从1到n的正整数排列而成的序列，1 ≤ n ≤ 10^4。 重构表示组合成seqs的一个最短的父序列 (意思是，一个最短的序列使得所有 seqs里的序列都是它的子序列).
判断是否有且仅有一个能从 seqs重构出来的序列，并且这个序列是org。

# 题目分析
翻译成人话就是：序列能否是另一个序列的子序列

**序列可以翻译成有向图**，而有向图可以用拓扑排序来解决问题

# 题目解答
```
待解决
```