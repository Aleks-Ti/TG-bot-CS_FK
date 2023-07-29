import logging
import os
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bitarray import bitarray
from stiker import STIKER_ANGRY_HACKER, STIKER_FANNY_HACKER
import asyncio as asin

load_dotenv()


logging.basicConfig(
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename=os.path.join(os.path.dirname(__file__), 'program.log'),
    encoding='utf-8',
)


TELEGRAM_TOKEN = os.getenv('TOKEN')
TELEGRAM_CHAT_ID = os.getenv('CHAT_ID')

RETRY_PERIOD = 10  # Период обращения


storage = MemoryStorage()
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)


class ByteState(StatesGroup):
    """Машина состояния.

    Сохранение пользовательского ввода для конвертации в байт код.
    """

    name = State()


class ConvertState(StatesGroup):
    """Машина состояния.

    Сохранение пользовательского ввода для конвертации байт кода в utf-8.
    """

    name = State()


def convert_byte(words: str) -> bytes:
    """Ковнертирование любового символа входящих данных в байт код."""
    return ' '.join(format(x, '08b') for x in bytearray(words, 'utf-8'))


def transcript_byte(code: str) -> str:
    """Перевод байт кода в человекочитаемый формат."""
    try:
        bts = bitarray(code)
        symbol_utf = bts.tobytes().decode('utf-8')
        return symbol_utf
    except BaseException:
        return (
            'Увы! Но данные не являются двоичным '
            'кодом!\nПопробуйте ещё раз!'
        )


@dp.message_handler(commands=['byte'])
async def byte_message(message: types.Message):
    """Пользовательский ввод и состояние для конвертации."""
    await ByteState.name.set()
    await message.reply(
        'Введите ваше слово или имя, для конвертации '
        'его в машинное представление 🦾'
    )

    # await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)


@dp.message_handler(commands=['transcript'])
async def transcript(message: types.Message):
    """Пользовательский ввод и состояние для дешифрации."""
    await ConvertState.name.set()
    await message.reply('Введите машинный код 📟 для дешифрации___ ')


@dp.message_handler(state=ConvertState.name)
async def process_transcript(message: types.Message, state: FSMContext):
    """Отправка сообщения с данными конвертации байт кода в utf-8"""
    chat_id = message.from_user.id
    await state.finish()

    messages = transcript_byte(message.text)
    await bot.send_message(
        chat_id=chat_id,
        text='Лучшие ученые мира принялись за расшифровку! 🧮🧮🧮',
    )
    await asin.sleep(3.5)
    await bot.send_sticker(
        chat_id=chat_id,
        sticker=STIKER_ANGRY_HACKER,
    )
    await asin.sleep(3)
    await bot.send_message(chat_id=chat_id, text='Получение данных ⚙️⚙️⚙️')
    await asin.sleep(3)
    await bot.send_message(
        chat_id=chat_id,
        text=f'Вернулся ответ. Читаем!\nРезультат'
        f':\n\t\t\t\t\t\t\t\t\t->\t\t\t{messages}',
    )


@dp.message_handler(state=ByteState.name)
async def process_name(message: types.Message, state: FSMContext):
    """Отправка сообщения с данными конвертированными в байт код."""
    chat_id = message.from_user.id
    await state.finish()
    messages = convert_byte(message.text)
    await bot.send_message(
        chat_id=chat_id,
        text='Происходит запрос 📡 на главные сервера планеты 📟📟📟',
    )
    await asin.sleep(3)
    await bot.send_sticker(
        chat_id=chat_id,
        sticker=STIKER_FANNY_HACKER,
    )
    await asin.sleep(3)
    await bot.send_message(chat_id=chat_id, text='Получение данных ⚙️⚙️⚙️')
    await asin.sleep(3)
    await bot.send_message(chat_id=chat_id, text=messages)


@dp.message_handler(commands=['*'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text='/byte')
    button_2 = types.KeyboardButton(text='/transcript')
    keyboard.add(button_1, button_2)

    await message.reply(
        'Привет!\nХочешь увидеть, как выглядит любой символ, '
        'или мб твоё имя в байтовом представлении?! - жми -> /byte\n'
        'Если нужно конвертировать машинный код в слова или буквы, '
        'то жми -> /transcript'
        '\nИли нажми кнопки внизу 👇👇👇',
        reply_markup=keyboard,
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
