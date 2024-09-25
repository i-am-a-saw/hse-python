"""
https://leetcode.com/problems/wildcard-matching/description/?envType=problem-list-v2&envId=string
"""


class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        sl = len(s)
        pl = len(p)

        dp = [[False] * (pl + 1) for i in range(sl + 1)]

        dp[0][0] = True

        for i in range(1, pl + 1):
            if p[i - 1] == "*":
                dp[0][i] = dp[0][i - 1]

        for i in range(1, sl + 1):
            for j in range(1, pl + 1):

                if p[j - 1] == s[i - 1] or p[j - 1] == "?":
                    dp[i][j] = dp[i - 1][j - 1]

                elif p[j - 1] == "*":
                    dp[i][j] = dp[i][j - 1] or dp[i - 1][j]

        return dp[sl][pl]
