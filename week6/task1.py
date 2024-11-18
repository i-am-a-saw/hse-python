from math import inf


class Solution:
    def minimumCardPickup(self, cards: List[int]) -> int:
        last_seen = {}
        min_ = inf

        for index, card_value in enumerate(cards):
            if card_value in last_seen:
                min_ = min(min_, index - last_seen[card_value] + 1)
            last_seen[card_value] = index

        return -1 if min_ == inf else min_
