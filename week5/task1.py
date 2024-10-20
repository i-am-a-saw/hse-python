"""
https://leetcode.com/problems/minimum-number-of-operations-to-make-array-continuous/?envType=problem-list-v2&envId=hash-table
"""

from typing import List


class Solution:
    def minOperations(self, nums: List[int]) -> int:
        list_length = len(nums)
        nums = sorted(set(nums))
        min_ops = list_length
        window_start = 0

        for window_end, value in enumerate(nums):
            while (
                window_start < len(nums)
                and nums[window_start] - value <= list_length - 1
            ):
                window_start += 1
            min_ops = min(min_ops, list_length - (window_start - window_end))

        return min_ops
