import asyncio
from random import choice, randint

from aiogram import types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from src.games.guess_number.utils import word_declension
from src.games.guess_query import guess_game_update
from src.state_machine import GuessGamesState
from src.utils.find_nearest_numbers import hint_number
from src.utils.stikers import (
    COLD_STICKER_LIST,
    HOT_STICKER_LIST,
    NOT_STICKER_LIST,
    WIN_STICKER_LIST,
)


class GameCondition:
    """Game conditions.

    Attributes:
        SECRETS_NUM_GAME: {user_id: Рандомное число от 0 до 100}.
        COUNT_ATTEMPTS: {user_id: Счетчик попыток одной игровой сессии}.
    """
    def __init__(self) -> None:
        # self.unique_id = str(uuid.uuid4())
        self.SECRETS_NUM_GAME = None
        self.COUNT_ATTEMPTS = 0
        self.ALL_USER_CHOICE_NUMBER = []
        self.LAST_MESSAGE_WITH_STICKER = None


async def sticker_message(message: types.Message, sticker: list[str], game_session: GameCondition | None = None):
    """Возвращает рандомный стикер из списка."""
    if game_session:
        all_number = [str(num) for num in game_session.ALL_USER_CHOICE_NUMBER]
        hint = await hint_number(game_session.ALL_USER_CHOICE_NUMBER, game_session.SECRETS_NUM_GAME)
        info_message_for_user = "Все ваши догадки: " + " \\| ".join(all_number) + "\n\nПодсказка: " + "||попробуй " + hint + "||"
        await message.answer(text=info_message_for_user, parse_mode=ParseMode.MARKDOWN_V2)
        await message.answer_sticker(
            sticker=choice(sticker),
        )
    else:
        await message.answer_sticker(
            sticker=choice(sticker),
        )


async def guess_number(message: types.Message, state: FSMContext):
    """Отправка сообщения c результатом игры."""
    state_data = await state.get_data()
    game_session: GameCondition = state_data["guess_game_session"]
    secret = game_session.SECRETS_NUM_GAME

    try:
        user_choice_number = int(message.text)
    except ValueError:
        user_choice_number = ord(message.text[0])

    game_session.ALL_USER_CHOICE_NUMBER.append(user_choice_number)
    game_session.COUNT_ATTEMPTS += 1

    if 0 > user_choice_number or user_choice_number > 100:
        await sticker_message(message, NOT_STICKER_LIST, game_session)
        return None
    if game_session.COUNT_ATTEMPTS >= 30:
        await state.clear()
        await message.answer(
            text="##########"
            "### 30 попыток это максимум!\n"
            "### Число не найдено.\n"
            "### В следующий раз получиться!\n"
            "### Игра окончена.\n"
            "###########",
        )
        return None
    if user_choice_number > secret:
        await sticker_message(message, HOT_STICKER_LIST, game_session)
        await message.delete()
        return None
    elif user_choice_number < secret:
        await sticker_message(message, COLD_STICKER_LIST, game_session)
        await message.delete()
        return None
    else:
        await sticker_message(message, WIN_STICKER_LIST)
        await state.clear()
        await asyncio.sleep(1.5)
        await guess_game_update(message, game_session.COUNT_ATTEMPTS)
        await message.answer(
            text="#######🎉🎉🎉\n"
            "### УРААА!!!\n### ПОБЕДА!\n"
            "### У тебя получилось угадать"
            " за "
            + str(game_session.COUNT_ATTEMPTS)
            + " "
            + word_declension(game_session.COUNT_ATTEMPTS)
            + "\n"
            "### 🎊 Внушительный результат!!!\n"
            "### Игра окончена! \n"
            "########🎉🎉🎉",
        )
        await message.delete()
        return None


async def info_game_number(message: types.Message, state: FSMContext, games_state: GuessGamesState):
    """Пользовательский ввод и состояние для игры."""
    await state.clear()
    await state.set_state(games_state.name)
    secret = randint(0, 100)
    guess_game_session_obj = GameCondition()
    guess_game_session_obj.SECRETS_NUM_GAME = secret
    await state.update_data(guess_game_session=guess_game_session_obj)
    await message.answer(
        "###########\n"
        "### Угадай ЧИСЛО!\n"
        "### Правила просты!\n"
        "#### Число может быть от 0 до 100.\n"
        "### Если введешь не число,\n"
        "#### оно конвертируется в число из таблицы utf-8\n"
        "##### и ты ошибешься! 😝\n"
        "### Если твое число больше загаднного, то я подскажу -"
        " горячо и нужно искать в меньших числах,\n"
        "#### если же твое число меньше загаданного, то подскажу, "
        "что холодно и значит загаданное число выше.\n"
        "##### а если вне диапазона?! ...\n"
        "### У тебя есть 30 попыток!\n"
        "### Вперед друг, к победе!!!\n"
        "###########",
    )
