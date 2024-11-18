class Solution:
    def maxConsecutiveAnswers(self, answer_key: str, k: int) -> int:
        def get_max_consecutive(char_to_flip, k):
            left = right = max_length = 0
            while right < len(answer_key):
                if answer_key[right] != char_to_flip:
                    k -= 1

                while k < 0:
                    if answer_key[left] != char_to_flip:
                        k += 1
                    left += 1

                max_length = max(max_length, right - left + 1)

                right += 1

            return max_length

        return max(get_max_consecutive("T", k), get_max_consecutive("F", k))
