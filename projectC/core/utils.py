def word_declension(count) -> str:
    '''Определяет склонение слова относительно числа.'''
    if count == '[NULL]':
        return 'попыток'
    if count <= 1:
        return 'попытку'
    elif count > 1 and count < 5:
        return 'попытки'
    else:
        return 'попыток'
