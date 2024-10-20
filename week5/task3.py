"""
https://leetcode.com/problems/optimal-partition-of-string/?envType=problem-list-v2&envId=hash-table
"""


class Solution:
    def partitionString(self, s: str) -> int:
        partitions = 1
        used_characters = 0

        for char in s:
            char_index = ord(char) - ord("a")
            if (used_characters >> char_index) & 1:
                used_characters = 0
                partitions += 1
            used_characters |= 1 << char_index

        return partitions
