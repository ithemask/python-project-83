import requests
from bs4 import BeautifulSoup


def check(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None
    result = {
        'status_code': response.status_code,
        'h1': None,
        'title': None,
        'description': None,
    }
    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.h1
    if h1:
        result['h1'] = h1.string
    title = soup.title
    if title:
        result['title'] = title.string
    for meta in soup.find_all('meta'):
        if meta.get('name') == 'description':
            result['description'] = meta.get('content')
    return result
