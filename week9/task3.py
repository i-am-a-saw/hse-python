"""
https://leetcode.com/problems/validate-binary-tree-nodes/?envType=problem-list-v2&envId=binary-tree
"""

from typing import List


class Solution:
    def validateBinaryTreeNodes(
        self, node_count: int, left_children: List[int], right_children: List[int]
    ) -> bool:
        def find_root(x: int) -> int:
            if parents[x] != x:
                parents[x] = find_root(parents[x])
            return parents[x]

        parents = list(range(node_count))

        visited = [False] * node_count

        for i, (left_child, right_child) in enumerate(
            zip(left_children, right_children)
        ):
            for child in (left_child, right_child):
                if child != -1:
                    if visited[child] or find_root(i) == find_root(child):
                        return False

                    parents[find_root(i)] = find_root(child)
                    visited[child] = True
                    node_count -= 1

        return node_count == 1
