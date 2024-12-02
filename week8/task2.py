"""
https://leetcode.com/problems/maximum-sum-of-two-non-overlapping-subarrays/description/?envType=problem-list-v2&envId=sliding-window
"""

from itertools import accumulate


class Solution:
    def maxSumTwoNoOverlap(self, nums: List[int], first_len: int, second_len: int) -> int:
        n = len(nums)
        prefix_sums = list(accumulate(nums, initial=0))
        max_sum = max_sum_first_array = 0
        i = first_len

        while i + second_len - 1 < n:
            max_sum_first_array = max(max_sum_first_array, prefix_sums[i] - prefix_sums[i - first_len])
            max_sum = max(max_sum, max_sum_first_array + prefix_sums[i + second_len] - prefix_sums[i])
            i += 1

        max_sum_second_array = 0        
        i = second_len

        while i + first_len - 1 < n:
            max_sum_second_array = max(max_sum_second_array, prefix_sums[i] - prefix_sums[i - second_len])
            max_sum = max(max_sum, max_sum_second_array + prefix_sums[i + first_len] - prefix_sums[i])
            i += 1
      
        return max_sum
