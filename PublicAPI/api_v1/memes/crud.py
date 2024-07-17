from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from .shemas import MemeCreate, MemeUpdate, MemeUpdatePartitial
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
    await session.refresh(meme)
    return meme


async def update_meme(
        session: AsyncSession,
        meme: Meme,
        meme_update: MemeUpdate | MemeUpdatePartitial,
        partial: bool = False,
) -> Meme:
    for name, value in meme_update.model_dump(exclude_unset=partial).items():
        setattr(meme, name, value)
    await session.commit()
    return meme


async def delete_meme(
        session: AsyncSession,
        meme: Meme
) -> None:
    await session.delete(meme)
    await session.commit()