from aiogram.fsm.state import State, StatesGroup


class WordInByteState(StatesGroup):
    """Машина состояния.

    Ожидание пользовательского ввода для конвертации байт кода в utf-8.
    """

    name = State()
    cancel = State()


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
