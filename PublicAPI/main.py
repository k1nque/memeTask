from typing import Union, Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

from models import Base, db_helper

import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


class Meme(BaseModel):
    meme_id: Union[int, None]
    description: str
    # image: bytes


app = FastAPI(lifespan=lifespan)


@app.get("/")
def index():
    return "Hello, Memes!"


@app.get("/memes", response_model=list[Meme])
async def list_memes():
    pass


@app.get("/memes/{id}")
async def get_meme(id: int) -> Meme:
    pass


@app.post("/memes", response_model=int, response_description="Created meme ID")
async def create_meme(description: str) -> int:
    return 1


@app.put("/memes/{id}")
async def update_meme(id: int, q: Union[str, None] = None):
    pass


@app.delete("/memes/{id}")
async def delete_meme(id: int):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
