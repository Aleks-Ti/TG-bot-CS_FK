import asyncio as asyn

from aiogram import types
from aiogram.fsm.context import FSMContext
from bitarray import bitarray

from src.games.binary_converter.binary_query import binary_in_word_update, word_in_binary_update
from src.utils.stikers import STICKER_ANGRY_HACKER, STICKER_FANNY_HACKER


async def word_convert_in_binary(words: str) -> bytes:
    """Ковнертирование любового символа входящих данных в двоичный код."""
    return " ".join(format(x, "08b") for x in bytearray(words, "utf-8"))


async def byte_convert_in_word(code: str) -> str:
    """Перевод двоичного кода в человекочитаемый формат."""
    try:
        bts = bitarray(code)
        symbol_utf = bts.tobytes().decode("utf-8")
        return symbol_utf
    except BaseException:
        return (
            "Увы! Но данные не являются двоичным "
            "кодом!\nПопробуйте ещё раз!"
        )


async def transcript_byte(message: types.Message, state: FSMContext):
    """Отправка сообщения с данными конвертации байт кода в utf-8"""
    await state.clear()
    await binary_in_word_update(message)
    result = await byte_convert_in_word(message.text)
    await message.answer(
        text="Лучшие ученые мира принялись за расшифровку! 🧮🧮🧮",
    )
    await asyn.sleep(2)
    await message.answer_sticker(
        sticker=STICKER_ANGRY_HACKER,
    )
    await asyn.sleep(2)
    await message.answer(text="Получение данных ⚙️⚙️⚙️")
    await asyn.sleep(2)
    text = "Вернулся ответ. Читаем!\nРезультат:\n"
    answer_message = text + "<pre>" + result + "</pre>"
    await message.answer(answer_message)


async def transcript_word(message: types.Message, state: FSMContext):
    """Отправка сообщения с данными конвертированными в байт код."""
    await state.clear()
    await word_in_binary_update(message)
    result = await word_convert_in_binary(message.text)
    await message.answer(
        text="Происходит запрос 📡 на главные сервера планеты 📟📟📟",
    )
    await asyn.sleep(2)
    await message.answer_sticker(
        sticker=STICKER_FANNY_HACKER,
    )
    await asyn.sleep(2)
    await message.answer(text="Получение данных ⚙️⚙️⚙️")
    await asyn.sleep(2)
    answer_message = "<pre>" + result + "</pre>"
    await message.answer(answer_message)
