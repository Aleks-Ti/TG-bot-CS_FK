import asyncio
import logging
import os
import sys
from os import getenv

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from dotenv import load_dotenv

from src.games.binary_converter.converter import transcript_byte as _transcript_byte
from src.games.binary_converter.converter import transcript_word as _transcript_word
from src.games.guess_number.guess_game import guess_number as _guess_number
from src.games.guess_number.guess_game import info_game_number
from src.user.user_query import get_or_create_user, get_profile_users
from src.utils.buttons import MainKeyboard as mk
from src.utils.buttons import ProfileInlineKeyboard as pic

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(funcName)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename=os.path.join(os.path.dirname(__file__), "program.log"),
    encoding="utf-8",
)

dp = Dispatcher()

TELEGRAM_TOKEN = getenv("TOKEN")
TELEGRAM_CHAT_ID = getenv("CHAT_ID")

RETRY_PERIOD = 10  # Период обращения


class GuessGamesState(StatesGroup):
    """Guess game.
    Ожидание пользовательского ввода guess game.
    """

    name = State()
    cancel = State()


class ByteInWordState(StatesGroup):
    """Машина состояния.

    Ожидание пользовательского ввода для конвертации в байт код.
    """

    name = State()
    cancel = State()


class WordInByteState(StatesGroup):
    """Машина состояния.

    Ожидание пользовательского ввода для конвертации байт кода в utf-8.
    """

    name = State()
    cancel = State()


@dp.message(Command("cancel"))
@dp.message((F.text.casefold() == mk.cancel) | (F.text == mk.cancel))
async def cancel_handler(message: types.Message, state: FSMContext):
    """Обработчик команды отмены."""
    try:
        current_state = await state.get_state()
        if current_state is not None:
            logging.info("Cancelling state %r", current_state)
            await state.clear()
            await message.answer("Операция отменена.")
        else:
            await message.answer("Нет активных операций для отмены.")
    except Exception as err:
        print(err)


# start CONVERT WORD IN BINARY
@dp.message((F.text == mk.CONVERT_WORD_IN_BINARY_CODE))
async def byte_message(message: Message, state: FSMContext):
    """Пользовательский ввод и состояние для конвертации."""
    await state.set_state(WordInByteState.name)
    await message.answer(
        "Введите ваше слово или имя, для конвертации "
        "в двоичный код 🦾",
    )


@dp.message(WordInByteState.name)
async def transcript_word(message: types.Message, state: FSMContext):
    await _transcript_word(message, state)
# end CONVERT WORD IN BINARY


# start CONVERT BINARY IN WORD
# NOTE Нужно добавить кол-во символов которое перебиралось и кол-во запросов, а еще в БД записывать все это
@dp.message((F.text == mk.CONVERT_BINARY_CODE_IN_WORD))
async def start_transcript(message: Message, state: FSMContext):
    """Пользовательский ввод и состояние для дешифрации."""
    await state.set_state(ByteInWordState.name)
    await message.answer("Введите двоичный код 📟 для дешифрации___ ")


# NOTE Нужно добавить кол-во символов которое перебиралось и кол-во запросов, а еще в БД записывать все это
@dp.message(ByteInWordState.name)
async def transcript_byte(message: types.Message, state: FSMContext):
    await _transcript_byte(message, state)
# end CONVERT BINARY IN WORD


# start GUESS GAME
@dp.message((F.text == mk.GAMES_GUESS_NUMBER))
async def start_guess_game(message: Message, state: FSMContext):
    await info_game_number(message, state, GuessGamesState)


@dp.message(GuessGamesState.name)
async def guess_number(message: types.Message, state: FSMContext):
    await _guess_number(message, state)
# end GUESS GAME


@dp.callback_query((F.data == pic.guess_game_profile))
async def guess_game_profile(callback_query: types.CallbackQuery):
    get_profile = await get_profile_users(callback_query)
    answer = "#" * 3 + "Угадай Число!\n"
    if guess_number := get_profile.guess_number:
        answer += f"Лучший результат: &lt; {guess_number.best_result} &gt;\n "
        answer += f"Общее количество попыток: &lt; {guess_number.total_number_games} &gt;\n"
    else:
        answer += " Нет результатов\n"
    await callback_query.message.answer(text=answer)


@dp.callback_query(F.data == pic.converter_profile)
async def converter_profile(callback_query: types.CallbackQuery):
    try:
        get_profile = await get_profile_users(callback_query)
        answer = "#" * 3 + "Конвертер\n"
        if binary_converter := get_profile.binary_converter:
            answer += " * Конвертирований слов в двоичное представление:\n"
            answer += f"  --  Общее количество попыток: &lt; {binary_converter.total_try_convert_word_in_byte} &gt;\n"
            answer += f"  --  Количество слов: &lt; {binary_converter.count_encrypted_word} &gt;\n"
            answer += f"  --  Итоговое количство символов: &lt; {binary_converter.count_encrypted_characters} &gt;\n"

            answer += " * Конвертирований двоичного кода в символы:\n"
            answer += f"  --  Общее количество попыток: &lt; {binary_converter.total_try_convert_byte_in_word} &gt;\n"
            answer += f"  --  Количество символов представленных в двоичном коде: &lt; {binary_converter.number_decoded_word} &gt;\n"
            answer += f"  --  Общее количество переданных нулей и единиц: &lt; {binary_converter.number_decoded_characters} &gt;\n"
        else:
            answer += " Нет результатов\n"
        await callback_query.message.answer(text=answer)
    except Exception as err:
        print(err)


@dp.callback_query(F.data == pic.haort_game_profile)
async def haort_game_profile(callback_query: types.CallbackQuery):
    get_profile = await get_profile_users(callback_query)
    answer = "#" * 3 + "Пирамида Хаорта\n"
    if gphp := get_profile.game_profile_haort_pyramid:
        answer += f"Лучший результат: &lt; {gphp.best_result} &gt;\n"
        answer += f"Общее количество попыток: &lt; {gphp.total_number_games} &gt;\n"
    else:
        answer += " Нет результатов\n"
    await callback_query.message.answer(text=answer)


@dp.message((F.text == mk.ME_PROFILE))
async def profile_user(message: Message):
    button_1 = types.InlineKeyboardButton(
        text=pic.guess_game_profile, callback_data=pic.guess_game_profile,
    )
    button_2 = types.InlineKeyboardButton(
        text=pic.converter_profile, callback_data=pic.converter_profile,
    )
    button_3 = types.InlineKeyboardButton(
        text=pic.haort_game_profile, callback_data=pic.haort_game_profile,
    )
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
                    [button_1], [button_2], [button_3],
                ],
    )
    await message.answer(
        "Профиль какой игры хотите посмотреть?",
        reply_markup=keyboard,
    )


@dp.message(CommandStart())
async def send_welcome(message: Message):
    """
    Вызывается в случаем получения команды `/start`

    methods:
        create_user - создания юзера и занесения в базу данных.
    """

    try:
        await get_or_create_user(message)
    except Exception as err:
        print(err)

    button_1 = types.KeyboardButton(text=mk.CONVERT_WORD_IN_BINARY_CODE)
    button_2 = types.KeyboardButton(text=mk.CONVERT_BINARY_CODE_IN_WORD)
    button_3 = types.KeyboardButton(text=mk.GAMES_GUESS_NUMBER)
    button_4 = types.KeyboardButton(text=mk.HAORT_GAME)
    button_5 = types.KeyboardButton(text=mk.ME_PROFILE)
    button_6 = types.KeyboardButton(text=mk.cancel)
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
                    [button_1], [button_2], [button_3], [button_4], [button_5], [button_6],
                ],
        resize_keyboard=True,
    )

    await message.answer(
        text="Привет!\nХочешь увидеть, как выглядит любой символ, "
        "или мб твоё имя в байтовом представлении?! - жми -> /byte\n"
        "Если нужно конвертировать машинный код в слова или буквы, "
        "то жми -> /transcript\n"
        "А может сыграем в игру Угадай число? - жми -> /numbers_game\n"
        "Или жми кнопки внизу 👇👇👇",
        reply_markup=keyboard,
    )


async def main() -> None:
    try:
        bot = Bot(TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
        await dp.start_polling(bot)
    except Exception as err:
        print(err)
        logging.exception(f"Error: {err}")

if __name__ == "__main__":
    try:
        print("поехали")
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as err:
        logging.exception(f"Error. {err}")
