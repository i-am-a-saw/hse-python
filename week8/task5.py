"""
https://leetcode.com/problems/maximum-beauty-of-an-array-after-applying-operation/description/?envType=problem-list-v2&envId=sliding-window
"""

from typing import List


class Solution:
    def maximumBeauty(self, flowers: List[int], steps: int) -> int:
        max_flower = max(flowers) + steps * 2 + 2
        diff_array = [0] * max_flower
    
        for flower_count in flowers:
            diff_array[flower_count] += 1
            diff_array[flower_count + steps * 2 + 1] -= 1
        
        max_beauty = running_sum = 0
      
        for count_diff in diff_array:
            running_sum += count_diff
            max_beauty = max(max_beauty, running_sum)
      
        return max_beauty
