"""
https://leetcode.com/problems/even-odd-tree/submissions/1474102614/?envType=problem-list-v2&envId=binary-tree
"""

from collections import deque


class Solution:
    def isEvenOddTree(self, root: TreeNode) -> bool:
        level = 0
        queue = deque([root])

        while queue:
            previous_value = 0 if level % 2 == 0 else float("inf")

            for _ in range(len(queue)):
                node = queue.popleft()

                if level % 2 == 0 and (node.val % 2 == 0 or previous_value >= node.val):
                    return False
                if level % 2 == 1 and (node.val % 2 == 1 or previous_value <= node.val):
                    return False

                previous_value = node.val

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            level += 1

        return True
