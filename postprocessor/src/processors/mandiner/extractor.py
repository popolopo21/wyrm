from __future__ import annotations

from typing import List
from bs4 import BeautifulSoup
from datetime import datetime
from models import Article


def extract_title(soup) -> str:
    title = soup.find("meta", {"property": "og:title"})
    title = title["content"].replace(" - Mandiner", "")
    return title.strip()


def extract_description(soup) -> str:
    description = soup.find("meta", {"name": "description"})
    return description["content"].strip()


def extract_authors(soup) -> List[str]:
    authors = soup.find_all("meta", {"name": "author"})
    if authors:
        return [author["content"].strip() for author in authors]
    else:
        return [""]


def extract_section(soup) -> str:
    section = soup.find("meta", {"name": "news_keywords"})
    if section:
        return section["content"].strip()
    return ""


# TODO: Make every tag first letter Uppercase
def extract_tags(soup) -> List[str]:
    tags = soup.find("meta", {"name": "keywords"})
    if tags:
        return [tag.strip() for tag in tags["content"].split()]
    else:
        return [""]


def extract_content_text(soup) -> str:
    return soup.find("div", class_="block-content").get_text()


def extract_a_published_at(soup) -> datetime:
    published_at = soup.find("meta", {"property": "article:published_time"})

    return datetime.fromisoformat(published_at["content"])


def extract_a_modified_at(soup) -> datetime:
    modified_at = soup.find("meta", {"property": "article:modified_time"})
    if modified_at:
        return datetime.fromisoformat(modified_at["content"])
    return None


def test_generate_article_from_html(html: str) -> Article:
    try:
        soup = BeautifulSoup(html, "html.parser")
        title = extract_title(soup)
        print(title)
        description = extract_description(soup)
        print(description)
        authors = extract_authors(soup)
        print(authors)
        section = extract_section(soup)
        print(section)
        tags = extract_tags(soup)
        print(tags)
        content_text = extract_content_text(soup)
        print(content_text)
        a_published_at = extract_a_published_at(soup)
        print(a_published_at)
        a_modified_at = extract_a_modified_at(soup)
        print(a_modified_at)
    except Exception as e:
        print(e)


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
