"""
https://leetcode.com/problems/delete-and-earn/description/?envType=problem-list-v2&envId=array
"""

from typing import List


class Solution:
    def deleteAndEarn(self, nums: List[int]) -> int:
        max_value = max(nums)
        total_points = [0] * (max_value + 1)

        for num in nums:
            total_points[num] += num

        earn_prev_prev = total_points[0]
        earn_prev = max(total_points[0], total_points[1])

        for i in range(2, max_value + 1):
            current_max = max(earn_prev_prev + total_points[i], earn_prev)
            earn_prev_prev = earn_prev
            earn_prev = current_max

        return earn_prev
