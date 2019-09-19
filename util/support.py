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
    
    def build_plagiat_item(self, g_text, src_text, sentences, idx, is_plagiat):
        concat_substr = ''
        list_substr, pos_text_src = [], []
        per_in_text, per_in_src = 0, 0
        if is_plagiat:
            concat_substr = ' . '.join(sentences)
            list_substr = sentences
            for i in range(len(list_substr)):
                try:
                    idx_src = g_text['sentences'].index(list_substr[i])
                    pos_text_src.append(tuple((idx_src,idx[i])))
                except ValueError:
                    pass
            per_in_text = float(float(len(concat_substr) / len(g_text)) * 100.0)
            per_in_src = float(float(len(concat_substr) / len(src_text['text'])) * 100.0)

        return {
            'concatenated_text': concat_substr,
            'sentences': list_substr,
            'pos_text_src': pos_text_src,
            'per_in_text': per_in_text,
            'per_in_src': per_in_src
        }
    
    def build_pair(self, g_text, src_text, plagiat_item, is_plagiat):
        return {
            'input_text': g_text['text'],
            'compared_text': src_text['text'],
            'is_plagiarism': is_plagiat,
            'plagiarism_details': {
                'concat_substr': plagiat_item['concatenated_text'],
                'list_substr': plagiat_item['sentences'],
                'pos_text_src': plagiat_item['pos_text_src'],
                'per_in_text': plagiat_item['per_in_text'],
                'per_in_src': plagiat_item['per_in_src']
            }
        }

    def build_all_pairs(self, keyword, pairs):
        return {
            "keyword": keyword,
            "pairs": pairs
        }

    def build_pairs_from_item(self, item):
        pairs = []
        base_text = item['base_text']
        generated_texts = item['generated_r_text']
        for g_text in generated_texts:
            for plagiat_item in g_text['plagiarism_data']['plagiarism_items']:
                for src_text in base_text:
                    if (plagiat_item['src_id'] == src_text['id']):
                        pairs.append(self.build_pair(g_text, src_text, plagiat_item, True))
                        break
                    elif (src_text['relevance'] == False):
                        # check
                        plgt_sentences = []
                        plgt_idx = []
                        is_plagiat = False
                        for sentences in src_text['sentences']:
                            if (sentences in g_text['text']) or (sentences in g_text['sentences']):
                                plgt_sentences.append(sentences)
                                plgt_idx.append(src_text['sentences'].index(sentences))
                        if (len(plgt_sentences) != 0):
                            print('ADAAAAAA')
                            is_plagiat = True
                        plgt_item = self.build_plagiat_item(g_text, src_text, plgt_sentences, plgt_idx, is_plagiat)
                        pairs.append(self.build_pair(g_text, src_text, plgt_item, is_plagiat))
                    else: continue

        return pairs

    def build_pairs_from_items(self, items):
        pairs = []
        count_pair = 0
        for item in items:
            pair = self.build_pairs_from_item(item)
            count_pair += len(pair)
            pairs.append(self.build_all_pairs(item['keyword'], pair))
        print('NUM PAIRS GENERATED  :', count_pair)
        return pairs

    
    