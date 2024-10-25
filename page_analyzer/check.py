import requests
from bs4 import BeautifulSoup


def get_response_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None
    return {'status': response.status_code, 'body': response.text}


def check(url):
    response_data = get_response_data(url)
    if not response_data:
        return None
    result = {
        'status_code': response_data['status'],
        'h1': None,
        'title': None,
        'description': None,
    }
    soup = BeautifulSoup(response_data['body'], 'html.parser')
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
