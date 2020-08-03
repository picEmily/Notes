# -*- coding:utf-8 -*-
import collections
import sys
import math


# 1. read one number
def read_one_int():
    n = int(sys.stdin.readline().strip())


# 2. read one char
def read_one_char():
    s = sys.stdin.readline().strip('\n')


# 3. 多行number，且以空格分隔
def read_multi_num():
    l = []
    while True:
        # 若是多输入，strip()默认是以空格分隔，返回一个包含多个字符串的list。
        line = sys.stdin.readline().strip()
        if sn == '':
            break
        # 如果是一个list数字强制转换成int等类型，可以调用map()函数。
        line_list = list(map(int, line.split()))
        l.append(line_list)


# 4. 多行字符，且以空格分隔
def read_multi_char():
    ls = []
    while True:
        # 若是多输入，strip()默认是以空格分隔，返回一个包含多个字符串的list。
        sn = sys.stdin.readline().strip()
        if sn == '':
            break
        ls.append(sn.split())


# 5. 格式输出 以空格分隔
def out_put(x):
    s = " ".join(str(i) for i in x)
    return s


# 6. 两种sort
def test_sort():
    list.sort(cmp=None, key=None, reverse=False)
    l = sorted(l, key=None, reverse=False)


# 7. stack and queue
def deque_sample():
    queue = collections.deque()
    for i in range(10):
        queue.append(i)
    node = queue.popleft()

    stack = collections.deque()
    for i in range(10):
        stack.append(i)
    node = stack.pop()


# 8. 常用math lib
def math_lib_sample():
    # math lib用float，比自带的精准
    # round
    math.ceil(3.1)  # 4
    math.floor(3.8)  # 3

    # pow and log
    math.exp(1)  # 2.718
    math.pow(2, 3)  # 8.0
    math.sqrt(9)  # 3.0

    math.log(100, 10)  # 2.0
    math.log2(8) == math.log(8, 2)  # True

    # abs sum
    math.fabs(-3)  # 3.0
    abs(-3.5)  # 3.5
    math.fsum([1,2,3])  # 6.0
    sum([1,2,3])  # 6


# 9. 字符串相关计算
# ascii to int
def test_ascii_num():
    ch = 'a'
    asc = 67

    print(ch + " 的ASCII 码为", ord(ch))
    print(asc, " 对应的字符为", chr(asc))


# 反转链表
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def ReverseList(self, pHead):
    # write code here
    if not pHead or not pHead.next:
        return pHead
    else:
        newHead = self.ReverseList(pHead.next)
        pHead.next.next = pHead
        pHead.next = None
        return newHead


def sample_lambda():
    lambda x, y, z: x+y+z


def sample_map():
    pass

# format
def sample_format():
    print("%.2f" % 1)

if __name__ == '__main__':
    test_ascii_num()


import java.io.*;
import java.util.*;

/*
 * To execute Java, please define "static void main" on a class
 *
 * If you define many classes, but you must have a class named Main and a public property.
 * The Main class should be the only public class.
 * The Main class must contain a static method (function) named "main" 
 * Do not add any package, like "package main"
 *
 * The TestCase is shown below
 * Input : 1 2
 * Output : 3
 */

class Main {
	public static void main(String[] args) {
		ArrayList<String> strings = new ArrayList<String>();
		strings.add("Hello, World!");
		strings.add("Welcome to online interview system of Acmcoder.");
		strings.add("This system is running Java 8.");

		for (String string : strings) {
			System.out.println(string);
		}

		int a, b;
		Scanner in = new Scanner(System.in);
		while(in.hasNextInt()) {
			a = in.nextInt();
			b = in.nextInt();
			System.out.printf("Your result is : %d\n", a + b);
		}
	}
}


多进程共用全局队列，那么无外乎两种情况，一种全局队列存在内存中，
比如用redis，一种全局队列存在硬盘上，比如数据库mysql。
多进程通信的话还可以考虑pipe和socket, multiprocessing.Manager.Queue就是pipe通信。


# 一维背包
# 背包总体来说是归纳
# dp[k] = dp[x] + dp[x]
import java.util.*;
 
public class Main{
    public static final int ASD = 1000000007;
     
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        int k=sc.nextInt();
        int a=sc.nextInt(), x=sc.nextInt();
        int b=sc.nextInt(), y=sc.nextInt();
        int[] dp = new int[k+1];
        dp[0] = 1;
        for(int i=0; i<x ; i++){
            for(int j=k; j>=a; j--){
                dp[j] = (dp[j] + dp[j-a]) % ASD;
            }
        }
         
        for(int i=0; i<y ; i++){
            for(int j=k; j>=b; j--){
                dp[j] = (dp[j] + dp[j-b]) % ASD;
            }
        }
         
        System.out.println(dp[k]);
        sc.close();
    }
}


# LCA
"""
Definition of TreeNode:
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None
"""


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
        
        return path_A[idx]
        
    def find(self, root, result, node):
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

            

