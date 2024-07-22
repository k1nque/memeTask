from aiohttp import ClientSession

import os

URL = os.environ.get("PRIVATE_API_URL")
PORT = os.environ.get("PRIVATE_API_PORT")

async def delete_file(filename: str):
    async with ClientSession() as session:
        r = await session.delete(f"{URL}:{PORT}/memes/{filename}")
        return r.status