import os

from aiohttp import ClientSession
from json import loads

URL = os.environ.get("PRIVATE_API_URL")
PORT = os.environ.get("PRIVATE_API_PORT")

async def download_file(filename: str) -> bytes | None:
    async with ClientSession() as session:
        r = await session.get(f"{URL}:{PORT}/memes/file/{filename}")
        contents = await r.text()
        link = loads(contents)["link"]

        r = await session.get(f"{URL}:{PORT}{link}")
        if r.status == 200:
            return await r.content.read()
        else:
            return None