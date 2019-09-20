import os
import json
import requests

from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

from helper.news_parser_helper import NewsContentParser

if __name__ == "__main__":
    url = 'https://www.tribunnews.com/regional/2019/08/19/dugaan-penyebab-kerusuhan-di-manokwari-papua-diawali-sikap-rasisme-ke-mahasiswa-papua-di-surabaya'
    html = requests.get(url).content
    parser = NewsContentParser(html, url)
    result = parser.parse_content()

    print(result['parsed_content'])
    