"""
https://leetcode.com/problems/count-the-number-of-good-subarrays/?envType=problem-list-v2&envId=hash-table
"""

from collections import Counter


class Solution:
    def countGood(self, nums: List[int], k: int) -> int:
        num_counter = Counter()
        result = current_sum = start_index = 0

        for num in nums:
            current_sum += num_counter[num]
            num_counter[num] += 1

            while current_sum - num_counter[nums[start_index]] + 1 >= k:
                num_counter[nums[start_index]] -= 1
                current_sum -= num_counter[nums[start_index]]
                start_index += 1

            if current_sum >= k:
                result += start_index + 1

        return result
