import os
import json
import requests

from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

from helper.google_cse_helper import GoogleCSEHelper

from util.support import SupportUtil

GoogleCSEHelper = GoogleCSEHelper()
SupportUtil = SupportUtil()

PARSE_FAILED_MSG = os.getenv('PARSE_FAILED_MSG')

if __name__ == "__main__":
    keywords = SupportUtil.get_keywords()
    items = []
    id_counter = 0
    iteration = 0
    for keyword in keywords:
        print('KEYWORD: ', keyword)
        print('ITERATION: ', iteration)
        iteration += 1
        raw_results, id_counter = GoogleCSEHelper.search_and_get_results(keyword, id_counter)
        raw = []
        for raw_result in raw_results:
            url = SupportUtil.resolve_url(raw_result['url'])
            raw_html = requests.get(url).content
            print(url)
            if (raw_html is not None):
                raw.append(raw_html)
            else:
                print(PARSE_FAILED_MSG)
        item = SupportUtil.build_item(keyword, raw)
        items.append(item)
            
    dict_obj = { 'items': items }
    file_obj = open('raw_html.json', 'w')
    json.dump(dict_obj, file_obj)
