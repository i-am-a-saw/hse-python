"""
https://leetcode.com/problems/longest-substring-without-repeating-characters/description/?envType=problem-list-v2&envId=string
"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        maxl, l = 0, 0
        unique = set()

        for r, char in enumerate(s):
            while char in unique:
                unique.remove(s[l])
                l += 1

            unique.add(char)
            maxl = max(maxl, r - l + 1)

        return maxl
