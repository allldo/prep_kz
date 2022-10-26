

def plural_time(number: int, type_time: str):
    if type_time == 'час':
        if number == 1:
            return '1 час назад'
        elif 1 < number < 5:
            return f'{number} часа назад'
        else:
            return f'{number} часов назад'
    elif type_time == 'минута':
        if number == 1:
            return '1 минуту назад'
        elif 1 < number < 5:
            return f'{number} минуты назад'
        else:
            return f'{number} минут назад'
