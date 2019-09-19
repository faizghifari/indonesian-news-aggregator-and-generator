import os
import errno
import json

class DumpUtil():

    def __init__(self):
        self.results_dir_path = os.getenv('RESULTS_DIR_PATH')
        self.base_text_dir_path = os.getenv('BASE_TEXT_DIR_PATH')
        self.generated_text_r_dir_path = os.getenv('GENERATED_TEXT_R_DIR_PATH')
        self.generated_text_ir_dir_path = os.getenv('GENERATED_TEXT_IR_DIR_PATH')
        self.results_json_path = os.getenv('RESULTS_JSON_PATH')

    def __resolve_dir_path(self, keyword):
        keyword_dir_path = keyword.replace(' ', '-') + '/'
        return self.results_dir_path + keyword_dir_path

    def __resolve_path(self, keyword, file_name, type_):
        dir_path = self.__resolve_dir_path(keyword)
        if (type_ == 'base_text'):
            dir_path += self.base_text_dir_path
        elif (type_ == 'generated_r_text'):
            dir_path += self.generated_text_r_dir_path
        else:
            dir_path += self.generated_text_ir_dir_path
        return dir_path + file_name

    def __write_file(self, filepath, text):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            f.write(text)
    
    def __dump_based_on_type(self, keyword, item, type_):
        for i in range(len(item[type_])):
            file_name = str(i) + '.txt'
            filepath = self.__resolve_path(keyword, file_name, type_)
            text = item[type_][i]['text']
            self.__write_file(filepath, text)

    def __dump_json(self, path, dict_obj):
        file_obj = open(path, 'w')
        json.dump(dict_obj, file_obj)
    
    def dump_item_to_txt(self, item):
        keyword = item['keyword']
        self.__dump_based_on_type(keyword, item, 'base_text')
        self.__dump_based_on_type(keyword, item, 'generated_r_text')
        # self.__dump_based_on_type(keyword, item, 'generated_ir_text')
    
    def dump_item_to_json(self, item):
        keyword = item['keyword']
        dir_path = self.__resolve_dir_path(keyword)
        filename = keyword.replace(' ', '-') + '.json'
        self.__dump_json(dir_path + filename, item)

    def dump_items_to_txt(self, items):
        for item in items:
            self.dump_item_to_txt(item)
    
    def dump_items_to_json(self, items):
        dict_obj = {}
        dict_obj['items'] = items
        self.__dump_json(self.results_json_path, dict_obj)
    
    def dump_pair_to_json(self, pair):
        keyword = pair['keyword']
        dir_path = self.__resolve_dir_path(keyword)
        filename = keyword.replace(' ', '-') + '-pairs' + '.json'
        self.__dump_json(dir_path + filename, pair)

    def dump_pairs_to_json(self, pairs):
        dict_obj = { 'pairs': pairs }
        self.__dump_json('test_pairs.json', dict_obj)