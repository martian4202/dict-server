import json
import requests
from bs4 import Tag, BeautifulSoup
from typing import List

app_id = ''
app_key = ''

url = "https://od-api.oxforddictionaries.com/api/v2/words/EN-US"

def embed_script(tag: Tag):
    if tag.name == "script":
        return True
    return False

def extendable(tag: Tag):
    if tag.has_attr('class'):
        return 'expandable' in tag['class']
    return False

def process_html(html_str: str) -> str:
    soup: BeautifulSoup = None
    soup = BeautifulSoup(html_str, 'html.parser')
    
    results: List[Tag] = soup.find_all(embed_script)
    for r in results:
        r.decompose()

    top_definition_tag: Tag = soup.find(id='top-definitions-section')
    div = top_definition_tag.parent
    if (div == None):
        div: Tag = soup.find(extendable)
    ecs: List[Tag] = div.find_all(class_='expandable-control')
    for ec in ecs:
        ec.decompose()
    root: Tag = soup.find(id='root')
    for c in root.children:
        print(c.name, type(c))
    root.div.replace_with(div)
    return str(soup)



if __name__ == "__main__":
    process_html('E:/projects/dictserver/test.html')
