from lib import embeddings, client
from lib.queries.search_description_euclidean_async_edgeql import (
    search_description_euclidean,
)
import asyncio

text = "hazugság"

embedding = embeddings.embed_query(text)


async def main():
    result = await search_description_euclidean(executor=client, vector=embedding)
    for res in result:
        print(res.description)


asyncio.run(main())
