from aiogram import types
from src.games.haort_pyramid.haort_query import get_all_result_game_by_difficulty
from src.games.models import HaortPyramid


async def parse_records_data(records: list[HaortPyramid]):
    text = ""
    for index, record in enumerate(records):
        text += (
            f"{index + 1}. {record.game_profile.user.username} - лучший рузультат "
            f"- {record.total_number_permutations} - всего сыграно игр - {record.total_number_games}\n"
        )
    return text


async def records_haort_game_by_game_difficulty(callback_query: types.CallbackQuery, game_difficulty: int):
    records = await get_all_result_game_by_difficulty(game_difficulty)
    if records:
        text = await parse_records_data(records)
        text = "<pre>" + text + "</pre>"
        await callback_query.message.answer(text=text)

    else:
        await callback_query.message.answer("В этой сложности нет рекордов. Можете поставить первый рекорд?!")