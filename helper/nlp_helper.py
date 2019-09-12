import requests
import json
import os


class NLPHelper():
    """
    Module for NLP supports
    """
    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
        self.endpoints = {
            'normalization': os.getenv('NORMALIZER_API',
                'http://10.181.131.241:20003/normalize'),
            'keywords_extraction': os.getenv('KEYWORDS_EXTRACTION_API',
                'http://10.181.131.241:4334/keywords'),
            'sentence_similarity': os.getenv('SENTENCE_SIMILARITY_API',
                'http://10.181.131.241:9337/similarity'),
            'pos_tag': os.getenv('POS_TAG_API',
                'http://10.181.131.241:5500'),
            'lemma' : os.getenv('SYNTAX_URL', 
                'http://10.181.131.241:5502')
        }


    def __create_request(self, endpoint, json_input):
        return requests.post(endpoint, headers=self.headers, json=json_input)

    def normalization(self, str_input):
        json_input = {'text': str_input}
        response = self.__create_request(self.endpoints['normalization'], json_input)
        if response.status_code != 200:
            return None
        return response.json()['text']

    def keywords_extraction(self, str_input):
        json_input = {'text': str_input}
        response = self.__create_request(self.endpoints['keywords_extraction'], json_input)
        if response.status_code != 200:
            return None
        return response.json()

    def sentence_similarity(self, sentences, sentence2, type_='sim', sem_type='lsa', document=False):
        json_input = {
            'text': sentences,
            'text2': sentence2,
            'types': type_,
            'sem_type': sem_type,
            'document': document
        }
        response = self.__create_request(self.endpoints['sentence_similarity'], json_input)
        if response.status_code != 200:
            return None
        return response.json()['similarity']

    def lemmatization(self, sentence):
        header = {
            'Content-Type' : 'application/json',
            'x-api-key': 'AabbbcgsFTHJH'
        }
        json_input = {
            'text' : sentence
        }
        response = requests.post(self.endpoints['lemma'], headers=header, json=json_input)
        if response.status_code != 200:
            return None
        sentences = response.json()['sentences']
        lemmas = []
        for sent in sentences:
            for token in sent['tokens']:
                lemmas.append(token['lemma'])
        return lemmas

    def pos_tag(self, str_input):
        self.headers['x-api-key'] = 'asdf'
        json_input = {'text': str_input}
        response = self.__create_request(self.endpoints['pos_tag'], json_input)
        if response.status_code != 200:
            return None
        sentences = response.json()['postags']
        retval = [elmt for sentence in sentences for elmt in sentence]
        del self.headers['x-api-key']
        return retval