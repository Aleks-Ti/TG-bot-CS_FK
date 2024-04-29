import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from src.core.base import metadata
from alembic import context
from src.core.connector_for_alembic_and_alchemy import DataBaseConfig
from src.user.models import (   # noqa
    User,
)
from src.games.models import (   # noqa
    GameProfile,
    HaortPyramid,
    BinaryConverter,
    GuessNumber,
)


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

### MY SETTINGS # noqa
DATABASE_URL = DataBaseConfig().build_connection_str()
target_metadata = metadata
config.set_main_option("sqlalchemy.url", DATABASE_URL)
### END MY SETTINGS # noqa


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
