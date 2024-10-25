from urllib.parse import urlparse


def normalize(url):
    components = urlparse(url)
    return f'{components.scheme}://{components.netloc}'
