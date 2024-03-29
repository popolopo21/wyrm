from __future__ import annotations

from typing import List
from bs4 import BeautifulSoup
from datetime import datetime
from models import Article


def extract_title(soup) -> str:
    title = soup.find("meta", {"property": "og:title"})
    return title["content"].strip()


def extract_description(soup) -> str:
    description = soup.find("meta", {"property": "og:description"})
    return description["content"].strip()


def extract_authors(soup) -> List[str]:
    authors = soup.find_all("meta", {"name": "article:author"})
    return [author["content"].strip() for author in authors]


def extract_section(soup) -> str:
    section = soup.find("meta", {"name": "article:section"})
    return section["content"].strip()


# TODO: Make every tag first letter Uppercase
def extract_tags(soup) -> List[str]:
    tags = soup.find_all("meta", {"name": "article:tag"})
    return [tag["content"].strip() for tag in tags]


def extract_content_text(soup) -> str:
    return soup.find("div", class_="article-html-content").get_text()


def extract_a_published_at(soup) -> datetime:
    published_at = soup.find("meta", {"name": "article:published_time"})
    return datetime.fromisoformat(published_at["content"])


def extract_a_modified_at(soup) -> datetime:
    modified_at = soup.find("meta", {"name": "article:modified_time"})
    if modified_at:
        return datetime.fromisoformat(modified_at["content"])
    return None


def generate_article_from_html(html: str) -> Article:
    soup = BeautifulSoup(html, "html.parser")
    return Article(
        title=extract_title(soup),
        description=extract_description(soup),
        authors=extract_authors(soup),
        section=extract_section(soup),
        tags=extract_tags(soup),
        content_text=extract_content_text(soup),
        a_published_at=extract_a_published_at(soup),
        a_modified_at=extract_a_modified_at(soup),
    )
