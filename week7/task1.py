"""
https://leetcode.com/problems/count-of-substrings-containing-every-vowel-and-k-consonants-ii/description/?envType=problem-list-v2&envId=sliding-window
"""


class Solution:
    def countOfSubstrings(self, word: str, k: int) -> int:
        def f(k: int) -> int:
            cnt = Counter()
            ans = l = x = 0
            for c in word:
                if c in "aeiou":
                    cnt[c] += 1
                else:
                    x += 1
                while x >= k and len(cnt) == 5:
                    d = word[l]
                    if d in "aeiou":
                        cnt[d] -= 1
                        if cnt[d] == 0:
                            cnt.pop(d)
                    else:
                        x -= 1
                    l += 1
                ans += l
            return ans

        return f(k) - f(k + 1)
