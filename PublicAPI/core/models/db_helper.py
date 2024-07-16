from asyncio import current_task
from dotenv import find_dotenv, load_dotenv
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession
)
import os

load_dotenv(find_dotenv())
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")

# POSTGRES_HOST = '0.0.0.0'
# POSTGRES_USERNAME = 'postgres'
# POSTGRES_PASSWORD = 'postgres'
# POSTGRES_PORT = '5432'


class DatabaseHelper:
    def __init__(self) -> None:
        self.engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}",
            echo=True,
            # future=True
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        return session
    
    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        session.close()


db_helper = DatabaseHelper()