import os
import errno
import json

from helper.article_generator_helper import ArticleGeneratorHelper

ArticleGeneratorHelper = ArticleGeneratorHelper()
results_path = "./results/"

raw = {}
with open('base_example.json') as json_file:
    raw = json.load(json_file)

items = raw['items']
items = ArticleGeneratorHelper.generate_from_items(items)

def write_file(filepath, text):
    print(filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(text)

for item in items:
    keyword_dir_path = item['keyword'].replace(' ', '-') + '/'
    base_dir_path = 'base_text/'
    for i in range(len(item['base_text'])):
        file_name = str(i) + '.txt'
        text = item['base_text'][i]['text']
        complete_path = results_path + keyword_dir_path + base_dir_path + file_name
        write_file(complete_path, text)

    generated_r_path = 'generated_r_text/'
    for i in range(len(item['generated_r_text'])):
        file_name = str(i) + '.txt'
        text = item['generated_r_text'][i]['text']
        complete_path = results_path + keyword_dir_path + generated_r_path + file_name
        write_file(complete_path, text)

    generated_ir_path = 'generated_ir_text/'
    for i in range(len(item['generated_ir_text'])):
        file_name = str(i) + '.txt'
        text = item['generated_ir_text'][i]['text']
        complete_path = results_path + keyword_dir_path + generated_ir_path + file_name
        write_file(complete_path, text)
