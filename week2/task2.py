"""
https://leetcode.com/problems/sum-of-prefix-scores-of-strings/description/?envType=problem-list-v2&envId=string&difficulty=HARD
"""


class Tree:
    def __init__(self):
        self.nodes = [""] * 26
        self.count = 0

    def insert(self, word):
        node = self
        for c in word:
            if node.nodes[ord(c) - ord("a")] == "":
                node.nodes[ord(c) - ord("a")] = Tree()
            node = node.nodes[ord(c) - ord("a")]
            node.count += 1

    def search(self, word):
        node = self
        total = 0
        for c in word:
            if node.nodes[ord(c) - ord("a")] == "":
                return total
            node = node.nodes[ord(c) - ord("a")]
            total += node.count
        # print(total)
        return total


class Solution:
    def sumPrefixScores(self, words: List[str]) -> List[int]:
        t = Tree()
        for w in words:
            t.insert(w)
        ans = []
        for i in range(len(words)):
            ans.append(t.search(words[i]))
        return ans
