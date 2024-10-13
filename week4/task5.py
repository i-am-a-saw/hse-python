"""
https://leetcode.com/problems/number-of-subarrays-with-bounded-maximum/description/?envType=problem-list-v2&envId=array
"""

from typing import List


class Solution:
    def numSubarrayBoundedMax(self, nums: List[int], left: int, right: int) -> int:
        def count_subarrays(bound: int) -> int:
            count = temp_count = 0
            for value in nums:
                temp_count = 0 if value > bound else temp_count + 1
                count += temp_count

            return count

        return count_subarrays(right) - count_subarrays(left - 1)
