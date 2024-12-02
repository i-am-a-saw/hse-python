"""
https://leetcode.com/problems/longest-nice-subarray/?envType=problem-list-v2&envId=sliding-window
"""


from typing import List

class Solution:
    def longestNiceSubarray(self, nums: List[int]) -> int:
        max_length = start_index = bit_mask = 0

        for end_index, number in enumerate(nums):
            while bit_mask & number:
                bit_mask ^= nums[start_index]
                start_index += 1
            max_length = max(max_length, end_index - start_index + 1)
            bit_mask |= number
          
        return max_length
