from urllib.parse import urlparse


def normalize(url):
    components = urlparse(url)
    return components._replace(
        path='',
        params='',
        query='',
        fragment='',
    ).geturl()
