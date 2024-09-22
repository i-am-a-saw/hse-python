"""
https://leetcode.com/problems/longest-palindromic-substring/description/?envType=problem-list-v2&envId=string
"""

import math


def f(s, a, b):
    while a >= 0 and b < len(s) and s[a] == s[b]:
        a -= 1
        b += 1
    return b - a - 1


class Solution:
    def longestPalindrome(self, s: str) -> str:
        start, end = 0, 0

        for i in range(0, len(s)):
            l1 = f(s, i, i)
            l2 = f(s, i, i + 1)
            ans = max(l1, l2)

            if ans > end - start:
                start = math.ceil(i - (ans - 1) / 2)
                end = math.floor(i + (ans / 2))

        return s[start : end + 1]
