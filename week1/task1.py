"""
https://leetcode.com/problems/zigzag-conversion/?envType=problem-list-v2&envId=string
"""


class Solution:
    def convert(self, s: str, numRows: int) -> str:
        direction = "down"
        index = 0
        mas = []

        if numRows == 1:
            return s

        for i in range(numRows):
            mas.append([])
        print(mas)

        for st in s:
            print(index)

            mas[index].append(st)

            if direction == "down":
                index += 1
            else:
                index -= 1

            if index + 1 == numRows:
                direction = "up"
            if index == 0:
                direction = "down"

        ans = ""
        for i in range(numRows):
            ans += "".join(mas[i])
        return "".join(ans)
