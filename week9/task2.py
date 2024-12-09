"""
https://leetcode.com/problems/longest-univalue-path/?envType=problem-list-v2&envId=binary-tree
"""


class Solution:
    def longestUnivaluePath(self, root: TreeNode) -> int:
        def dfs(node):
            if node is None:
                return 0

            left_path_length = dfs(node.left)
            right_path_length = dfs(node.right)

            left_path = left_path_length + 1 if node.left and node.left.val == node.val else 0
            right_path = right_path_length + 1 if node.right and node.right.val == node.val else 0

            nonlocal longest_path
            longest_path = max(longest_path, left_path + right_path)

            return max(left_path, right_path)

        longest_path = 0
        dfs(root)
        return longest_path
