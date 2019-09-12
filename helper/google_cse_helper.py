import os

from googleapiclient.discovery import build

class GoogleCSEHelper():
    """
    Module to search on Google CSE based
    """
    def google_search(self, search_term, api_key, cse_id, **kwargs):
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return res
    
    def get_links(self, results, qty):
        items = results['items']
        links = []
        for idx in range(int(qty)):
            links.append(items[idx]['link'])
        return links