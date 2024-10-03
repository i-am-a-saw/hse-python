"""
https://leetcode.com/problems/container-with-most-water/description/?envType=problem-list-v2&envId=array
"""


class Solution(object):
    def maxArea(self, height):
        left, right = 0, len(height) - 1
        curr_vol = 0

        while left != right:
            if (right - left) * (min(height[left], height[right])) > curr_vol:
                curr_vol = (right - left) * (min(height[left], height[right]))
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
              
        return curr_vol
