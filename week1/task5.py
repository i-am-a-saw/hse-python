"""
https://leetcode.com/problems/string-to-integer-atoi/description/?envType=problem-list-v2&envId=string
"""


class Solution:
    def myAtoi(self, s: str) -> int:

        begin = 0
        sign = 0
        ans = ""

        for i in range(len(s)):
            if s[i] == " " and (begin == 1 or sign == 1):
                break
            elif (s[i] == "-") and sign == 0 and begin == 0:
                ans += "-"
                sign = 1
            elif s[i] == "+" and begin == 1:
                break
            elif s[i] == "+" and sign == 0:
                sign = 1
            elif s[i] == "-" and (begin == 1 or sign == 1) or s[i] == "+" and sign == 1:
                break
            elif s[i].isdigit() and begin == 0 and s[i] != "0":
                ans += s[i]
                begin = 1
            elif s[i].isdigit() and begin == 0:
                begin = 1
            elif s[i].isdigit() and begin == 1:
                ans += s[i]
            elif s[i].isalpha() or s[i] == "." or (s[i] == " " and begin == 1):
                break

        if ans and ans != "-":
            if int(ans) < -(2**31):
                return -(2**31)
            elif int(ans) > 2**31 - 1:
                return 2**31 - 1
            return int(ans)
        return 0
