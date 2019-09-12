import os
import json
import requests

from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

from helper.news_parser_helper import NewsContentParser
from helper.google_cse_helper import GoogleCSEHelper

API_KEY = os.getenv('API_KEY')
CSE_KEY = os.getenv('CSE_KEY')

SEARCH_SERVICE_NAME = os.getenv('SEARCH_SERVICE_NAME')
SEARCH_SERVICE_VERSION = os.getenv('SEARCH_SERVICE_VERSION')

NEWS_DICT_PATH = os.getenv('NEWS_DICT_PATH')
KEYWORDS_PATH = os.getenv('KEYWORDS_PATH')
RESULTS_PATH = os.getenv('RESULTS_PATH')

RELEVANCE_THRESHOLD = os.getenv('RELEVANCE_THRESHOLD')

GoogleCSEHelper = GoogleCSEHelper()

keywords = set()
with open(KEYWORDS_PATH, 'r') as f:
    for line in f:
        keywords.add(line.strip().lower())

items = []

for keyword in keywords:
    search_results = GoogleCSEHelper.google_search(keyword, API_KEY, CSE_KEY)
    raw_results = GoogleCSEHelper.get_all_info(search_results, RELEVANCE_THRESHOLD)
    base_text = []
    for raw_result in raw_results:
        url = raw_result['url']
        if ('detik.com' in url):
            url = url + '?single=1'

        raw_html = requests.get(url).content

        parser = NewsContentParser(raw_html, NEWS_DICT_PATH, url)

        results = parser.parse_content()
        print(url)
        if (results is not None):
            base_text.append({
                "url": url,
                "title": raw_result['title'],
                "sims": raw_result['sims'],
                "relevance": raw_result['relevance'],
                "text": results['parsed_content'],
                "sentences": results['parsed_sentences']
            })
        else:
            print('\n', "WARNING: CONTENT FAILED TO BE PARSED/URL NOT INCLUDED", '\n')
    items.append({
        "keyword": keyword,
        "base_text": base_text
    })

file_obj = open(RESULTS_PATH, 'w')
dict_obj = {}

dict_obj['items'] = items

json.dump(dict_obj, file_obj)

