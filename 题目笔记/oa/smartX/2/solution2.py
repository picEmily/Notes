# 2 sum
class Solutoin(object):
    def __init__(self, K, nums):
        self.K = K
        self.nums = nums

    def get_sum_k(self):
        cnt = 0
        hash_set = set()
        for i in range(len(self.nums)):
            if self.K - self.nums[i] in hash_set:
                cnt += 1
            hash_set.add(self.nums[i])

        return cnt

    def get_subs_k(self):
        cnt = 0
        hash_set = set()
        for i in range(len(self.nums)):
            if abs(self.K - self.nums[i] in hash_set):
                cnt += 1
            hash_set.add(self.nums[i])

        return cnt
