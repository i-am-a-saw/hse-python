"""
https://leetcode.com/problems/search-in-rotated-sorted-array/description/?envType=problem-list-v2&envId=array
"""


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1

        while l < r:
            m = (l + r) // 2
            if nums[0] <= nums[m]:
                if nums[0] <= target <= nums[m]:
                    r = m
                else:
                    l = m + 1
            else:
                if nums[m] < target <= nums[-1]:
                    l = m + 1
                else:
                    r = m
                    
        if nums[l] == target:
            return l
        else:
            return -1
