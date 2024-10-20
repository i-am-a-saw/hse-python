"""
https://leetcode.com/problems/minimum-number-of-groups-to-create-a-valid-assignment/?envType=problem-list-v2&envId=hash-table
"""

from collections import Counter
from typing import List


class Solution:
    def minGroupsForValidAssignment(self, nums: List[int]) -> int:
        frequency_count = Counter(nums)

        for group_size in range(max(frequency_count.values()), 0, -1):
            groups_needed = 0
            for frequency in frequency_count.values():
                if frequency // group_size < frequency % group_size:
                    groups_needed = 0
                    break

                groups_needed += -(-frequency // (group_size + 1))

            if groups_needed:
                return groups_needed

        return 0
