# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from typing import Union, Optional, List
from datetime import datetime
from dataclasses import dataclass

@dataclass
class TelexhuArticle():
        url: str
        title: str
        author: str
        tags: str
        content_html: str
        content_text: Optional[str]
        content_text_embedding: Optional[List[float]]
        a_published_at: Union[str, datetime]
        a_modified_at: Union[str, datetime]
