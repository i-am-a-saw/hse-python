"""
https://leetcode.com/problems/delete-leaves-with-a-given-value/?envType=problem-list-v2&envId=binary-tree
"""


class Solution:
    def removeLeafNodes(
        self, root: Optional[TreeNode], target: int
    ) -> Optional[TreeNode]:
        if root is None:
            return None
        root.left = self.removeLeafNodes(root.left, target)
        root.right = self.removeLeafNodes(root.right, target)

        if root.left is None and root.right is None and root.val == target:
            return None

        return root
