from processors.mandiner.process import process_mandiner
from processors.telex.process import process_telex
from processors.index.process import process_index

import asyncio


async def main():
    print("process mandiner started")
    await process_mandiner()
    print("process telex started")
    await process_telex()
    print("process index started")
    await process_index()


asyncio.run(main())
