from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .shemas import Meme, MemeCreate

from . import crud
from core.models import db_helper


router = APIRouter(tags=["Memes"])


@router.get("/", response_model=list[Meme])
async def get_memes(
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    memes: list[Meme] = await crud.get_memes(session=session)
    return memes


@router.get("/{meme_id}", response_model=Meme)
async def get_meme(
    meme_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    meme = await crud.get_meme(session, meme_id)
    if meme is not None:
        return meme
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Meme {meme_id} is not found!"
    )



@router.post("/", response_model=Meme)
async def create_meme(
    meme_in: MemeCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    meme: Meme = await crud.create_meme(session, meme_in)
    return meme

