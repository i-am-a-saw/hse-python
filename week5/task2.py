"""
https://leetcode.com/problems/count-words-obtained-after-adding-a-letter/?envType=problem-list-v2&envId=hash-table
"""

from typing import List


class Solution:
    def wordCount(self, start_words: List[str], target_words: List[str]) -> int:
        bit_masks = set()
        
        for word in start_words:
            mask = 0
            for char in word:
                mask |= 1 << (ord(char) - ord("a"))
            bit_masks.add(mask)

        valid_target_count = 0

        for word in target_words:
            mask = 0
            
            for char in word:
                mask |= 1 << (ord(char) - ord("a"))

            for char in word:
                temp_mask = mask ^ (1 << (ord(char) - ord("a")))
                if temp_mask in bit_masks:
                    valid_target_count += 1
                    break

        return valid_target_count
