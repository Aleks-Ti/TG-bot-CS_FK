from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from PIL import Image, ImageDraw, ImageFont

from src.state_machine import HaortGamesState
from src.utils.buttons import HaortPyramidInlineKeyboard as hpik

"""
Можно изменять буквы, из расчёт на удобное для вас управление,
как ABC так и 123, по желанию.
"""


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
        space = "   " * (total_disc)
        result += space + "|_   _|" + space
    else:
        space = "   " * ((total_disc) - disc)
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
    tower_a = [0] * ((total_disc + 1) - len(towers[hpik.TOWER_1].result)) + towers[hpik.TOWER_1].result[::-1]
    tower_b = [0] * ((total_disc + 1) - len(towers[hpik.TOWER_2].result)) + towers[hpik.TOWER_2].result[::-1]
    tower_c = [0] * ((total_disc + 1) - len(towers[hpik.TOWER_3].result)) + towers[hpik.TOWER_3].result[::-1]

    count = 0
    result = ""
    while not count > total_disc:
        result += builder_level_towers(tower_a[count], total_disc, count)
        result += builder_level_towers(tower_b[count], total_disc, count)
        result += builder_level_towers(tower_c[count], total_disc, count) + "\n"
        count += 1
        yield result
        result = ""


def game_condition_check(
        towers: dict[str, Stack], victory_order: list[int],
) -> bool:
    """Проверка условий победы."""

    if (
        towers[hpik.TOWER_2].result == victory_order
        or towers[hpik.TOWER_3].result == victory_order
    ):
        return True
    return False


async def text_to_image(text, image_path, towers, game_difficulty):
    line_height = 15
    image = Image.new("RGB", (450, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    y_text = 10
    for line in show_towers(towers, game_difficulty):
        draw.text((10, y_text), line, font=font, fill=(0, 0, 0))
        y_text += line_height
    image.save(image_path)
    return image


def get_image(image_path):
    return FSInputFile(image_path, filename="Снеговик")


async def active_haort_game(callback_query: types.CallbackQuery, state: FSMContext, keyboard) -> None:
    state_data = await state.get_data()
    try:
        disck_from_to_tower = state_data["towers_condition"][state_data["step_1"]].pop()  # towers[user_input[0]].pop()
        state_data["towers_condition"][callback_query.data].push(disck_from_to_tower)  # towers[user_input[-1]].push(disck_from_to_tower)
    except StackIsEmptyError:
        error_message = "В этой башне нет диска для перемещения. Выберите корректную комбинацию!\n"
        print(error_message)
        await state.update_data(step_1=None)
        await callback_query.message.edit_caption(reply_markup=keyboard)
        await callback_query.message.answer(text=error_message, show_alert=True)
        return
    except IncorrectMove:
        state_data["towers_condition"][state_data["step_1"]].push(disck_from_to_tower)
        error_message = "Нельзя помещать больший диск на малый!\n"
        print(error_message)
        await state.update_data(step_1=None)
        await callback_query.message.edit_caption(reply_markup=keyboard)
        await callback_query.message.answer(text=error_message, show_alert=True)
        return
    await state.update_data(step_1=None)

    output_image_path = "static/" + callback_query.message.from_user.first_name + "_hanoi_towers.png"
    message_towers = show_towers(state_data["towers_condition"], state_data["game_difficulty"])
    await text_to_image(message_towers, output_image_path, state_data["towers_condition"], state_data["game_difficulty"])
    await callback_query.message.edit_media(types.InputMediaPhoto(media=types.FSInputFile(output_image_path)))
    await callback_query.message.edit_caption(reply_markup=keyboard)


async def start_haort_game(callback_query: types.CallbackQuery, state: FSMContext, games_state: HaortGamesState) -> None:
    """Запуск одной сессии игры 'Ханойски башни'."""
    # await state.set_state(games_state.name)
    # await state.set_state(games_state.game_difficulty)
    state_data = await state.get_data()
    complete_tower = [x for x in range((state_data["game_difficulty"]), 0, -1)]
    towers = {
        hpik.TOWER_1: Stack(complete_tower),
        hpik.TOWER_2: Stack(),
        hpik.TOWER_3: Stack(),
    }
    await state.update_data(towers_condition=towers)
    start_message = "Игра началась!\n"
    start_message += (
        (
            f"Даны три пирамиды/стержня, слева направо:\n"
            f" <b>{hpik.TOWER_1}</b>, <b>{hpik.TOWER_2}</b> и <b>{hpik.TOWER_3}</b>\n"
        )
    )
    start_message += (
        (
            f"Перед вами стартовая позиция.\n"
            f"Переместите диски пирамиды {hpik.TOWER_1},"
            f" на любой другой стержень {hpik.TOWER_2} или {hpik.TOWER_3}, в"
            f" правильном порядке, чтобы победить!\n"
        )
    )
    message = show_towers(towers, state_data["game_difficulty"])
    start_message += (
            f"Переместите диск с одной башни на другую.\n"
            f"Пример команды: с {hpik.TOWER_1} на {hpik.TOWER_3} или с {hpik.TOWER_1} на {hpik.TOWER_2} или"
            f" с {hpik.TOWER_3} на {hpik.TOWER_2} и т.п.\n")

    await callback_query.message.answer(text=start_message)
    output_image_path = "static/" + callback_query.message.from_user.first_name + "_hanoi_towers.png"
    await text_to_image(message, output_image_path, towers, state_data["game_difficulty"])
    button_1 = types.InlineKeyboardButton(text=hpik.TOWER_1, callback_data=hpik.TOWER_1)
    button_2 = types.InlineKeyboardButton(text=hpik.TOWER_2, callback_data=hpik.TOWER_2)
    button_3 = types.InlineKeyboardButton(text=hpik.TOWER_3, callback_data=hpik.TOWER_3)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[[button_1], [button_2], [button_3]],
    )

    pyramid_message = await callback_query.message.answer_photo(
        get_image(output_image_path), reply_markup=keyboard,
    )
    await state.update_data(last_pyramid_message=pyramid_message.message_id)
