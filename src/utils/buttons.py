from aiogram import types


class MainKeyboard:
    """
    Кнопки для главного меню.

    Attributes:
    - GAMES_GUESS_NUMBER = 'Игра угадай число'
    - ME_PROFILE = 'Мой профиль'
    - CONVERT_WORD_IN_BINARY_CODE = 'Слова в двоичный код'
    - CONVERT_BINARY_CODE_IN_WORD = 'Двоичный код в слова'
    - cancel = 'Отмена'
    """

    GAMES_GUESS_NUMBER: str = "Игра - Угадай число! -"
    ME_PROFILE: str = "Мой Профиль"
    CONVERT_WORD_IN_BINARY_CODE: str = "Конвертер - Слова в двоичный код"
    CONVERT_BINARY_CODE_IN_WORD: str = "Конвертер - Двоичный код в слова"
    HAORT_GAME: str = "Игра - Пирамида Хаорта"
    cancel: str = "Отмена"
    records_haort_game: str = "Рекорды: Пирамида Хаорта"


class ProfileInlineKeyboard:
    """
    Инлайн кнопки для меню напоминаний.

    Attributes:
    - guess_game_profile = "профиль: Угадай число"
    - converter_profile = "профиль: Конвертер"
    - haort_game_profile = "профиль: Игра Хаорта"
    """

    guess_game_profile: str = "профиль: Угадай число"
    converter_profile: str = "профиль: Конвертер"
    haort_game_profile: str = "профиль: Игра Хаорта"


class HaortPyramidInlineKeyboard:
    """Инлайн кнопки для перемещений пирамид.
    Attributes:
    - TOWER_1 = "Alpha"
    - TOWER_2 = "Betta"
    - TOWER_3 = "Gamma"
    """

    TOWER_1: str = "Alpha"
    TOWER_2: str = "Betta"
    TOWER_3: str = "Gamma"


async def inline_buttons_generator(buttons: list[str, int], prefix=None, postfix=None) -> list:
    max_button_one_page = 3
    result_list_buttons = []
    temp_list_buttons = []
    count = 0
    for value in buttons:
        text = f"{prefix if prefix else ''}{value if isinstance(value, str) else str(value)}{postfix if postfix else ''}"
        if count == max_button_one_page:
            result_list_buttons.append(temp_list_buttons)
            temp_list_buttons = []
            count = 0  # because clear temp_list_buttons
            temp_list_buttons.append(types.InlineKeyboardButton(text=text, callback_data=text))
            count += 1  # + 1 because after clearing the list, a subsequent button from the iteration has already been added
        else:
            temp_list_buttons.append(types.InlineKeyboardButton(text=text, callback_data=text))
            count += 1
    if temp_list_buttons is not None:
        result_list_buttons.append(temp_list_buttons)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=result_list_buttons,
    )
    return keyboard
