"""
https://leetcode.com/problems/integer-to-roman/description/?envType=problem-list-v2&envId=string
"""


class Solution:
    def intToRoman(self, num: int) -> str:

        num = (str(num))[::-1]
        ans = ""

        ed = {
            "1": "I",
            "2": "II",
            "3": "III",
            "4": "IV",
            "5": "V",
            "6": "VI",
            "7": "VII",
            "8": "VIII",
            "9": "IX",
            "0": "",
        }
        des = {
            "1": "X",
            "2": "XX",
            "3": "XXX",
            "4": "XL",
            "5": "L",
            "6": "LX",
            "7": "LXX",
            "8": "LXXX",
            "9": "XC",
            "0": "",
        }
        sot = {
            "1": "C",
            "2": "CC",
            "3": "CCC",
            "4": "CD",
            "5": "D",
            "6": "DC",
            "7": "DCC",
            "8": "DCCC",
            "9": "CM",
            "0": "",
        }
        tis = {"1": "M", "2": "MM", "3": "MMM"}

        for i in range(len(num)):
            if i == 0:
                ans += ed[num[0]]
            elif i == 1:
                if num[0] == "1" and num[1] == "1":
                    ans = "X" + ans
                else:
                    ans = des[num[1]] + ans
            elif i == 2:
                if num[0] == "1" and num[1] == "0" and num[2] == "1":
                    ans = "C" + ans
                else:
                    ans = sot[num[2]] + ans
            else:
                ans = tis[num[3]] + ans
        return ans
