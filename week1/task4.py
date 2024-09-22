"""
https://leetcode.com/problems/count-and-say/description/?envType=problem-list-v2&envId=string
"""


def prep(s: str):
    if s == "1":
        return "11"

    ans = ""
    count = 1

    for i in range(len(s) - 1):
        if s[i] == s[i + 1]:
            count += 1
        else:
            ans += str(count) + s[i]
            count = 1

    if s[-1] == s[-2]:
        ans += str(count) + s[-1]
    else:
        ans += "1" + s[-1]

    return ans


class Solution:
    def countAndSay(self, n: int) -> str:
        if n == 1:
            return "1"
        return prep(self.countAndSay(n - 1))
