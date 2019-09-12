import json

from bs4 import BeautifulSoup

class NewsContentParser():
    """
    Module to parse content from news
    """
    def __init__(self, html, dict_dir, url):
        self.news_dict = self.__load_news_dict(dict_dir)
        self.soup = self.__load_soup(html)
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
            if ('{' not in string and '}' not in string) and (string != ''):
                processed_str = ' '.join([processed_str, string])
        return processed_str

    def __parse_descendants(self, descendants):
        processed_str = ''
        paragraph = []
        for descendant in descendants:
            paragraph_str = self.__parse_content(descendant)
            processed_str = '\n'.join([processed_str, paragraph_str])
            paragraph.append(paragraph_str)
        return processed_str, paragraph

    def __make_response(self, is_found, parsed_content, parsed_paragraph):
        return {
            'is_found': is_found,
            'parsed_content': parsed_content,
            'parsed_paragraph': parsed_paragraph
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

        if (is_desc and desc_tag is None):
           content = self.__find_content_all(tag, attr, attr_name)
           parsed_content, parsed_paragraph = self.__parse_descendants(content)
           return self.__make_response(True, parsed_content, parsed_paragraph)
        
        content = self.__find_content(tag, attr, attr_name)
        if is_desc:
            descendants = self.__find_descendants(content, desc_tag)
            parsed_content, parsed_paragraph = self.__parse_descendants(descendants)
            return self.__make_response(True, parsed_content, parsed_paragraph)
        else:
            parsed_content = self.__parse_content(content)
            parsed_paragraph = parsed_content.split('.')
            return self.__make_response(True, parsed_content, parsed_paragraph)
