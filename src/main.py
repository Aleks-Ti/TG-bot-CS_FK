import logging
from os import getenv
from random import choice, randint
import os
from aiogram import Bot, Dispatcher, types, F, Router
from dotenv import load_dotenv
import asyncio
import sys
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command
from src.utils.buttons import MainKeyboard as mk
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from src.user.query import (
    create_user,
)
from src.games.guess_number.guess_game import GameCon, GamesState, guess_number as _guess_number
from src.games.guess_number.guess_game import info_game_number
from aiogram.fsm.context import FSMContext
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename=os.path.join(os.path.dirname(__file__), 'program.log'),
    encoding='utf-8',
)

dp = Dispatcher()

TELEGRAM_TOKEN = getenv('TOKEN')
TELEGRAM_CHAT_ID = getenv('CHAT_ID')

RETRY_PERIOD = 10  # Период обращения


class ByteState(StatesGroup):
    """Машина состояния.

    Ожидание пользовательского ввода для конвертации в байт код.
    """

    name = State()
    cancel = State()


class ConvertState(StatesGroup):
    """Машина состояния.

    Ожидание пользовательского ввода для конвертации байт кода в utf-8.
    """

    name = State()
    cancel = State()


@dp.message(Command("cancel"))
@dp.message((F.text.casefold() == mk.cancel) | (F.text == mk.cancel))
async def cancel_handler(message: types.Message, state):
    """Обработчик команды отмены."""
    current_state = await state.get_state()
    if current_state is not None:
        logging.info('Cancelling state %r', current_state)
        await state()
        await message.answer('Операция отменена.')
    else:
        await message.answer('Нет активных операций для отмены.')


# @dp.message()
async def byte_message(message: Message):
    """Пользовательский ввод и состояние для конвертации."""
    await ByteState.name.set()
    await message.reply(
        'Введите ваше слово или имя, для конвертации '
        'в двоичный код 🦾'
    )


# @dp.message()
async def transcript(message: Message):
    """Пользовательский ввод и состояние для дешифрации."""
    await ConvertState.name.set()
    await message.reply('Введите двоичный код 📟 для дешифрации___ ')


# start guess game


@dp.message((F.text == mk.GAMES_GUESS_NUMBER))
async def start_guess_game(message: Message):
    await info_game_number(message)


# @dp.message(GamesState.name)
async def guess_number(message: types.Message, state: FSMContext):
    await _guess_number(message, state)
# end guess game


# @dp.message()
async def profile_user(message: Message):
    get_user = await get_profile_users(message)
    await bot.send_message(chat_id=message.from_user.id, text=get_user)


@dp.message(CommandStart())
async def send_welcome(message: Message):
    """
    Вызывается в случаем получения команды `/start`

    methods:
        create_user - создания юзера и занесения в базу данных.
    """

    try:
        await create_user(message)
    except Exception as err:
        print(err)
    button_1 = types.KeyboardButton(text=mk.CONVERT_WORD_IN_BINARY_CODE)
    button_2 = types.KeyboardButton(text=mk.CONVERT_BINARY_CODE_IN_WORD)
    button_3 = types.KeyboardButton(text=mk.GAMES_GUESS_NUMBER)
    button_4 = types.KeyboardButton(text=mk.ME_PROFILE)
    button_5 = types.KeyboardButton(text=mk.cancel)
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
                    [button_1], [button_2], [button_3], [button_4], [button_5],
                ],
        resize_keyboard=True,
    )
    await message.reply(
        'Привет!\nХочешь увидеть, как выглядит любой символ, '
        'или мб твоё имя в байтовом представлении?! - жми -> /byte\n'
        'Если нужно конвертировать машинный код в слова или буквы, '
        'то жми -> /transcript\n'
        'А может сыграем в игру Угадай число? - жми -> /numbers_game\n'
        'Или жми кнопки внизу 👇👇👇',
        reply_markup=keyboard,
    )


async def main(bot) -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    bot = Bot(TELEGRAM_TOKEN, default=ParseMode.HTML)
    try:
        print("поехали")
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main(bot))
    except KeyboardInterrupt:
        pass
    except Exception as err:
        logging.exception(f"Error. {err}")
