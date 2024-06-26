import logging

from aiogram.types import Message
from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload

from src.core.database import async_session_maker
from src.games.models import GameProfile, GuessNumber
from src.user.models import User
from src.user.user_query import get_or_create_user


async def guess_game_update(message: Message, count_attempts):
    async with async_session_maker() as session:
        try:
            user: User = await get_or_create_user(message)
            stmt_guess_number = (
                select(GuessNumber)
                .options(
                    selectinload(GuessNumber.game_profile),
                    selectinload(GuessNumber.game_profile, GameProfile.guess_number),
                ).join(GameProfile,  GameProfile.id == GuessNumber.game_profile_id, isouter=True)
                .where(GameProfile.user_id == user.id)
            )
            res_guess_number = (await session.execute(stmt_guess_number)).scalar_one_or_none()
            if res_guess_number:
                new_result = {"total_number_games": GuessNumber.total_number_games + 1}
                if res_guess_number.best_result > count_attempts:
                    new_result["best_result"] = count_attempts
                stmt = update(GuessNumber).where(GuessNumber.game_profile_id == user.game_profile.id).values(**new_result)
                await session.execute(stmt)
                await session.commit()
            else:
                game_result = {
                    "total_number_games": 1,
                    "best_result": count_attempts,
                    "game_profile_id": user.game_profile.id,
                }
                stmt = insert(GuessNumber).values(**game_result)
                await session.execute(stmt)
                await session.commit()
        except Exception as err:
            logging.exception(f"Error. {err}")
