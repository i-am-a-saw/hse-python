"""
https://leetcode.com/problems/find-the-longest-equal-subarray/?envType=problem-list-v2&envId=sliding-window
"""

from collections import Counter


class Solution:
    def longestEqualSubarray(self, nums: List[int], k: int) -> int:
        element_count = Counter()
        left = 0
        max_frequency = 0

        for right, element in enumerate(nums):
            element_count[element] += 1
             max_frequency = max(max_frequency, element_count[element])
            if right - left + 1 - max_frequency > k:     
                element_count[nums[left]] -= 1
                left += 1
     
        return right - left + 1
