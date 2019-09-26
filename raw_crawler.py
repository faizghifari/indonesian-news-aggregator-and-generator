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
        search_res = GoogleCSEHelper.search_only(keyword)
        items.append({
            "keyword": keyword,
            "search_res": search_res
        })
            
    dict_obj = { 'items': items }
    file_obj = open('raw_cse_2.json', 'w')
    json.dump(dict_obj, file_obj)
