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
    CONVERT_WORD_IN_BINARY_CODE: str = "Слова в двоичный код"
    CONVERT_BINARY_CODE_IN_WORD: str = "Двоичный код в слова"
    HAORT_GAME: str = "Пирамида Хаорта"
    cancel: str = "Отмена"


class ProfileInlineKeyboard:
    """
    Инлайн кнопки для меню напоминаний.

    Attributes:
    - cycle_reminder = 'Циклическое напоминание'
    - single_reminder = 'Одноразовое напоминание'
    - cancel = 'Отмена'
    """

    guess_game_profile: str = "профиль: Угадай число"
    converter_profile: str = "профиль: Конвертер"
    haort_game_profile: str = "профиль: Игра Хаорта"
