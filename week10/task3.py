"""
https://leetcode.com/problems/maximum-binary-tree-ii/?envType=problem-list-v2&envId=binary-tree
"""

class Solution:
    def insertIntoMaxTree(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if root is None or root.val < val:
            return TreeNode(val, root)

        root.right = self.insertIntoMaxTree(root.right, val)

        return root
