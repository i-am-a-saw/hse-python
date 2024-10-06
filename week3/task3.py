"""
https://leetcode.com/problems/gas-station/description/?envType=problem-list-v2&envId=array
"""

from typing import List


class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        nums = len(gas)
        ind = ind_e = nums - 1
        vis = total = 0

        while vis < nums:
            total += gas[ind_e] - cost[ind_e]
            vis += 1
            ind_e = (ind_e + 1) % nums

            while vis < nums and total < 0:
                ind = nums + ind - 1
                ind %= nums
                total += gas[ind] - cost[ind]
                vis += 1

        if total < 0:
            return -1
        else:
            return ind
