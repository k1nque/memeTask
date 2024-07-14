from fastapi import FastAPI
from pydantic import BaseModel

class Meme(BaseModel):
    meme_id: int
    image: bytes
    description: str

app = FastAPI()


