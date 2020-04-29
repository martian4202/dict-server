import json, re
import requests
from bs4 import Tag, BeautifulSoup
from typing import List, Callable
from io import BytesIO

app_id = ''
app_key = ''

url = "https://od-api.oxforddictionaries.com/api/v2/words/EN-US"

def embed_script(tag: Tag):
    if tag.name == "script" or tag.name == "meta":
        return True
    return False


def process(html_str: str, handle_soup: Callable[[BeautifulSoup], List[Tag]]):
    soup = BeautifulSoup(html_str, 'html5lib')
    head = soup.find('head')
    body = soup.find('body')

    filterd = handle_soup(soup)
    head.clear()
    body.clear()
    for tag in filterd:
        if tag.name == 'style':
            head.append(tag)
        else:
            body.append(tag)
    response = requests.post('https://purifycss.online/api/purify', data={
        'htmlCode': str(body),
        'cssCode': str(head)
    })
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise err
    
    d = json.load(BytesIO(response.content))
    head.clear()
    style = soup.new_tag('style')
    style.string = d['purified']['content']
    head.append(style)
    [r.decompose() for r in soup.find_all(embed_script)]

    return str(soup).replace('\r\n', '').replace('\r', '').replace('\n', '')

if __name__ == "__main__":
    pass
