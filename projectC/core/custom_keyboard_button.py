keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_game_guess_number = types.KeyboardButton(
    text='Игра угадай число', request_location=True
)
button_1 = types.KeyboardButton(text='/byte')
button_2 = types.KeyboardButton(text='/transcript')
button_3 = types.KeyboardButton(text='/me_profile')
button_4 = types.KeyboardButton(text='/cancel')

# Добавляем кнопку "Игра угадай число" в клавиатуру
keyboard.add(button_game_guess_number, button_1, button_2, button_3, button_4)


@dp.message_handler(
    lambda message: message.text == 'Игра угадай число', content_types=['text']
)
async def game_guess_number(message: types.Message):
    # Отправляем команду /game_guess_number при нажатии кнопки "Игра угадай число"
    await message.reply('/game_guess_number')
