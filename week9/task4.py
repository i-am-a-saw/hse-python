"""
https://leetcode.com/problems/count-nodes-with-the-highest-score/submissions/1474101544/?envType=problem-list-v2&envId=binary-tree
"""

from typing import List


class Solution:
    def countHighestScoreNodes(self, parents: List[int]) -> int:
        num_nodes = len(parents)
        max_score = 0
        answer = 0

        graph = [[] for _ in range(num_nodes)]

        for i in range(1, num_nodes):
            graph[parents[i]].append(i)

        def dfs(current_node: int) -> int:
            nonlocal max_score, answer
            subtree_size = 1
            node_score = 1

            for child in graph[current_node]:
                child_subtree_size = dfs(child)
                subtree_size += child_subtree_size
                node_score *= child_subtree_size

            if current_node > 0:
                node_score *= num_nodes - subtree_size

            if node_score > max_score:
                max_score = node_score
                answer = 1
            elif node_score == max_score:
                answer += 1

            return subtree_size

        dfs(0)

        return answer
