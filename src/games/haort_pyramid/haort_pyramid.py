import asyncio
import sys
from random import choice, randint

from aiogram import types
from aiogram.fsm.context import FSMContext

from src.state_machine import HaortGamesState

"""
Можно изменять буквы, из расчёт на удобное для вас управление,
как ABC так и 123, по желанию.
"""
TOWER_1 = "Alpha"
TOWER_2 = "Betta"
TOWER_3 = "Gamma"


class StackIsEmptyError(Exception):
    pass


class IncorrectMove(Exception):
    pass


class Stack:
    def __init__(self, result=None) -> None:
        self.result = result if result is not None else []

    def pop(self) -> int:
        try:
            item = self.result.pop(-1)
            return item
        except IndexError as err:
            raise StackIsEmptyError("error: stack is empty") from err

    def push(self, item: int) -> None:
        if self.result == []:
            self.result.append(item)
        else:
            if self.result[-1] < item:
                raise IncorrectMove(
                    'error: an item can"t be placed on top of'
                    ' the stack, that"s the rules of the game.',
                )
            self.result.append(item)


def builder_level_towers(disc: int, total_disc: int, count: int) -> str:
    """Генерирует горизонтальный уровень башни."""

    result = ""
    if disc == 0:
        space = " " * (total_disc)
        result += space + "|_ _|" + space
    else:
        space = " " * ((total_disc) - disc)
        if count > 9:
            result += space + "#" * disc + f"|_{disc}_|" + "#" * (disc - 1) + space
        else:
            result += space + "#" * disc + f"|_{disc}_|" + "#" * disc + space
    return result


def show_towers(towers: dict[str, Stack], total_disc: int) -> None:
    """Выводит в терминал отображение Ханойских башен.

    - tower_a, tower_b, tower_c - Полное копирование списка дисков башен \
        из экземпляров класса Stack хранящегося по ключу в словаре 'towers',\
        и заполнение их нулями (total_disc + 1) \
        для полноценного графического отображения башни в терминале.
    """

    tower_a = [0] * ((total_disc + 1) - len(towers[TOWER_1].result)) + towers[TOWER_1].result[::-1]
    tower_b = [0] * ((total_disc + 1) - len(towers[TOWER_2].result)) + towers[TOWER_2].result[::-1]
    tower_c = [0] * ((total_disc + 1) - len(towers[TOWER_3].result)) + towers[TOWER_3].result[::-1]

    count = 0
    result = ""
    while not count > total_disc:
        result += builder_level_towers(tower_a[count], total_disc, count)
        result += builder_level_towers(tower_b[count], total_disc, count)
        result += builder_level_towers(tower_c[count], total_disc, count) + "\n"
        count += 1

    result = "<pre>" + result + "</pre>"
    return result


def game_condition_check(
        towers: dict[str, Stack], victory_order: list[int],
) -> bool:
    """Проверка условий победы."""

    if (
        towers[TOWER_2].result == victory_order
        or towers[TOWER_3].result == victory_order
    ):
        return True
    return False


async def start_haort_game(callback_query: types.CallbackQuery, state: FSMContext, games_state: HaortGamesState) -> None:
    """Запуск одной сессии игры 'Ханойски башни'."""

    complete_tower = [x for x in range(games_state.game_difficulty, 0, -1)]
    towers = {
        TOWER_1: Stack(complete_tower),
        TOWER_2: Stack(),
        TOWER_3: Stack(),
    }
    start_message = "Игра началась!\n"
    start_message += (
        (
            f"Даны три пирамиды/стержня, слева направо:\n"
            f" <b>{TOWER_1}</b>, <b>{TOWER_2}</b> и <b>{TOWER_3}</b>\n"
        )
    )
    start_message += (
        (
            f"Перед вами стартовая позиция.\n"
            f"Переместите диски пирамиды {TOWER_1},"
            f" на любой другой стержень {TOWER_2} или {TOWER_3}, в"
            f" правильном порядке, чтобы победить!\n"
        )
    )
    message = show_towers(towers, games_state.game_difficulty)
    start_message += (
            f"Переместите диск с одной башни на другую.\n"
            f"Пример команды: {TOWER_1}{TOWER_3} or {TOWER_1}{TOWER_2} or"
            f" {TOWER_3}{TOWER_2} etc.\n")

    await callback_query.message.answer(text=start_message)
    pyramid_message = await callback_query.message.answer(text=message)
    games_state.last_pyramid_message = pyramid_message.message_id
    # while True:
    #     user_input = str(input("Переместите диск:\t")).strip().upper()
    #     if (
    #         not isinstance(user_input, str)
    #         or len(user_input) != 2
    #         or not all([x in (TOWER_1, TOWER_2, TOWER_3) for x in user_input])
    #     ):
    #         color_print(
    #             (
    #                 f"Команда, должна быть символом из двух букв английского"
    #                 f" алфавита соответствующих названиям башен"
    #                 f" {TOWER_1}, {TOWER_2} и {TOWER_3}."
    #                 f"\n\tПример: {TOWER_1}{TOWER_3} or {TOWER_1}{TOWER_2} or"
    #                 f" {TOWER_3}{TOWER_2} etc.\n"
    #             ),
    #         )
    #         continue

    #     try:
    #         disck_from_to_tower = towers[user_input[0]].pop()
    #         towers[user_input[-1]].push(disck_from_to_tower)
    #     except StackIsEmptyError:
    #         color_print(
    #             "В этой башне нет диска для перемещения."
    #             " Выберите корректную комбинацию!\n",
    #         )
    #         continue
    #     except IncorrectMove:
    #         towers[user_input[0]].push(
    #             disck_from_to_tower,
    #         )  # лишняя операция, хоть и O(1)
    #         color_print(
    #             "Нельзя помещать больший диск на малый!\n",
    #             Fore.YELLOW,
    #         )
    #     if game_condition_check(towers, complete_tower):
    #         color_print("Вы победили! Отличный результат!\n", Fore.GREEN)
    #         show_towers(towers, total_disc)
    #         break
    #     show_towers(towers, total_disc)
