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

RESULTS_USED_QTY = os.getenv('RESULTS_USED_QTY')

GoogleCSEHelper = GoogleCSEHelper()

keywords = set()
with open(KEYWORDS_PATH, 'r') as f:
    for line in f:
        keywords.add(line.strip().lower())

items = []

for keyword in keywords:
    search_results = GoogleCSEHelper.google_search(keyword, API_KEY, CSE_KEY)
    urls = GoogleCSEHelper.get_links(search_results, RESULTS_USED_QTY)
    base_text = []
    for url in urls:
        raw_html = requests.get(url).content

        parser = NewsContentParser(raw_html, NEWS_DICT_PATH, url)

        results = parser.parse_content()
        print(url)
        base_text.append({
            "url": url,
            "text": results['parsed_content'],
            "paragraph": results['parsed_paragraph']
        })
    items.append({
        "keyword": keyword,
        "base_text": base_text
    })

file_obj = open(RESULTS_PATH, 'w')
dict_obj = {}

dict_obj['items'] = items

json.dump(dict_obj, file_obj)

