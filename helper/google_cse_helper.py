import os

from googleapiclient.discovery import build
from helper.nlp_helper import NLPHelper

class GoogleCSEHelper():
    """
    Module to search on Google CSE based on keyword. Also help to parse results
    """
    def __init__(self):
        self.nlp_helper = NLPHelper()

    def google_search(self, search_term, api_key, cse_id, **kwargs):
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return res
    
    def __get_links(self, items):
        links = []
        for item in items:
            links.append(item['link'])
        return links
    
    def __get_titles(self, items):
        titles = []
        for item in items:
            titles.append(item['title'])
        return titles

    def __get_titles_similarity(self, base, titles):
        sims = self.nlp_helper.sentence_similarity(titles, base)
        return sims
    
    def get_all_info(self, results, relevance_threshold):
        items = results['items']
        links = self.__get_links(items)
        titles = self.__get_titles(items)

        base = titles[0]
        sims = self.__get_titles_similarity(base, titles)
        all_info = []
        for i in range(len(items)):
            info = {
                "url": links[i],
                "title": titles[i],
                "sims": sims[i],
                "relevance": float(sims[i]) > float(relevance_threshold)
            }
            all_info.append(info)
        return all_info
