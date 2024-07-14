from dotenv import find_dotenv, load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import os

load_dotenv(find_dotenv())
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")


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


db_helper = DatabaseHelper()