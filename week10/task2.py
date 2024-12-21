"""
https://leetcode.com/problems/binary-tree-pruning/?envType=problem-list-v2&envId=binary-tree
"""


class Solution:
    def prune_tree(self, root: TreeNode) -> TreeNode:
        if root is None:
            return None

        root.left = self.prune_tree(root.left)
        root.right = self.prune_tree(root.right)

        if root.val == 0 and root.left is None and root.right is None:
            return None

        return root

    pruneTree = prune_tree
