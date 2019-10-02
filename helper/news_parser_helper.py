import json
import re
import os

from bs4 import BeautifulSoup

from helper.nlp_helper import NLPHelper

class NewsContentParser():
    """
    Module to parse content from news
    """
    def __init__(self, html, url):
        self.news_dict = self.__load_news_dict(os.getenv('NEWS_DICT_PATH'))
        self.soup = self.__load_soup(html)
        self.nlp_helper = NLPHelper()
        self.url = url

    def __load_news_dict(self, dict_dir):
        with open(dict_dir) as json_file:
            news_dict = json.load(json_file)
            return news_dict
    
    def __load_soup(self, html):
        soup = BeautifulSoup(html, features='lxml')
        return soup

    def __get_news_info(self):
        all_news = self.news_dict['items']
        for news in all_news:
            if news['base_url'] in self.url:
                return news
        return None
    
    def __normalize_content(self, str_input):
        res = self.nlp_helper.normalization(str_input)
        if res is not None:
            res = re.sub('\[ .{1,3} \]', '', res)
            res = re.sub('\"(.+?)\"', '', res)
            res = re.sub('((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*', '', res)
            res = res.replace('\n', ' ')
            res = res.replace('\" ', '')
            return res
        else:
            return None

    def __find_content(self, tag, attr, attr_name):
        content = self.soup.find(tag, {attr: attr_name})
        return content
    
    def __find_content_all(self, tag, attr, attr_name):
        content = self.soup.find_all(tag, {attr: attr_name})
        return content
    
    def __find_descendants(self, content, descendant_tag):
        descendants = content.find_all(descendant_tag)
        return descendants
    
    def __parse_content(self, content):
        processed_str = ''
        for string in content.stripped_strings:
            if ((('{' not in string and '}' not in string) and (string != '')) 
                and (string is not None and 'Baca ' not in string)):
                processed_str = ' '.join([processed_str, string])
        return processed_str

    def __parse_descendants(self, descendants):
        processed_str = ''
        for descendant in descendants:
            paragraph_str = self.__parse_content(descendant)
            if ((paragraph_str is not None) and ('Baca ' not in paragraph_str)):
                processed_str = ' '.join([processed_str, paragraph_str])
        return processed_str
    
    def __parse_sentences(self, parsed_content):
        if parsed_content is not None:
            parsed_sentences = parsed_content.split(' .')
            parsed_sentences = [p for p in parsed_sentences if ((p is not None) and (len(p) > 50))]
            if (len(parsed_sentences) > 2):
                return parsed_sentences
            else:
                return None
        else:
            return None

    def __make_response(self, is_found, parsed_content, parsed_sentences):
        return {
            'is_found': is_found,
            'parsed_content': parsed_content,
            'parsed_sentences': parsed_sentences
        }

    def __not_found_response(self):
        self.__make_response(False, None, None)
    
    def parse_content(self):
        news_info = self.__get_news_info()
        if news_info is None:
            return self.__not_found_response()
        
        tag = news_info['content_tag']
        attr = news_info['content_attr']
        attr_name = news_info['attr_name']
        is_desc = news_info['use_descendants']
        desc_tag = news_info['descendants_tag']
        
        content = self.__find_content(tag, attr, attr_name)
        if content is not None:
            parsed_content = ''

            if is_desc:
                descendants = self.__find_descendants(content, desc_tag)
                parsed_content = self.__parse_descendants(descendants)
            else:
                parsed_content = self.__parse_content(content)

            parsed_content = self.__normalize_content(parsed_content)
            parsed_sentences = self.__parse_sentences(parsed_content)
            if (parsed_content is None) or (parsed_sentences is None):
                return self.__not_found_response()
            else:
                return self.__make_response(True, parsed_content, parsed_sentences)