from datetime import datetime, UTC

from sqlalchemy import insert, update, delete, select
from sqlalchemy.orm import selectinload

from src.core.database import async_session_maker
from src.user.models import User
from src.games.models import GameProfile, GameProfileHaortPyramid, GuessNumber, HaortPyramid, BinaryConverter
from aiogram.types import Message


async def create_user(message: Message):
    async with async_session_maker() as session:
        stmt = select(User).where(message.from_user.id == User.tg_user_id)
        res = (await session.execute(stmt)).scalar_one_or_none()
        if res:
            return res
        else:
            user_data = {
                "username": message.from_user.full_name,
                "tg_user_id": message.from_user.id,
                "first_name": message.from_user.first_name,
                "last_name": message.from_user.last_name
            }
            stmt_user = insert(User).values(**user_data).returning(User)
            res_user = await session.execute(stmt_user)
            await session.flush()
            user = res_user.scalar_one()
            stmt_game_profile = insert(GameProfile).values({"user_id": user.id})
            await session.execute(stmt_game_profile)
            await session.commit()


async def get_profile_users(message: Message):
    try:
        async with async_session_maker() as session:
            stmt_user = (
                select(User).where(message.from_user.id == User.tg_user_id)
            )
            res_user = (await session.execute(stmt_user)).scalar_one_or_none()
            if not res_user:
                res_user = await create_user(message)
            stmt_game_profile = (
                select(GameProfile).where(GameProfile.user_id == res_user.id)
                .options(
                    selectinload(GameProfile.binary_converter),
                    selectinload(GameProfile.guess_number),
                    selectinload(GameProfile.game_profile_haort_pyramid)
                    # .options(selectinload(GameProfileHaortPyramid.haort_pyramid)),
                )
            )
            res = await session.execute(stmt_game_profile)
            return res.scalar_one()
    except Exception as err:
        print(err)
