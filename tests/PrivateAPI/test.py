import asyncio
import requests as req
import aiofiles

from aiohttp import ClientSession
from json import loads, dumps

filename = "22_16331.xls"
URL = "http://127.0.0.1"
PORT = "8001"


# r = req.get(f"{URL}:{PORT}/memes/file/{filename}")
# print(r.content)
# contents = loads(r.text)
# link = contents["link"]

# r = req.get(f"{URL}:{PORT}/{link}")
# print(r.status_code)
# if r.status_code == 200:
#     with open(filename, "wb") as f:
#         f.write(r.content)

async def download_file():
    async with ClientSession() as session:
        r = await session.get(f"{URL}:{PORT}/memes/file/{filename}")
        contents = await r.text()
        link = loads(contents)["link"]

        r = await session.get(f"{URL}:{PORT}{link}")
        if r.status == 200:
            async with aiofiles.open(filename, "wb") as f:
                await f.write(await r.content.read())


if __name__ == "__main__":
    asyncio.run(download_file())