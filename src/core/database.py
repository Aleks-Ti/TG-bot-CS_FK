from collections.abc import Callable

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.connector_for_alembic_and_alchemy import DataBaseConfig as conf


def create_async_engine(url: URL | str) -> AsyncEngine:
    return _create_async_engine(url=url, echo=False, pool_pre_ping=True)


async_session_maker: Callable[..., AsyncSession] = sessionmaker(
    create_async_engine(conf().build_connection_str()), class_=AsyncSession, expire_on_commit=False,
)
