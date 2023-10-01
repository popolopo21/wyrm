import asyncio
from bs4 import BeautifulSoup
from typing import List
from tqdm import tqdm
from loguru import logger
from queries.get_articles_without_title_embeddings_async_edgeql import (
    get_articles_without_title_embeddings,
)
from queries.get_articles_without_desc_embeddings_async_edgeql import (
    get_articles_without_desc_embeddings,
)
from queries.update_article_desc_embedding_async_edgeql import (
    update_article_desc_embedding,
)
from queries.update_article_title_embedding_async_edgeql import (
    update_article_title_embedding,
)
from queries.get_unprocessed_webpages_async_edgeql import get_unprocessed_webpages
from queries.create_article_async_edgeql import create_article

from common import client, embeddings
from telex.extractor import generate_article_from_html

logger.add("out.log", backtrace=True, diagnose=True)

domain = "https://telex.hu"


async def create_articles():
    webpages = await get_unprocessed_webpages(client, domain=domain)
    for webpage in webpages:
        try:
            article = generate_article_from_html(webpage.html)
            article.webpage_id = webpage.id
            article.title_embedding = [float(0) for i in range(1024)]
            article.description_embedding = [float(0) for i in range(1024)]
            if article.a_modified_at is None:
                article.a_modified_at = article.a_published_at
            await create_article(client, **article.model_dump())
        except Exception as exception:
            raise Exception(
                f"Error while generating article:{webpage.path}: {exception}"
            )


async def generate_embeddings():
    articles_wo_title = await get_articles_without_title_embeddings(
        client, domain=domain
    )
    articles_wo_desc = await get_articles_without_desc_embeddings(client, domain=domain)
    for article in tqdm(articles_wo_title):
        try:
            embedding_title = embeddings.embed_query(article.title)
            title_embedding_data = {
                "uuid": article.id,
                "title_embedding": embedding_title,
            }
            await update_article_title_embedding(client, **title_embedding_data)
        except Exception as exception:
            logger.error(
                f"Error while generating title embedding:{article.webpage.path}: {exception}"
            )

    for article in tqdm(articles_wo_desc):
        try:
            embedding_desc = embeddings.embed_query(article.description)

            description_embedding_data = {
                "uuid": article.id,
                "description_embedding": embedding_desc,
            }
            await update_article_desc_embedding(client, **description_embedding_data)
        except Exception as exception:
            logger.error(
                f"Error while generating description embedding:{article.webpage.path}: {exception}"
            )


async def process_telex():
    await create_articles()
    await generate_embeddings()
