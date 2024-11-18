from collections import defaultdict


class Solution:
    def maxSubarrayLength(self, nums: List[int], k: int) -> int:
        frequency_counter = defaultdict(int)
        max_length = 0
        left_pointer = 0

        for right_pointer, value in enumerate(nums):
            frequency_counter[value] += 1

            while frequency_counter[value] > k:
                frequency_counter[nums[left_pointer]] -= 1
                left_pointer += 1

            current_length = right_pointer - left_pointer + 1
            max_length = max(max_length, current_length)

        return max_length
