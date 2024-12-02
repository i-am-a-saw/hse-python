"""
https://leetcode.com/problems/count-zero-request-servers/submissions/1468042559/?envType=problem-list-v2&envId=sliding-window
"""

from collections import Counter
from itertools import count


class Solution:
    def countServers(self, server_count: int, logs: List[List[int]], time_window: int, queries: List[int]) -> List[int]:
        server_activity_counter = Counter()
        logs.sort(key=lambda log: log[1])
        answer = [0] * len(queries)
        log_index = time_index = 0

        for query_time, original_index in sorted(zip(queries, count())):
            lower_time_limit = query_time - time_window

            while log_index < len(logs) and logs[log_index][1] <= query_time:
                server_activity_counter[logs[log_index][0]] += 1
                log_index += 1
           
            while time_index < len(logs) and logs[time_index][1] < lower_time_limit:
                server_activity_counter[logs[time_index][0]] -= 1
                if server_activity_counter[logs[time_index][0]] == 0:     
                    del server_activity_counter[logs[time_index][0]]
                time_index += 1

            answer[original_index] = server_count - len(server_activity_counter)
      
        return answer
