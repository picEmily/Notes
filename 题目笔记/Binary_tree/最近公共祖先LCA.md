# 最近公祖先
## 题目描述
88，474，578
- 给定一棵二叉树，找到两个节点的最近公共父节点(LCA)。
最近公共祖先是两个节点的公共的祖先节点且具有最大深度。

578是最general的情况：如果不存在就返回None
## 题目分析
思路一：

我的第一个思路，先用dfs（回溯）找到A和B的path，然后再通过比较path找到LCA

思路二：

答案的方法利用递归，返回是否找到A，是否找到B，LCA(Null 或者一个点)。但是我并没有很明白为什么要这么做（大概是可以通过递归和分类讨论，不需要很大的代码量和思考）

递归查找A和B， 找到A和B第一次在同一棵子树中的子树根节点即是LCA。
归纳一下：
- 转化为判断某个节点是不是公共祖先的问题：用递归去判断，一直往下找
- 接下来是把最深的一个公共节点返回

注意：题目分为加入一定存在公共祖先的情况下和不一定存在的情况（返回None）。第一种情况更简单。

对于第二种情况

每次返回 是否在左子树中找到了节点A/B，是否在右子树中找到了节点A/B，以及是否已经找到了LCA(或找到A/B)，
这三个结果。然后分类讨论。如果已经在子树中找到了LCA,就直接return。否则，如果当前节点是
A且在子树中找到了B，或者当前节点是B且已经在子树中找到了A，就说明当前节点是LCA。
## 题目解答
```python
# V1 找到path，然后比较path找到路径
class Solution:
    """
    @param: root: The root of the binary search tree.
    @param: A: A TreeNode in a Binary.
    @param: B: A TreeNode in a Binary.
    @return: Return the least common ancestor(LCA) of the two nodes.
    """
    def lowestCommonAncestor(self, root, A, B):
        # first find these two nodes
        path_A = []
        path_B = []
        
        self.find(root, path_A, A)
        self.find(root, path_B, B)
        
        idx = 0
        # 思路一
        while True:
            if idx < len(path_A) and idx < len(path_B):
                if path_A[idx] == path_B[idx]:
                    idx += 1
                    continue
                else:
                    idx -= 1
                    print(idx)
                    break
            else:
                idx -= 1
                break
        # 思路二
        # 有点那个交叉链表找公共点的意思，先把长度搞成一样，然后倒着遍历找到第一个公共点
        
        return path_A[idx]
        
    def find(self, root, result, node):
      	# dfs 搜索路径
        if root:
            # put in 
            result.append(root)

            # recursion
            self.find(root.left, result, node)
            self.find(root.right, result, node)
            
            if len(result) > 0 and result[len(result) - 1] == node:
                return
            # pop out
            result.pop()
```
```python
# v2
# 答案的方法
class Solution:
    """
    @param: root: The root of the binary tree.
    @param: A: A TreeNode
    @param: B: A TreeNode
    @return: Return the LCA of the two nodes.
    """
    def lowestCommonAncestor3(self, root, A, B):
        a, b, lca = self.helper(root, A, B)
        if a and b:
            # 因为有可能有找不到A或B的情况需要判断
            return lca
        else:
            return None
    
    def helper(self, root, A, B):
        if root is None:
            return False, False, None
        
        # left_lca 指的是公共节点 没有就是None
        left_a, left_b, left_lca = self.helper(root.left, A, B)
        right_a, right_b, right_lca = self.helper(root.right, A, B)
        
        # 如果左边或右边有A或root本身就是A则a为true,说明A存在
        # false 表示A不存在
        a = left_a or right_a or root == A
        b = left_b or right_b or root == B
        
        # 如果找到A or B，就把它们一步步往上传
        if root == A or root == B:
            return a, b, root
        if left_lca is not None and right_lca is not None:
            # 此时left_lca 和 right_lca 应该是同一个
            return a, b, root
        if left_lca is not None:
            return a, b, left_lca
        if right_lca is not None:
            return a, b, right_lca
        
        return a, b, None
```