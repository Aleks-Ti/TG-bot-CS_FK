from aiogram.types import Message
from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload

from src.core.database import async_session_maker
from src.games.models import BinaryConverter, GameProfile
from src.user.models import User
from src.user.user_query import get_or_create_user


async def word_in_binary_update(message: Message):
    async with async_session_maker() as session:
        try:
            user: User = await get_or_create_user(message)
            stmt_guess_number = (
                select(BinaryConverter)
                .options(
                    selectinload(BinaryConverter.game_profile),
                    selectinload(BinaryConverter.game_profile, GameProfile.user),
                )
                .where(GameProfile.user_id == user.id)
            )
            res_guess_number = (await session.execute(stmt_guess_number)).scalar_one_or_none()
            if res_guess_number:
                new_result = {
                    "total_try_convert_word_in_byte": BinaryConverter.total_try_convert_word_in_byte + 1,
                    "count_encrypted_word": BinaryConverter.count_encrypted_word + len(message.text.split(" ")),
                    "count_encrypted_characters": BinaryConverter.count_encrypted_characters + len(message.text),
                }
                stmt = update(BinaryConverter).where(BinaryConverter.game_profile_id == user.game_profile.id).values(**new_result)
                await session.execute(stmt)
                await session.commit()
            else:
                convert_result = {
                    "total_try_convert_word_in_byte": 1,
                    "count_encrypted_word": len(message.text.split(" ")),
                    "count_encrypted_characters": len(message.text),
                    "game_profile_id": user.game_profile.id,
                }
                stmt = insert(BinaryConverter).values(**convert_result)
                await session.execute(stmt)
                await session.commit()
        except Exception as err:
            print(err)


async def binary_in_word_update(message: Message):
    async with async_session_maker() as session:
        try:
            user: User = await get_or_create_user(message)
            stmt_bynary_converter = (
                select(BinaryConverter)
                .options(
                    selectinload(BinaryConverter.game_profile),
                    selectinload(BinaryConverter.game_profile, GameProfile.user),
                )
                .where(GameProfile.user_id == user.id)
            )
            stmt_bynary = (await session.execute(stmt_bynary_converter)).scalar_one_or_none()
            if stmt_bynary:
                new_result = {
                    "total_try_convert_byte_in_word": BinaryConverter.total_try_convert_word_in_byte + 1,
                    "number_decoded_word": BinaryConverter.count_encrypted_word + len(message.text.split(" ")),
                    "number_decoded_characters": BinaryConverter.count_encrypted_characters + len(message.text),
                }
                stmt = update(BinaryConverter).where(BinaryConverter.game_profile_id == user.game_profile.id).values(**new_result)
                await session.execute(stmt)
                await session.commit()
            else:
                convert_result = {
                    "total_try_convert_byte_in_word": 1,
                    "number_decoded_word": len(message.text.split(" ")),
                    "number_decoded_characters": len(message.text),
                    "game_profile_id": user.game_profile.id,
                }
                stmt = insert(BinaryConverter).values(**convert_result)
                await session.execute(stmt)
                await session.commit()
        except Exception as err:
            print(err)
