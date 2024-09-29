"""
https://leetcode.com/problems/decode-ways/submissions/1406545279/?envType=problem-list-v2&envId=string
"""


class Solution:
    def numDecodings(self, s: str) -> int:

        last, now = 0, 1

        for i in range(len(s)):
            next_ = 0

            if s[i] != "0":
                next_ = now
            if i > 0 and (s[i - 1] == "1" or (s[i - 1] == "2" and s[i] < "7")):
                if s[i - 1] != "0":
                    next_ += last

            last, now = now, next_

        return now
