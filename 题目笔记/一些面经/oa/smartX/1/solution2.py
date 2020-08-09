class Solution(object):
    """
    move within a list, odd nums moved to the first half and even the second
    """

    def partition(self, nums):
        left = 0
        right = len(nums) - 1

        while left <= right:
            while left <= right and self.is_odd(nums[left]):
                left += 1
            while left <= right and self.is_even(nums[right]):
                right -= 1

            # swap
            if left <= right:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1
                right -= 1

        return nums

    @staticmethod
    def is_odd(n):
        if n % 2 == 1:
            return True
        return False

    @staticmethod
    def is_even(n):
        if n % 2 == 0:
            return True
        return False


class Tests(object):
    def is_valid(self, nums):
        # odd flag = 0; even flag = 1
        flag = 0
        for n in nums:
            if flag == 1 and Solution.is_odd(n):
                return False
            if flag == 0 and Solution.is_even(n):
                flag = 1

        return True

    def test1(self):
        nums = [1, 2, 3, 4, 5, 6, 7, 8]
        print(Solution().partition(nums))
        assert(self.is_valid(Solution().partition(nums)))

    def test2(self):
        nums = [3, 4, 6, 8, 1, 2, 2, 2, 2, 2, 1]
        print(Solution().partition(nums))
        assert(self.is_valid(Solution().partition(nums)))

    def test3(self):
        nums = [0]
        print(Solution().partition(nums))
        assert(self.is_valid(Solution().partition(nums)))

    def test4(self):
        nums = []
        print(Solution().partition(nums))
        assert(self.is_valid(Solution().partition(nums)))

    def test5(self):
        nums = [1]
        print(Solution().partition(nums))
        assert(self.is_valid(Solution().partition(nums)))

    def test6(self):
        nums = [-1, 0, 1]
        print(Solution().partition(nums))
        assert(self.is_valid(Solution().partition(nums)))


if __name__ == "__main__":
    t = Tests()
    print('begin tests')
    t.test1()
    t.test2()
    t.test3()
    t.test4()
    t.test5()
    t.test6()
    print('pass')