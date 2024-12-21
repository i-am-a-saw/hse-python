"""
https://leetcode.com/problems/count-nodes-equal-to-average-of-subtree/?envType=problem-list-v2&envId=binary-tree
"""

class Solution:
    def averageOfSubtree(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if node is None:
                return 0, 0
            
            left_sum, left_count = dfs(node.left)
            right_sum, right_count = dfs(node.right)
            subtree_sum = left_sum + right_sum + node.val
            subtree_count = left_count + right_count + 1

            if subtree_sum // subtree_count == node.val:
                nonlocal total_count
                total_count += 1

            return subtree_sum, subtree_count

        total_count = 0
        dfs(root)

        return total_count
