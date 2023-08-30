import logging
import os
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bitarray import bitarray
from stiker import (
    STICKER_ANGRY_HACKER,
    STICKER_FANNY_HACKER,
    not_sticker,
    hot_sticker,
    cold_sticker,
    win_sticker,
)
import asyncio as asin
from random import randint, choice
from core.utils_db import (
    create_user,
    game_data_update_users_profile,
    get_profile_users,
)

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TOKEN')
TELEGRAM_CHAT_ID = os.getenv('CHAT_ID')

RETRY_PERIOD = 10  # Период обращения

storage = MemoryStorage()
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)


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


class GamesState(StatesGroup):
    """Машина состояния.

    Ожидание пользовательского ввода guess game.
    """

    name = State()


class GameCon:
    """Game conditions.

    Attributes:
        SECRETS_NUM_GAME: Рандомное число от 0 до 100.
        COUNT_GAME: Счетчик попыток одной сессии.
    """

    SECRETS_NUM_GAME: int
    COUNT_GAME = 0


@dp.message_handler(commands=['cancel'], state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """Обработчик команды отмены."""
    current_state = await state.get_state()
    if current_state is not None:
        logging.info('Cancelling state %r', current_state)
        await state.finish()
        await message.answer('Операция отменена. Вернулся в начальное состояние.')
    else:
        await message.answer('Нет активных операций для отмены.')


def word_declension(count: int) -> str:
    '''Определяет склонение слова относительно числа.'''
    if count <= 1:
        return 'попытку'
    elif count > 1 and count < 5:
        return 'попытки'
    else:
        return 'попыток'


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


@dp.message_handler(commands=['numbers_game'])
async def game_number(message: types.Message):
    """Пользовательский ввод и состояние для игры."""
    await GamesState.name.set()
    GameCon.COUNT_GAME = 0
    GameCon.SECRETS_NUM_GAME = randint(0, 100)
    await message.reply(
        '###########\n'
        '### Угадай ЧИСЛО!\n'
        '### Правила просты!\n'
        '#### Число может быть от 0 до 100.\n'
        '### Если введешь не число,\n'
        '#### оно конвертируется в число из таблицы utf-8\n'
        '##### и ты ошибешься! 😝\n'
        '### Если число больше, то я подскажу - горячо,\n'
        '#### если меньше - холодно\n'
        '##### а если вне диапазона?! ...\n'
        '### Вперед друг, к победе!!!\n'
        '###########'
    )


async def sticker_message(id, sticker):
    await bot.send_sticker(
        chat_id=id,
        sticker=choice(sticker),
    )


@dp.message_handler(state=GamesState.name)
async def guess_number(message: types.Message, state: FSMContext):
    """Отправка сообщения c результатом игры."""
    secret = GameCon.SECRETS_NUM_GAME
    chat_id = message.from_user.id
    try:
        value = int(message.text)
    except ValueError:
        value = ord(message.text[0])
    while True:
        GameCon.COUNT_GAME += 1
        if 0 > value or value > 100:
            await sticker_message(chat_id, not_sticker)
            await state.update_data(value=value)
            break
        if GameCon.COUNT_GAME == 100:
            await state.finish()
            await bot.send_message(
                chat_id=chat_id,
                text='##########'
                '### 100 попыток это максимум!\n'
                '### Число не найдено.\n'
                '### В следующий раз получиться!\n'
                '### Игра окончена.\n'
                '###########',
            )
            break
        if value > secret:
            await sticker_message(chat_id, hot_sticker)
            await state.update_data(value=value)
            break
        elif value < secret:
            await sticker_message(chat_id, cold_sticker)
            await state.update_data(value=value)
            break
        else:
            await sticker_message(chat_id, win_sticker)
            await state.finish()
            await asin.sleep(1.5)
            count_game = GameCon.COUNT_GAME
            create_user(message)
            game_data_update_users_profile(message, count_game)
            await bot.send_message(
                chat_id=chat_id,
                text='#######🎉🎉🎉\n'
                '### УРААА!!!\n### ПОБЕДА!\n'
                '### У тебя получилось угадать'
                ' за '
                + str(count_game)
                + ' '
                + word_declension(count_game)
                + '\n'
                '### 🎊 Внушительный результат!!!\n'
                '### Игра окончена! \n'
                '########🎉🎉',
            )
            break


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
        sticker=STICKER_ANGRY_HACKER,
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
        sticker=STICKER_FANNY_HACKER,
    )
    await asin.sleep(3)
    await bot.send_message(chat_id=chat_id, text='Получение данных ⚙️⚙️⚙️')
    await asin.sleep(3)
    await bot.send_message(chat_id=chat_id, text=messages)


@dp.message_handler(commands=['profile'])
async def profile_user(message: types.Message):
    get_user = get_profile_users(message)
    await bot.send_message(chat_id=message['from']['id'], text=get_user)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Вызывается в случаем получения команды `/start`

    methods:
        create_user - создания юзера и занесения в базу данных.
    """

    create_user(message)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text='/byte')
    button_2 = types.KeyboardButton(text='/transcript')
    button_3 = types.KeyboardButton(text='/numbers_game')
    button_4 = types.KeyboardButton(text='/profile')
    button_5 = types.KeyboardButton(text='/cancel')
    keyboard.add(button_1, button_2, button_3, button_4, button_5)

    await message.reply(
        'Привет!\nХочешь увидеть, как выглядит любой символ, '
        'или мб твоё имя в байтовом представлении?! - жми -> /byte\n'
        'Если нужно конвертировать машинный код в слова или буквы, '
        'то жми -> /transcript\n'
        'А может сыграем в игру Угадай число? - жми -> /numbers_game\n'
        'Или нажми кнопки внизу 👇👇👇',
        reply_markup=keyboard,
    )


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    except BaseException as err:
        logging.info(f'Ошибка: {err}')
