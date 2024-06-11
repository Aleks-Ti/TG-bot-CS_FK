import json
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload

from src.core.database import async_session_maker
from src.games.models import GameProfile, HaortPyramid
from src.user.models import User
from src.user.user_query import get_or_create_user


async def get_dict_and_encode_values_stack(state_dict: dict):
    result = {}
    for key, value in state_dict.items():
        result[key] = json.loads(state_dict[value])
    return result


async def get_dict_and_decode_values_stack(state_dict: dict):
    result = {}
    for key, value in state_dict.items():
        result[key] = json.loads(state_dict[value])
    return result


async def update_or_create_haort_game(message: Message, state: FSMContext) -> None:
    state_game = await state.get_data()
    game_difficulty: int = state_game["game_difficulty"]
    count_permutations: int = state_game["number_of_permutations"]
    state_of_play: dict = state_game["towers_condition"]
    state_of_play_json = json.dumps({key: value.to_dict() for key, value in state_of_play.items()})
    user: User = await get_or_create_user(message)
    async with async_session_maker() as session:
        try:
            stmt_haort_game = (
                select(HaortPyramid)
                .options(selectinload(HaortPyramid.game_profile))
                .where(
                    HaortPyramid.game_profile_id == user.game_profile.id,
                    HaortPyramid.game_difficulty == game_difficulty,
                )
            )
            haort_game = (await session.execute(stmt_haort_game)).scalar_one_or_none()
            if haort_game is None:
                new_haort_game = (
                    insert(HaortPyramid)
                    .values(
                        {
                            "game_difficulty": game_difficulty,
                            "game_profile_id": user.game_profile.id,
                            "best_result": state_of_play_json,
                            "total_number_permutations": count_permutations,
                            "total_number_games": 1,
                        },
                    )
                )
                await session.execute(new_haort_game)
                await session.commit()
            elif haort_game.total_number_permutations > count_permutations:
                stmt = (
                    update(HaortPyramid)
                    .where(HaortPyramid.id == haort_game.id)
                    .values(
                        {
                            "best_result": state_of_play_json,
                            "total_number_permutations": count_permutations,
                            "total_number_games": HaortPyramid.total_number_games + 1,
                        },
                    )
                )
                await session.execute(stmt)
                await session.commit()
            else:
                stmt = (
                    update(HaortPyramid)
                    .where(HaortPyramid.id == haort_game.id)
                    .values(
                        {
                            "total_number_games": HaortPyramid.total_number_games + 1,
                        },
                    )
                )
                await session.execute(stmt)
                await session.commit()
                return None

        except Exception as err:
            logging.exception(f"Error. {err}")


async def get_win_game_by_difficulty(message: Message, game_difficulty: int) -> HaortPyramid:
    user: User = await get_or_create_user(message)
    async with async_session_maker() as session:
        try:
            subquery = select(GameProfile.id).where(GameProfile.user_id == user.id).scalar_subquery()
            stmt = (
                select(HaortPyramid)
                .where(
                    HaortPyramid.game_profile_id == subquery,
                    HaortPyramid.game_difficulty == game_difficulty,
                )
            )
            res = await session.execute(stmt)
            return res.scalar_one()

        except Exception as err:
            logging.exception(f"Error. {err}")
