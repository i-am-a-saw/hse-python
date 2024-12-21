"""
https://leetcode.com/problems/maximum-width-of-binary-tree/?envType=problem-list-v2&envId=binary-tree
"""

from collections import deque


class Solution:
    def widthOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        max_width = 0
        queue = deque([(root, 1)])

        while queue:
            current_width = queue[-1][1] - queue[0][1] + 1
            max_width = max(max_width, current_width)

            for _ in range(len(queue)):
                node, index = queue.popleft()

                if node.left:
                    queue.append((node.left, index << 1))

                if node.right:
                    queue.append((node.right, (index << 1) | 1))

        return max_width
