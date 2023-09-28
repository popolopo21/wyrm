# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from typing import Union, Optional, List, Dict
from datetime import datetime
import dataclasses
from dataclasses import dataclass
from urllib.parse import urlparse

@dataclass
class TelexhuArticle():
        url: str
        title: str
        author: str
        tags: str
        content_html: str
        content_text: Optional[str]
        content_text_embedding: Optional[List[float]]
        sitemap_date: datetime
        a_published_at: Union[str, datetime]
        a_modified_at: Union[str, datetime]

        @property
        def domain(self):
                return urlparse(self.url).hostname
        
        
        def to_dict(self) -> Dict:
                return dataclasses.asdict(self)