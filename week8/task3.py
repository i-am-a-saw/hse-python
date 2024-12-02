"""
https://leetcode.com/problems/k-radius-subarray-averages/description/?envType=problem-list-v2&envId=sliding-window
"""

from typing import List


class Solution:
    def getAverages(self, nums: List[int], k: int) -> List[int]:
        window_sum = 0
        averages = [-1] * len(nums)  
      
        for index, value in enumerate(nums):
            window_sum += value
            if index >= k * 2:
                averages[index - k] = window_sum // (k * 2 + 1)
                window_sum -= nums[index - k * 2]
      
        return averages
