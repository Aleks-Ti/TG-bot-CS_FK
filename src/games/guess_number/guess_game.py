from aiogram import types
import logging
from os import getenv
from random import choice, randint
import os
from aiogram import Bot, Dispatcher, types, F, Router
from dotenv import load_dotenv
import asyncio
import sys
from aiogram
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command,
from src.utils.buttons import MainKeyboard as mk
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from core.query_db import (
    create_user,
    game_data_update_users_profile,
    get_profile_users,
)
from aiogram.fsm.context import FSMContext
from src.games.guess_number.utils import word_declension
from src.games.guess_number.stiker import (
    COLD_STICKER_LIST,
    HOT_STICKER_LIST,
    NOT_STICKER_LIST,
    STICKER_ANGRY_HACKER,
    STICKER_FANNY_HACKER,
    WIN_STICKER_LIST,
)
from src.main import dp, bot

class GameCon:
    """Game conditions.

    Attributes:
        SECRETS_NUM_GAME: {user_id: Рандомное число от 0 до 100}.
        COUNT_ATTEMPTS: {user_id: Счетчик попыток одной игровой сессии}.
    """

    SECRETS_NUM_GAME = {}
    COUNT_ATTEMPTS = {}


class GamesState(StatesGroup):
    """Машина состояния.

    Ожидание пользовательского ввода guess game.
    """

    name = State()
    cancel = State()


@dp.message()
async def sticker_message(id, sticker, message: types.Message):
    """Возвращает рандомный стикер из списка."""
    await message.s(
        chat_id=id,
        sticker=choice(sticker),
    )


@dp.message_handler(state=GamesState.name)
async def guess_number(message: types.Message, state: FSMContext):
    """Отправка сообщения c результатом игры."""
    chat_id = message.from_user.id
    secret = GameCon.SECRETS_NUM_GAME[chat_id]
    try:
        value = int(message.text)
    except ValueError:
        value = ord(message.text[0])
    while True:
        GameCon.COUNT_ATTEMPTS[chat_id] += 1
        if 0 > value or value > 100:
            await sticker_message(chat_id, NOT_STICKER_LIST)
            await state.update_data(value=value)
            break
        if GameCon.COUNT_ATTEMPTS[chat_id] >= 30:
            await state.clear()
            await bot.send_message(
                chat_id=chat_id,
                text='##########'
                '### 30 попыток это максимум!\n'
                '### Число не найдено.\n'
                '### В следующий раз получиться!\n'
                '### Игра окончена.\n'
                '###########',
            )
            break
        if value > secret:
            await sticker_message(chat_id, HOT_STICKER_LIST)
            await state.update_data(value=value)
            break
        elif value < secret:
            await sticker_message(chat_id, COLD_STICKER_LIST)
            await state.update_data(value=value)
            break
        else:
            await sticker_message(chat_id, WIN_STICKER_LIST)
            await state.clear()
            await asyncio.sleep(1.5)
            count_attempts = GameCon.COUNT_ATTEMPTS.pop(chat_id)
            del GameCon.SECRETS_NUM_GAME[chat_id]
            create_user(message)
            game_data_update_users_profile(message, count_attempts)
            await bot.send_message(
                chat_id=chat_id,
                text='#######🎉🎉🎉\n'
                '### УРААА!!!\n### ПОБЕДА!\n'
                '### У тебя получилось угадать'
                ' за '
                + str(count_attempts)
                + ' '
                + word_declension(count_attempts)
                + '\n'
                '### 🎊 Внушительный результат!!!\n'
                '### Игра окончена! \n'
                '########🎉🎉🎉',
            )
            break


@dp.message_handler(commands=['game_guess_number'])
async def info_game_number(message: types.Message):
    """Пользовательский ввод и состояние для игры."""
    await GamesState.name.set()
    identifier_user = message.from_user.id
    secret = randint(0, 100)
    GameCon.COUNT_ATTEMPTS[identifier_user] = 0
    GameCon.SECRETS_NUM_GAME[identifier_user] = secret
    await message.reply(
        '###########\n'
        '### Угадай ЧИСЛО!\n'
        '### Правила просты!\n'
        '#### Число может быть от 0 до 100.\n'
        '### Если введешь не число,\n'
        '#### оно конвертируется в число из таблицы utf-8\n'
        '##### и ты ошибешься! 😝\n'
        '### Если твое число больше загаднного, то я подскажу -'
        ' горячо и нужно искать в меньших числах,\n'
        '#### если же твое число меньше загаднного, то подскажу, '
        'что холодно и значит загаданное число выше.\n'
        '##### а если вне диапазона?! ...\n'
        '### У тебя есть 30 попыток!\n'
        '### Вперед друг, к победе!!!\n'
        '###########'
    )
