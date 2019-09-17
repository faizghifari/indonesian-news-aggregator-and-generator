
class ArticleGeneratorHelper():

    def __parse_based_on_relevancy(self, base_text):
        relevance_texts = []
        irrelevance_texts = []
        for text in base_text:
            if text['relevance']:
                relevance_texts.append(text)
            else:
                irrelevance_texts.append(text)
        return relevance_texts, irrelevance_texts

    def __get_text_details(self, combined_sentences, text):
        temp_str = ''
        start_idx_doc, stop_idx_doc = -1, -1
        start_idx_src, stop_idx_src = -1, -1
        src_text, src_sentences, doc_pos, src_pos = [], [], [], []
        sentences = text['sentences']
        for i in range(len(sentences)):
            try:
                idx = combined_sentences.index(sentences[i])
                temp_str = ''.join([temp_str, sentences[i]])
                src_sentences.append(sentences[i])
                if (start_idx_doc == -1):
                    start_idx_doc = idx
                    start_idx_src = i
                stop_idx_doc = idx
                stop_idx_src = i

            except ValueError:
                if (start_idx_doc == -1):
                    pass
                else:
                    src_text.append(temp_str)
                    doc_pos.append(tuple((start_idx_doc, stop_idx_doc)))
                    src_pos.append(tuple((start_idx_src, stop_idx_src)))
                    temp_str = ''
                    start_idx_doc, stop_idx_doc = -1, -1
                    start_idx_src, stop_idx_src = -1, -1
            
            if (i == len(sentences) - 1) and (start_idx_doc != -1):
                src_text.append(temp_str)
                doc_pos.append(tuple((start_idx_doc, stop_idx_doc)))
                src_pos.append(tuple((start_idx_src, stop_idx_src)))

        sum_len_text = 0
        for txt in src_text:
            sum_len_text += len(txt)

        return {
            "text": src_text,
            "sentences": src_sentences,
            "pos_in_text": doc_pos,
            "pos_in_src": src_pos,
            "sum_len_text": sum_len_text
        }

    def __get_plagiarism_details(self, g_text, combined_sentences, text):
        text_details = self.__get_text_details(combined_sentences, text)
        copied_text = text_details['text']
        sum_len_text = text_details['sum_len_text']
        return {
            "src_id": text['id'],
            "src_url": text['url'],
            "concated_text": copied_text,
            "sentences": text_details['sentences'],
            "pos_in_text": text_details['pos_in_text'],
            "pos_in_src": text_details['pos_in_src'],
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
    
    def __generate_articles(self, texts):
        generated_articles = []
        for i in range(len(texts)):
            generated_text = ''
            combined_sentences = []
            start_idx = i
            for j in range(len(texts)):
                sentences = texts[start_idx]['sentences']
                count_sentences = int(len(sentences) / len(texts))
                if count_sentences == 0:
                    count_sentences = 1
                count_idx = int(count_sentences * j)
                if count_idx >= len(sentences):
                    count_idx = len(sentences) - 1
                for _ in range(count_sentences):
                    if generated_text != '':
                        generated_text = ''.join([generated_text, ' . ', sentences[count_idx]])
                    else:
                        generated_text = sentences[count_idx]
                    combined_sentences.append(sentences[count_idx])
                    count_idx += 1
                if (start_idx == len(texts) - 1):
                    start_idx = 0
                else:
                    start_idx += 1
            plagiarism_data = self.__get_generated_info(generated_text, combined_sentences, texts)
            generated_articles.append({
                "text": generated_text,
                "sentences": combined_sentences,
                "plagiarism_data": plagiarism_data
            })
        
        return generated_articles
    
    def generate_from_item(self, raw_item):
        item = raw_item
        base_text = item['base_text']

        relevance_texts, irrelevance_texts = self.__parse_based_on_relevancy(base_text)

        generated_r_texts = self.__generate_articles(relevance_texts)
        item['generated_r_text'] = generated_r_texts
        return item

    def generate_from_items(self, raw_items):
        items = raw_items
        for item in items:
            item = self.generate_from_item(item)
        return items