from validators.url import url as validate


def is_valid(url):
    if len(url) <= 255 and validate(url):
        return True
    return False
