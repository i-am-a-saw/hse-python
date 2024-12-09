"""
https://leetcode.com/problems/construct-string-from-binary-tree/?envType=problem-list-v2&envId=binary-tree
"""


class Solution:
    def tree2str(self, root: Optional[TreeNode]) -> str:
        def dfs(root):
            if root is None:
                return ""
            if root.left is None and root.right is None:
                return str(root.val)
            if root.right is None:
                return f"{root.val}({dfs(root.left)})"
            return f"{root.val}({dfs(root.left)})({dfs(root.right)})"

        return dfs(root)
