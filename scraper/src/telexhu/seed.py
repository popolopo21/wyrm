from queries.create_website_async_edgeql import create_website
import edgedb
import asyncio

websites = ['telex.hu', '444.hu']

client = edgedb.create_async_client()

async def main():
    tasks = []
    for website in websites:
        task = asyncio.create_task(create_website(client,domain=website))
        tasks.append(task)
    await asyncio.gather(*tasks)
    
    
if __name__ == '__main__':
    asyncio.run(main())
