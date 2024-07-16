from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from .shemas import MemeCreate
from core.models import Meme


async def get_memes(session: AsyncSession) -> list[Meme]:
    statement = select(Meme).order_by(Meme.id)
    result: Result = await session.execute(statement)
    memes = result.scalars().all()
    return list(memes)


async def get_meme(session: AsyncSession, meme_id: int) -> Meme | None:
    return await session.get(Meme, meme_id)


async def create_meme(session: AsyncSession, meme_in: MemeCreate):
    print(meme_in)
    meme = Meme(**meme_in.model_dump())
    session.add(meme)
    await session.commit()
    print(meme.id)
    await session.refresh(meme)
    return meme