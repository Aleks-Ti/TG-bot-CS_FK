import json
import logging

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from PIL import Image, ImageDraw, ImageFont

from src.games.haort_pyramid.haort_query import get_win_game_by_difficulty_for_user, update_or_create_haort_game
from src.utils.buttons import HaortPyramidInlineKeyboard as hpik
from src.utils.delete_image import delete_image_in_system

MAX_LEVEL_TOWER = 12


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

    def to_dict(self):
        return {"result": self.result}

    @staticmethod
    def from_dict(data):
        stack = Stack()
        stack.result = data["result"]
        return stack


def builder_level_towers(disc: int, total_disc: int) -> str:
    """Генерирует горизонтальный уровень башни."""

    symbol = "🔤"
    result = ""
    if disc == 0:
        space = "   " * (total_disc)
        result += space + "|_   _|" + space
    else:
        space = "   " * ((total_disc) - disc)
        if disc > 9:
            result += space + symbol * disc + f"|_{disc}_|" + symbol * (disc - 1) + space
        else:
            result += space + symbol * disc + f"|_{disc}_|" + symbol * disc + space
    return result


def show_towers(towers: dict[str, Stack], total_disc: int):
    """Собрщик уровней башни, сверху вниз.

    - tower_a, tower_b, tower_c - Полное копирование списка дисков башен \
        из экземпляров класса Stack хранящегося по ключу в словаре 'towers',\
        и заполнение их нулями (total_disc + 1) \
        для полноценного графического отображения башни в терминале.
    """
    tower_a = [0] * (MAX_LEVEL_TOWER - len(towers[hpik.TOWER_1].result)) + towers[hpik.TOWER_1].result[::-1]
    tower_b = [0] * (MAX_LEVEL_TOWER - len(towers[hpik.TOWER_2].result)) + towers[hpik.TOWER_2].result[::-1]
    tower_c = [0] * (MAX_LEVEL_TOWER - len(towers[hpik.TOWER_3].result)) + towers[hpik.TOWER_3].result[::-1]

    count = 0
    result = ""
    while count < MAX_LEVEL_TOWER:
        result += builder_level_towers(tower_a[count], total_disc)
        result += builder_level_towers(tower_b[count], total_disc)
        result += builder_level_towers(tower_c[count], total_disc) + "\n"
        count += 1
        yield result
        result = ""


async def game_condition_check(
        towers: dict[str, Stack], victory_order: list[int],
) -> bool:
    """Проверка условий победы."""

    if (
        towers[hpik.TOWER_2].result == victory_order
        or towers[hpik.TOWER_3].result == victory_order
    ):
        return True
    return False


async def text_to_image(image_path, towers, game_difficulty):
    try:
        y_level_between_spacing = 13  # отступ между уровнями башни
        image = Image.new("RGB", (470, 200), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default(size=11.0)
        y_distance_top = 35  # отступ по Y от верхнего края картинки.
        for line in show_towers(towers, game_difficulty):
            _, _, text_w, _ = font.getbbox(line)
            x_distance_left = ((image.width - text_w) // 2)  # Положение текста по оси X к центру
            draw.text((x_distance_left, y_distance_top), line, font=font, fill=(0, 0, 0))
            y_distance_top += y_level_between_spacing
        image.save(image_path)
        return image
    except Exception as err:
        logging.exception(f"Error. {err}")


def get_image(image_path):
    return FSInputFile(image_path, filename="Снеговик")


async def show_image_by_game_difficulty_in_profile_user(callback_query: types.CallbackQuery, game_difficulty: int):
    requested_game = await get_win_game_by_difficulty_for_user(callback_query, game_difficulty)
    output_image_path = "static/" + str(callback_query.from_user.id) + "_show_hanoi_towers.png"

    state_of_play_data: dict = json.loads(requested_game.best_result)
    towers = {key: Stack.from_dict(value) for key, value in state_of_play_data.items()}

    await text_to_image(output_image_path, towers, game_difficulty)

    return output_image_path


async def active_haort_game(callback_query: types.CallbackQuery, state: FSMContext, keyboard) -> None:
    state_data = await state.get_data()
    complete_tower = [x for x in range((state_data["game_difficulty"]), 0, -1)]
    try:
        await state.update_data(number_of_permutations=state_data["number_of_permutations"] + 1)
        TowerStack: dict[str, Stack] = state_data["towers_condition"]
        disck_from_to_tower = TowerStack[state_data["step_1"]].pop()
        TowerStack[callback_query.data].push(disck_from_to_tower)
    except StackIsEmptyError:
        error_message = "В этой башне нет диска для перемещения. Выберите корректную комбинацию!\n"
        await state.update_data(step_1=None)
        await callback_query.message.edit_caption(reply_markup=keyboard)
        await callback_query.answer(text=error_message, show_alert=True)
        return
    except IncorrectMove:
        TowerStack[state_data["step_1"]].push(disck_from_to_tower)
        error_message = "Нельзя помещать больший диск на малый!\n"
        await state.update_data(step_1=None)
        await callback_query.message.edit_caption(reply_markup=keyboard)
        await callback_query.answer(text=error_message, show_alert=True)
        return
    await state.update_data(step_1=None)

    output_image_path = "static/" + str(callback_query.from_user.id) + "_hanoi_towers.png"
    await text_to_image(output_image_path, TowerStack, state_data["game_difficulty"])
    if await game_condition_check(TowerStack, complete_tower):
        await callback_query.message.edit_media(types.InputMediaPhoto(media=types.FSInputFile(output_image_path)))
        win_keyboard = types.InlineKeyboardMarkup(
                inline_keyboard=[[types.InlineKeyboardButton(text="Ура! Это ПОБЕДА!", callback_data="Ура! Это ПОБЕДА!")]],
            )
        await callback_query.message.edit_caption(reply_markup=win_keyboard)
        await callback_query.answer(
            text=f"Ура! Это ПОБЕДА!\nКоличество перестановок за игру"
                 f": {state_data["number_of_permutations"]}.\n"
                 f"Вы всегда можете посмотреть результат игры в профиле в главном меню!",
            show_alert=True,
        )
        await update_or_create_haort_game(callback_query, state)
        await state.clear()
        await delete_image_in_system(output_image_path)
    else:
        await callback_query.message.edit_media(types.InputMediaPhoto(media=types.FSInputFile(output_image_path)))
        await callback_query.message.edit_caption(reply_markup=keyboard)


async def start_haort_game(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    state_data = await state.get_data()
    complete_tower = [x for x in range((state_data["game_difficulty"]), 0, -1)]
    stack = Stack
    towers = {
        hpik.TOWER_1: stack(complete_tower),
        hpik.TOWER_2: stack(),
        hpik.TOWER_3: stack(),
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
    start_message += (
            f"Переместите диск с одной башни на другую.\n"
            f"Пример команды: с {hpik.TOWER_1} на {hpik.TOWER_3} или с {hpik.TOWER_1} на {hpik.TOWER_2} или"
            f" с {hpik.TOWER_3} на {hpik.TOWER_2} и т.п.\n")

    await callback_query.message.answer(text=start_message)
    output_image_path = "static/" + str(callback_query.from_user.id) + "_hanoi_towers.png"
    await text_to_image(output_image_path, towers, state_data["game_difficulty"])
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
