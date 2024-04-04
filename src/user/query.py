from datetime import datetime, UTC

from sqlalchemy import insert, update, delete, select

from src.core.database import async_session_maker
from src.user.models import User
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
            stmt = insert(User).values(**user_data)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()
