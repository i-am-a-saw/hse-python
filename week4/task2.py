"""
https://leetcode.com/problems/accounts-merge/description/?envType=problem-list-v2&envId=array
"""

from collections import defaultdict


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        def find(index: int) -> int:
            if parent[index] != index:
                parent[index] = find(parent[index])
            return parent[index]

        num_accounts = len(accounts)
        parent = list(range(num_accounts))
        email_to_account_id = {}

        for account_id, account in enumerate(accounts):
            for email in account[1:]:
                
                if email in email_to_account_id:
                    parent[find(account_id)] = find(email_to_account_id[email])
                else:
                    email_to_account_id[email] = account_id

        emails_under_parent_account = defaultdict(set)
        
        for account_index, account in enumerate(accounts):
            for email in account[1:]:
                emails_under_parent_account[find(account_index)].add(email)

        merged_accounts = []
        
        for parent_index, emails in emails_under_parent_account.items():
            sorted_emails = sorted(emails)
            account_name = [accounts[parent_index][0]]
            merged_account = account_name + sorted_emails
            merged_accounts.append(merged_account)

        return merged_accounts
