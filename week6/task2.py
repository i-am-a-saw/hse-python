from bisect import bisect_left


class Solution:
    def maximizeWin(self, prize_positions: List[int], k: int) -> int:
        num_positions = len(prize_positions)
        dp = [0] * (num_positions + 1)
        max_win = 0

        for i, position in enumerate(prize_positions, 1):
            j = bisect_left(prize_positions, position - k)
            max_win = max(max_win, dp[j] + i - j)
            dp[i] = max(dp[i - 1], i - j)

        return max_win
