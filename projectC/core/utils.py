def word_declension(count: int) -> str:
    '''Определяет склонение слова относительно числа.'''
    if count <= 1:
        return 'попытку'
    elif count > 1 and count < 5:
        return 'попытки'
    else:
        return 'попыток'
