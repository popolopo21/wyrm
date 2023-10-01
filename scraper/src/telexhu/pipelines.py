# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from typing import List
from datetime import datetime
from bs4 import BeautifulSoup

# useful for handling different item types with a single interface
from .items import Webpage
import edgedb
from .queries.create_webpage_async_edgeql import create_webpage
from loguru import logger

logger.add("out.log", backtrace=True, diagnose=True)

# class TelexhuPipeline:
#     @staticmethod
#     def clean_author(author: str) -> str:
#         return author.strip()

#     @staticmethod
#     def clean_title(title: str) -> str:
#         return title.strip()
#     @staticmethod
#     def clean_content(content: str) -> str:
#         return  BeautifulSoup(content).get_text()
#     @staticmethod
#     def clean_tags(tags: List[str]) -> List[str]:
#         return [tag.strip() for tag in tags]
#     @staticmethod
#     def clean_a_published_at(published_at: str) -> datetime:
#         # Map Hungarian month names to English
#         published_at = published_at.strip()
#         month_map = {
#             'január': 'January',
#             'február': 'February',
#             'március': 'March',
#             'április': 'April',
#             'május': 'May',
#             'június': 'June',
#             'július': 'July',
#             'augusztus': 'August',
#             'szeptember': 'September',
#             'október': 'October',
#             'november': 'November',
#             'december': 'December'
#         }

#         for hun_month, eng_month in month_map.items():
#             published_at = published_at.replace(hun_month, eng_month)

#         naive_dt = datetime.strptime(published_at, "%Y. %B %d. – %H:%M")
#         return naive_dt.replace(tzinfo=pytz.UTC)

#     @staticmethod
#     def clean_modified_at(modified_at: str) -> datetime:
#         return datetime.fromisoformat(modified_at)

#     @staticmethod
#     def clean_sitemap_date(modified_at: str) -> datetime:
#         return datetime.fromisoformat(modified_at)
#     def process_item(self, article: TelexhuArticle, spider) -> TelexhuArticle:
#         try:
#             article.title = self.clean_title(article.title)
#             article.author = self.clean_author(article.author)
#             article.tags = self.clean_tags(article.tags)
#             article.content_text = self.clean_content(article.content_html)
#             article.a_published_at = self.clean_a_published_at(article.a_published_at)
#             article.a_modified_at = self.clean_modified_at(article.a_modified_at)
#             article.sitemap_date = self.clean_sitemap_date(article.sitemap_date)
#         except Exception as e:
#             print(str(e) + '\n' * 10)
#         return article


class StoreWebpage:
    def __init__(self):
        self.client = edgedb.create_async_client()

    async def process_item(self, webpage: Webpage, spider) -> Webpage:
        try:
            await create_webpage(self.client, **webpage.model_dump())
            # print(webpage.model_dump())
        except Exception as e:
            logger.error(f"{e}")
