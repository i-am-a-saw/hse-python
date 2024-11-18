from collections import defaultdict
from itertools import accumulate


class Solution:
    def maximumUniqueSubarray(self, nums: List[int]) -> int:
        index_dict = defaultdict(int)
        prefix_sums = list(accumulate(nums, initial=0))
        max_sum = start_index = 0

        for current_index, value in enumerate(nums, 1):
            start_index = max(start_index, index_dict[value])
            current_subarray_sum = prefix_sums[current_index] - prefix_sums[start_index]
            max_sum = max(max_sum, current_subarray_sum)
            index_dict[value] = current_index

        return max_sum
