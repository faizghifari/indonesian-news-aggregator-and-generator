import os

class SupportUtil():

    def __init__(self):
        self.keywords = self.__load_keywords(os.getenv('KEYWORDS_PATH'))
    
    def __load_keywords(self, keywords_path):
        keywords = set()
        with open(keywords_path, 'r') as f:
            for line in f:
                keywords.add(line.strip().lower())
        return keywords
    
    def get_keywords(self):
        return self.keywords
    
    def resolve_url(self, url):
        if ('detik.com' in url):
            return url + '?single=1'
        else:
            return url
    
    def build_base_text(self, raw_result, results):
        return {
            "id": raw_result['id'],
            "url": self.resolve_url(raw_result['url']),
            "title": raw_result['title'],
            "base": raw_result['base'],
            "sims": raw_result['sims'],
            "relevance": raw_result['relevance'],
            "text": results['parsed_content'],
            "sentences": results['parsed_sentences']
        }
    
    def build_item(self, keyword, base_text):
        return {
            "keyword": keyword,
            "base_text": base_text
        }