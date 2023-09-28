# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from typing import List
from datetime import datetime
from bs4 import BeautifulSoup
# useful for handling different item types with a single interface
from telexhu.items import TelexhuArticle
from langchain.embeddings.openai import OpenAIEmbeddings
import edgedb

openai_api_key = ""

class TelexhuPipeline:
    @staticmethod
    def clean_author(author: str) -> str:
        return author.strip()
    
    @staticmethod
    def clean_title(title: str) -> str:
        return title.strip()
    @staticmethod
    def clean_content(content: str) -> str:
        return  BeautifulSoup(content).get_text()
    @staticmethod
    def clean_tags(tags: List[str]) -> List[str]:
        return [tag.strip() for tag in tags]
    @staticmethod
    def clean_a_published_at(published_at: str) -> datetime:
        # Map Hungarian month names to English
        published_at = published_at.strip()
        month_map = {
            'január': 'January',
            'február': 'February',
            'március': 'March',
            'április': 'April',
            'május': 'May',
            'június': 'June',
            'július': 'July',
            'augusztus': 'August',
            'szeptember': 'September',
            'október': 'October',
            'november': 'November',
            'december': 'December'
        }

        for hun_month, eng_month in month_map.items():
            published_at = published_at.replace(hun_month, eng_month)

        return datetime.strptime(published_at, "%Y. %B %d. – %H:%M")
    
    @staticmethod
    def clean_modified_at(modified_at: str) -> datetime:
        return datetime.fromisoformat(modified_at)
    
    def process_item(self, article: TelexhuArticle, spider) -> TelexhuArticle:
        try:
            article.title = self.clean_title(article.title)
            article.author = self.clean_author(article.author)
            article.tags = self.clean_tags(article.tags)
            article.content_text = self.clean_content(article.content_html)
            article.a_published_at = self.clean_a_published_at(article.a_published_at)
            article.a_modified_at = self.clean_modified_at(article.a_modified_at)
        except Exception as e:
            print(str(e) + '\n' * 10)
        return article


embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

class StoreArticlePipeline:
        def __init__(self):
            self.client = edgedb.create_client()

        def process_item(self, article: TelexhuArticle, spider) -> TelexhuArticle:
            pass