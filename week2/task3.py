"""
https://leetcode.com/problems/letter-combinations-of-a-phone-number/description/?envType=problem-list-v2&envId=string
"""


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if digits == "":
            return []

        ans = []
        letters = ["abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"]

        for char1 in letters[int(digits[0]) - 2]:
            if len(digits) > 1:
                for char2 in letters[int(digits[1]) - 2]:
                    if len(digits) > 2:
                        for char3 in letters[int(digits[2]) - 2]:
                            if len(digits) > 3:
                                for char4 in letters[int(digits[3]) - 2]:
                                    s = char1 + char2 + char3 + char4
                                    ans.append(s)
                            else:
                                ans.append(char1 + char2 + char3)
                    else:
                        ans.append(char1 + char2)
            else:
                ans.append(char1)

        return ans
