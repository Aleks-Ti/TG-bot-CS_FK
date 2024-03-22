from datetime import datetime


def word_declension(count) -> str:
    '''Определяет склонение слова относительно числа.'''
    if count <= 1:
        return 'попытку'
    elif count > 1 and count < 5:
        return 'попытки'
    else:
        return 'попыток'


def get_message_profile_user(instance: object, best_result=False):
    '''Возвращает сформирование сообщение профиля пользователя.'''
    registered_at = str(instance.registered_at)
    registered_at = datetime.strptime(registered_at, '%Y-%m-%d %H:%M:%S.%f')
    formatted_date = registered_at.strftime('%d %B %Y')
    if best_result:
        return (
            f'Хэй {instance.first_name}! 👋\n'
            f'Твой лучший результат в игре:\n'
            f' - угадано за {best_result} {word_declension(best_result)} 🎊\n'
            f'🧮 Сыграно: {instance.total_number_games} игр\n'
            f'Дата регистрации: {formatted_date} 🕰'
        )
    return (
        f'Хэй {instance.first_name}! 👋\n'
        f'Твой лучший результат в игре:\n'
        f'     - Вы, еще ни разу не играли - данные отсутствуют. 🎊\n'
        f'🧮 Сыграно:  {instance.total_number_games} игр\n'
        f'Дата регистрации: {formatted_date} 🕰'
    )
