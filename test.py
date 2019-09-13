import json

from helper.article_generator_helper import ArticleGeneratorHelper

raw = {}

with open('try.json') as json_file:
    raw = json.load(json_file)

items = raw['items']

ArticleGeneratorHelper = ArticleGeneratorHelper()

items = ArticleGeneratorHelper.generate_from_items(items)

file_obj = open('test.json', 'w')
dict_obj = {}

dict_obj['items'] = items

json.dump(dict_obj, file_obj)