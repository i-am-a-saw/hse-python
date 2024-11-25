"""
https://leetcode.com/problems/smallest-subarrays-with-maximum-bitwise-or/description/?envType=problem-list-v2&envId=sliding-window
"""

from typing import List


class Solution:
    def smallestSubarrays(self, nums: List[int]) -> List[int]:
        length = len(nums)
        result = [1] * length
        last_seen_at = [-1] * 32

        for i in reversed(range(length)):
            max_size = 1
            for j in range(32):
                if (nums[i] >> j) & 1:
                    last_seen_at[j] = i
                elif last_seen_at[j] != -1:
                    max_size = max(max_size, last_seen_at[j] - i + 1)
            result[i] = max_size

        return result
