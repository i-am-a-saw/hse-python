"""
https://leetcode.com/problems/create-maximum-number/description/?envType=problem-list-v2&envId=array
"""

from typing import List


class Solution:
    def maxNumber(self, nums1: List[int], nums2: List[int], k: int) -> List[int]:
        def is_greater(nums1: List[int], nums2: List[int], i: int, j: int) -> bool:
            while i < len(nums1) and j < len(nums2) and nums1[i] == nums2[j]:
                i += 1
                j += 1
            return j == len(nums2) or (i < len(nums1) and nums1[i] > nums2[j])

        def find_max_sequence(nums: List[int], k: int) -> List[int]:
            stack = [0] * k
            to_remove = len(nums) - k
            top = -1
            for num in nums:
                while top >= 0 and stack[top] < num and to_remove > 0:
                    top -= 1
                    to_remove -= 1
                if top + 1 < k:
                    top += 1
                    stack[top] = num
                else:
                    to_remove -= 1
            return stack

        def merge(nums1: List[int], nums2: List[int]) -> List[int]:
            merged = []
            i = j = 0
            while i < len(nums1) or j < len(nums2):
                if is_greater(nums1, nums2, i, j):
                    merged.append(nums1[i])
                    i += 1
                else:
                    merged.append(nums2[j])
                    j += 1
            return merged

        best_sequence = [0] * k
        for count in range(max(0, k - len(nums2)), min(k, len(nums1)) + 1):
            candidate1 = find_max_sequence(nums1, count)
            candidate2 = find_max_sequence(nums2, k - count)
            candidate_merged = merge(candidate1, candidate2)
            if best_sequence < candidate_merged:
                best_sequence = candidate_merged

        return best_sequence
