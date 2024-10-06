"""
https://leetcode.com/problems/maximal-square/description/?envType=problem-list-v2&envId=array
"""

from typing import List


class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        r, c = len(matrix), len(matrix[0])
        max_side_length = 0
        dp = [[0] * (c + 1) for _ in range(r + 1)]

        for row in range(r):
            for col in range(c):
                if matrix[row][col] == "1":
                    dp[row + 1][col + 1] = (
                        min(dp[row][col + 1], dp[row + 1][col], dp[row][col]) + 1
                    )
                    max_side_length = max(max_side_length, dp[row + 1][col + 1])

        return max_side_length * max_side_length
