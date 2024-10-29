from validators.url import url as is_valid


def validate(url):
    if not url:
        return 'Пожалуйста, введите URL для проверки'
    if not is_valid(url):
        return 'Пожалуйста, проверьте корректность введенного URL'
    if len(url) > 255:
        return 'Длина URL не должна превышать 255 символов'
