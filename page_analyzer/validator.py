from validators.url import url as is_valid


def validate(url):
    if not url:
        return 'Поле не должно быть пустым'
    if not is_valid(url):
        return 'Убедитесь в правильности введенного URL'
    if len(url) > 255:
        return 'Длина URL не должна превышать 255 символов'
