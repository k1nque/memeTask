import os

from aiohttp import ClientSession, FormData

URL = os.environ.get("PRIVATE_API_URL")
PORT = os.environ.get("PRIVATE_API_PORT")

async def upload_file(file: bytes, filename: str) -> int:
    async with ClientSession() as session:
        data = FormData()
        
        extension = filename.split('.')[-1]

        if extension == "jpg" or extension == "jpeg":
            content_type = "image/jpeg"
        elif extension == "png":
            content_type = "image/png"
        else:
            content_type = "application/octet-stream"

        data.add_field(
            name="file",
            value=file,
            filename=filename,
            content_type=content_type,
        )

        async with session.post(
            f"{URL}:{PORT}/memes",
            data=data,
            headers={
                "accept": "application/json",
            }, 
            ssl=False,
        ) as response:
            status = response.status
            body = await response.json()

            return status