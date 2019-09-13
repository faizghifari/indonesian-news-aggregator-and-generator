
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
            generated_articles.append({
                "text": generated_text,
                "sentences": combined_sentences
            })
        
        return generated_articles
    
    def generate_from_item(self, raw_item):
        item = raw_item
        base_text = item['base_text']

        relevance_texts, irrelevance_texts = self.__parse_based_on_relevancy(base_text)

        generated_r_texts = self.__generate_articles(relevance_texts)
        generated_ir_texts = self.__generate_articles(irrelevance_texts)
        item['generated_r_text'] = generated_r_texts
        item['generated_ir_text'] = generated_ir_texts
        return item

    def generate_from_items(self, raw_items):
        items = raw_items
        for item in items:
            item = self.generate_from_item(item)
        return items