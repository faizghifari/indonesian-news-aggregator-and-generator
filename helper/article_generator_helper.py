import random
import math
import os

class ArticleGeneratorHelper():
    def __init__(self):
        self.num_articles = int(os.getenv('NUM_ARTICLES'))
        self.num_texts = int(os.getenv('NUM_TEXTS'))
        self.max_n_articles = int(os.getenv('MAX_N_ARTICLES'))
        self.min_n_texts = int(os.getenv('MIN_N_TEXTS'))
        self.list_text_per = [float(i) for i in os.getenv('LIST_TEXT_PER').split(',')]

    def __parse_based_on_relevancy(self, base_text):
        relevance_texts = []
        irrelevance_texts = []
        for text in base_text:
            if text['relevance']:
                relevance_texts.append(text)
            else:
                irrelevance_texts.append(text)
        return relevance_texts, irrelevance_texts

    def __get_max_min_length(self, texts):
        min_len = 999
        max_len = -1
        for text in texts:
            length = len(text['sentences'])
            min_len = min(min_len, length)
            max_len = max(max_len, length)
        return max_len, min_len
    
    def __get_n_articles(self, lent, opt='random'):
        if (opt == 'random'):
            return random.randint(lent, self.max_n_articles)
        else:
            return self.num_articles
    
    def __get_n_texts(self, lent, opt='random'):
        if (opt == 'random'):
            try:
                return random.randint(self.min_n_texts, lent)
            except ValueError:
                return min(lent, self.num_texts)
            
        else:
            return min(lent, self.num_texts)
    
    def __get_n_sentences(self, sentences, texts, counter, len_article, n_texts_remain, opt):
        if (counter == len(self.list_text_per)):
            counter = 0
        n_sentences = math.ceil(float(self.list_text_per[counter] * len(sentences)))
        if (opt == 'random'):
            n_sentences = random.randint(1, len_article - n_texts_remain)
        else:
            counter += 1

        first = False
        if (n_texts_remain == len(texts) - 1):
            n_sentences -= 1
            first = True
        
        return min(n_sentences, len(sentences) - 1), first, counter
    
    def __get_len_article(self, texts, opt='random'):
        if (opt == 'random'):
            max_len, min_len = self.__get_max_min_length(texts)
            if (min_len < len(texts)):
                min_len = len(texts)
            return random.randint(min_len, max_len)
        else:
            return -1

    def __get_text_details(self, combined_sentences, text):
        pos_text_src, src_sentences = [], []
        sentences = text['sentences']
        for i in range(len(sentences)):
            try:
                idx = combined_sentences.index(sentences[i])
                src_sentences.append(sentences[i])
                pos_text_src.append(tuple((idx,i)))
            except ValueError:
                pass
        src_text = ' . '.join(src_sentences)
        return {
            "text": src_text,
            "sentences": src_sentences,
            "pos_text_src": pos_text_src,
            "sum_len_text": len(src_text)
        }

    def __get_plagiarism_details(self, g_text, combined_sentences, text):
        text_details = self.__get_text_details(combined_sentences, text)
        copied_text = text_details['text']
        sum_len_text = text_details['sum_len_text']
        return {
            "src_id": text['id'],
            "src_url": text['url'],
            "concatenated_text": copied_text,
            "sentences": text_details['sentences'],
            "pos_text_src": text_details['pos_text_src'],
            "per_in_text": float(float(sum_len_text / len(g_text)) * 100.0),
            "per_in_src": float(float(sum_len_text / len(text['text'])) * 100.0)
        }
    
    def __get_generated_info(self, g_text, combined_sentences, texts):
        plagiarism_items = []
        for text in texts:
            plagiarism_items.append(self.__get_plagiarism_details(g_text,combined_sentences, text))
        plagiarism_per_text = float(0.0)
        for item in plagiarism_items:
            plagiarism_per_text +=  item['per_in_text']
        plagiarism_data = {
            "plagiarism_items": plagiarism_items,
            "plagiarism_total_in_text": plagiarism_per_text
        }
        return plagiarism_data

    def __generate_article(self, texts, len_article, counter, id_counter, opt='random'):
        n_texts_remain = len(texts)
        combined_sentences = []
        for text in texts:
            try:
                sentences = text['sentences'].copy()
                n_texts_remain -= 1
                n_sentences, first, counter = self.__get_n_sentences(sentences, texts, counter, len_article, n_texts_remain, opt)
                if first:
                    combined_sentences.append(sentences[0])
                sentences.pop(0)
                if (opt == 'random'):
                    if (n_texts_remain == 0):
                        n_sentences = len_article
                    len_article -= n_sentences
                chosen_sentences = random.sample(sentences, n_sentences)
                for sentence in chosen_sentences:
                    combined_sentences.append(sentence)
            
            except IndexError:
                pass
        
        generated_text = ' . '.join(combined_sentences)
        plagiarism_data = self.__get_generated_info(generated_text, combined_sentences, texts)
        return {
            "id": id_counter,
            "text": generated_text,
            "sentences": combined_sentences,
            "plagiarism_data": plagiarism_data
        }, counter, id_counter+1

    def __generate_articles_v2(self, texts, counter, id_counter):
        n_articles = self.__get_n_articles(len(texts))
        generated_articles = []
        for _ in range(n_articles):
            n_texts = self.__get_n_texts(len(texts))
            chosen_texts = random.sample(texts, n_texts)
            len_article = self.__get_len_article(chosen_texts, opt='fixed')
            article, counter, id_counter = self.__generate_article(chosen_texts, len_article, counter, id_counter, opt='fixed')
            generated_articles.append(article)

        return generated_articles, counter, id_counter
    
    def generate_from_item(self, raw_item, counter, id_counter):
        item = raw_item
        base_text = item['base_text']

        relevance_texts, _ = self.__parse_based_on_relevancy(base_text)

        if (relevance_texts is not None) and (len(relevance_texts) > 0):
            generated_r_texts, counter, id_counter = self.__generate_articles_v2(relevance_texts, counter, id_counter)
            item['generated_r_text'] = generated_r_texts
        return item, counter, id_counter

    def generate_from_items(self, raw_items, counter):
        items = raw_items
        data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        id_counter = 0
        for item in items:
            item, counter, id_counter = self.generate_from_item(item, counter, id_counter)
            try:
                for article in item['generated_r_text']:
                    for plagiat_data in article['plagiarism_data']['plagiarism_items']:
                        data[int(round(plagiat_data['per_in_src'],-1) / 10)] += 1
            except KeyError:
                pass

        print('DATA     : ', data)
        print('SUM      : ', sum(data))
        return items