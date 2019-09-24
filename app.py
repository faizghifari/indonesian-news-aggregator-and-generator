import os
import json
import requests

from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

from helper.news_parser_helper import NewsContentParser
from helper.google_cse_helper import GoogleCSEHelper
from helper.article_generator_helper import ArticleGeneratorHelper

from util.support import SupportUtil
from util.dump import DumpUtil

GoogleCSEHelper = GoogleCSEHelper()
ArticleGeneratorHelper = ArticleGeneratorHelper()
SupportUtil = SupportUtil()
DumpUtil = DumpUtil()

PARSE_FAILED_MSG = os.getenv('PARSE_FAILED_MSG')

if __name__ == "__main__":
    keywords = SupportUtil.get_keywords()
    items = []
    id_counter = 0
    for keyword in keywords:
        raw_results, id_counter = GoogleCSEHelper.search_and_get_results(keyword, id_counter)
        base_text = []
        for raw_result in raw_results:
            url = SupportUtil.resolve_url(raw_result['url'])
            raw_html = requests.get(url).content
            parser = NewsContentParser(raw_html, url)

            results = parser.parse_content()
            print(url)
            if (results is not None):
                check = SupportUtil.build_base_text(raw_result, results)
                base_text.append(check)
            else:
                print('\n', PARSE_FAILED_MSG, '\n')
        
        item = SupportUtil.build_item(keyword, base_text)
        # item, per_counter = ArticleGeneratorHelper.generate_from_item(item, per_counter)

        # DumpUtil.dump_item_to_txt(item)
        # DumpUtil.dump_item_to_json(item)
        
        items.append(item)
    
    dict_obj = { 'items': items }
    file_obj = open('base_example.json', 'w')
    json.dump(dict_obj, file_obj)

    per_counter = 0
    items = ArticleGeneratorHelper.generate_from_items(items, per_counter)  
    pairs = SupportUtil.build_pairs_from_items(items)
    base_texts = SupportUtil.build_base_texts(items)
    for pair in pairs:
        DumpUtil.dump_pair_to_json(pair)
    DumpUtil.dump_base_texts_to_json(base_texts)
    DumpUtil.dump_pairs_to_json(pairs)
    DumpUtil.dump_items_to_json(items)
