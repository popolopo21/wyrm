from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class Article(BaseModel):
    title: str
    description: str
    authors: List[str]
    section: str
    tags: List[str]
    content_text: str
    title_embedding: Optional[List[float]] = None
    description_embedding: Optional[List[float]] = None
    a_published_at: datetime
    a_modified_at: Optional[datetime] = None
    webpage_id: Optional[UUID] = None
