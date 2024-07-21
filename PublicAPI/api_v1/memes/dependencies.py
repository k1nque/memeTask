from typing import Annotated

from fastapi import Path, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Meme

from . import crud

async def meme_by_id(
    meme_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    meme = await crud.get_meme(session, meme_id)
    if meme is not None:
        return meme
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Meme {meme_id} is not found!"
    )


def get_pagination_params(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, gt=0)
):
    return {"offset": offset, "limit"   : limit}