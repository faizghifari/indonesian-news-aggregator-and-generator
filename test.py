import os
import json

from dotenv import load_dotenv
from pathlib import Path

ENV_PATH = Path('.') / '.env'
load_dotenv(dotenv_path=ENV_PATH)

from helper.article_generator_helper import ArticleGeneratorHelper
from util.dump import DumpUtil

ArticleGeneratorHelper = ArticleGeneratorHelper()
DumpUtil = DumpUtil()

if __name__ == "__main__":
    raw = {}
    with open('base_example.json') as json_file:
        raw = json.load(json_file)

    items = raw['items']
    items = ArticleGeneratorHelper.generate_from_items(items)

    # DumpUtil.dump_items_to_txt(items)
    DumpUtil.dump_items_to_json(items)
