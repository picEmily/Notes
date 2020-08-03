import heapq
import sys

# 出现最多的k个单词


class Solution(object):
    def __init__(self):
        self.k = 10
        self.m = {}

    def read(self):
        while True:
            # 读
            line = sys.stdin.readline().strip()
            if line == '':
                break
            for word in line:
                if word in self.m:
                    self.m[word] += 1
                else:
                    self.m[word] = 1

    def top_k_words(self):
        self.heap = []

        for word in self.m:
            if len(self.heap) < self.k:
                heapq.heappush(self.heap, (self.m[word], word))
            else:
                # 和最小的数比较，若大于它，将其替换
                if (self.m[word], word) > self.heap[0]:
                    heapq.heapreplace(self.heap, (self.m[word], word))

        result = []
        while self.k > 0:
            cnt, w = heapq.heappop(self.heap)
            result.append((w, cnt))
            self.k -= 1

        return result
