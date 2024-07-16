from fastapi import APIRouter

from .memes.views import router as memes_router

router = APIRouter()

router.include_router(memes_router, prefix="/memes")