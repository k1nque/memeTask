from typing import Union, Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

from core.models import Base, db_helper
from api_v1 import router

import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router)


@app.get("/")
def index():
    return "Hello, Memes!"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
