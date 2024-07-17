from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.utils import deep_dict_update
from sqlalchemy.ext.asyncio import AsyncSession

from .shemas import Meme, MemeCreate, MemeUpdate, MemeUpdatePartitial
from .dependencies import meme_by_id

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
    meme: Meme = Depends(meme_by_id)
):
    return meme
    

@router.post("/", response_model=Meme)
async def create_meme(
    meme_in: MemeCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    meme: Meme = await crud.create_meme(session, meme_in)
    return meme


@router.put("/{meme_id}")
async def update_meme(
    meme_update: MemeUpdate,
    meme: Meme = Depends(meme_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.update_meme(
        session=session,
        meme=meme,
        meme_update=meme_update,
    )


@router.patch("/{meme_id}")
async def update_meme_partial(
    meme_update: MemeUpdatePartitial,
    meme: Meme = Depends(meme_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.update_meme(
        session=session,
        meme=meme,
        meme_update=meme_update,
        partial=True
    )


@router.delete("/{meme_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meme(
    meme: Meme = Depends(meme_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_meme(session=session, meme=meme)