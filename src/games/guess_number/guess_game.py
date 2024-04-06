import asyncio
from random import choice, randint

from aiogram import types
from aiogram.fsm.context import FSMContext

from src.games.guess_number.utils import word_declension
from src.games.guess_query import guess_game_update
from src.utils.stikers import (
    COLD_STICKER_LIST,
    HOT_STICKER_LIST,
    NOT_STICKER_LIST,
    WIN_STICKER_LIST,
)


class GameCon:
    """Game conditions.

    Attributes:
        SECRETS_NUM_GAME: {user_id: Рандомное число от 0 до 100}.
        COUNT_ATTEMPTS: {user_id: Счетчик попыток одной игровой сессии}.
    """

    SECRETS_NUM_GAME = {}
    COUNT_ATTEMPTS = {}
    LAST_MESSAGE = {}


async def sticker_message(message: types.Message, sticker):
    """Возвращает рандомный стикер из списка."""
    res = await message.answer_sticker(
        sticker=choice(sticker),
    )
    return res


async def guess_number(message: types.Message, state: FSMContext):
    """Отправка сообщения c результатом игры."""
    identifier_user = message.from_user.id
    game_session = GameCon()
    secret = game_session.SECRETS_NUM_GAME[identifier_user]
    try:
        value = int(message.text)
    except ValueError:
        value = ord(message.text[0])
    game_session.COUNT_ATTEMPTS[identifier_user] += 1
    if 0 > value or value > 100:
        await sticker_message(message, NOT_STICKER_LIST)
        await state.update_data(value=value)
        return
    if game_session.COUNT_ATTEMPTS[identifier_user] >= 30:
        await state.clear()
        await message.answer(
            text="##########"
            "### 30 попыток это максимум!\n"
            "### Число не найдено.\n"
            "### В следующий раз получиться!\n"
            "### Игра окончена.\n"
            "###########",
        )
        return
    if value > secret:
        await sticker_message(message, HOT_STICKER_LIST)
        await state.update_data(value=value)
        return
    elif value < secret:
        await sticker_message(message, COLD_STICKER_LIST)
        await state.update_data(value=value)
        return
    else:
        await sticker_message(message, WIN_STICKER_LIST)
        await state.clear()
        await asyncio.sleep(1.5)
        count_attempts = game_session.COUNT_ATTEMPTS.pop(identifier_user)
        del game_session.SECRETS_NUM_GAME[identifier_user]
        # await create_user(message)
        await guess_game_update(message, count_attempts)
        await message.answer(
            text="#######🎉🎉🎉\n"
            "### УРААА!!!\n### ПОБЕДА!\n"
            "### У тебя получилось угадать"
            " за "
            + str(count_attempts)
            + " "
            + word_declension(count_attempts)
            + "\n"
            "### 🎊 Внушительный результат!!!\n"
            "### Игра окончена! \n"
            "########🎉🎉🎉",
        )
        return


async def info_game_number(message: types.Message, state: FSMContext, games_state):
    """Пользовательский ввод и состояние для игры."""
    await state.set_state(games_state.name)
    identifier_user = message.from_user.id
    secret = randint(0, 100)
    game_session = GameCon()
    game_session.COUNT_ATTEMPTS[identifier_user] = 0
    game_session.SECRETS_NUM_GAME[identifier_user] = secret
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
        "#### если же твое число меньше загаднного, то подскажу, "
        "что холодно и значит загаданное число выше.\n"
        "##### а если вне диапазона?! ...\n"
        "### У тебя есть 30 попыток!\n"
        "### Вперед друг, к победе!!!\n"
        "###########",
    )
