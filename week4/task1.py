"""
https://leetcode.com/problems/falling-squares/description/?envType=problem-list-v2&envId=array
"""


class Node:
    def __init__(self, start, end):
        self.left = None
        self.right = None
        self.start = start
        self.end = end
        self.mid = (start + end) >> 1
        self.value = 0
        self.add = 0


class SegmentTree:
    def __init__(self):
        self.root = Node(1, int(1e9))

    def modify(self, start, end, value, node=None):
        if start > end:
            return
        if node is None:
            node = self.root
        if node.start >= start and node.end <= end:
            node.value = value
            node.add = value
            return
        self.pushdown(node)
        if start <= node.mid:
            self.modify(start, end, value, node.left)
        if end > node.mid:
            self.modify(start, end, value, node.right)
        self.pushup(node)

    def query(self, start, end, node=None):
        if start > end:
            return 0
        if node is None:
            node = self.root
        if node.start >= start and node.end <= end:
            return node.value
        self.pushdown(node)
        max_value = 0
        if start <= node.mid:
            max_value = max(max_value, self.query(start, end, node.left))
        if end > node.mid:
            max_value = max(max_value, self.query(start, end, node.right))
        return max_value

    def pushup(self, node):
        node.value = max(node.left.value, node.right.value)

    def pushdown(self, node):
        if node.left is None:
            node.left = Node(node.start, node.mid)
        if node.right is None:
            node.right = Node(node.mid + 1, node.end)
        if node.add:
            node.left.value = node.add
            node.right.value = node.add
            node.left.add = node.add
            node.right.add = node.add
            node.add = 0


class Solution:
    def fallingSquares(self, positions: List[List[int]]) -> List[int]:
        max_height = 0
        result = []
        tree = SegmentTree()

        for left, size in positions:
            right = left + size - 1

            height = tree.query(left, right) + size
            max_height = max(max_height, height)
            result.append(max_height)

            tree.modify(left, right, height)

        return result
