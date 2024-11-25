"""
https://leetcode.com/problems/find-longest-special-substring-that-occurs-thrice-i/?envType=problem-list-v2&envId=sliding-window
"""

from collections import defaultdict


class Solution:
    def maximumLength(self, s: str) -> int:
        def is_valid(x: int) -> bool:
            char_counts = defaultdict(int)
            index = 0
            while index < string_length:
                next_index = index + 1
                while next_index < string_length and s[next_index] == s[index]:
                    next_index += 1
                char_counts[s[index]] += max(0, next_index - index - x + 1)
                index = next_index
            return max(char_counts.values()) >= 3

        string_length = len(s)
        left, right = 0, string_length

        while left < right:
            mid = (left + right + 1) >> 1
            if is_valid(mid):
                left = mid
            else:
                right = mid - 1

        return -1 if left == 0 else left
