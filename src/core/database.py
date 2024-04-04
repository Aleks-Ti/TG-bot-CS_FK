import subprocess

from collections.abc import Callable

from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine as _create_async_engine
from src.core.connector_for_alembic_and_alchemy import DataBaseConfig as conf


def create_async_engine(url: URL | str) -> AsyncEngine:
    return _create_async_engine(url=url, echo=True, pool_pre_ping=True)


async_session_maker: Callable[..., AsyncSession] = sessionmaker(
    create_async_engine(conf().build_connection_str()), class_=AsyncSession, expire_on_commit=False
)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


async def migrate():
    subprocess.run("alembic upgrade head", shell=True, check=True)
