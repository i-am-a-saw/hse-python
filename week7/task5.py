"""
https://leetcode.com/problems/maximum-points-you-can-obtain-from-cards/description/?envType=problem-list-v2&envId=sliding-window
"""


class Solution:
    def maxScore(self, cardPoints: List[int], k: int) -> int:
        n = len(cardPoints)
        leftSum = 0
      
        for i in range(k):
            leftSum += cardPoints[i]
          
        rightSum = 0
        rightIndex = n
        ans = leftSum
      
        for leftIndex in range(k - 1, -1, -1):
            leftSum -= cardPoints[leftIndex]
            rightIndex -= 1
            rightSum += cardPoints[rightIndex]
            ans = max(ans, leftSum + rightSum)
          
        return ans
