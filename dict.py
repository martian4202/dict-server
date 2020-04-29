import mdict_query
from typing import (
    List, TypeVar, Generic
)
from debug import debugger
import re, logging, requests, asyncio
from online import process
from bs4 import Tag, BeautifulSoup, NavigableString

KT = TypeVar('KT') 
VT = TypeVar('VT')

class IDictionary(Generic[KT, VT]):
    def lookup(self, word: KT)->VT:
        pass

Dictionary = IDictionary[str, List[str]]

class OLDict():
    def __init__(self):
        pass

    def process_oldict(self, soup: BeautifulSoup) -> List[Tag]:
        ret = []
        ret.extend(soup.find_all(class_='css-1urpfgu', limit=2))
        style = soup.find('style')
        ret.append(style)
        return ret

    async def lookup(self, word: str) -> List[str]:
        url = 'https://www.dictionary.com/browse/{word}?s=t' 
        return lookup(word, url, self.process_oldict)

def lookup(word: str, url_pattern: str, handler) -> List[str]:
    url = url_pattern.format(word=word)
    ret = []
    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        logging.error(http_err)
        return ret
    try:
        ret.append(process(response.text, handler))
    except Exception as e:
        logging.error(e)
        return []
    return ret

class MDict():
    def __init__(self, mdx_file: str=None, css_file: str=None)-> None:
        with open(css_file, 'r', encoding='utf8') as css:
           self._css_file = css.read()
        self._builder = mdict_query.IndexBuilder(mdx_file)

    @debugger
    async def lookup(self, word: str) -> List[str]:
        keys = self._builder.mdx_lookup(word, ignorecase=True)
        ret = []
        logging.debug(keys)
        for key in keys:
            result = re.match(r'@@@LINK=(\w*)\r\n', key)
            if (result):
                key = self.lookup_must_success(result.group(1))
            content: str = self.__build_content(key)
            ret.append(content)
        return ret
    
    def lookup_must_success(self, word: str)->str:
        keys = self._builder.mdx_lookup(word, ignorecase=True)
        key = keys[0]
        return key
        
    def __build_content(self, key: str)->str:
        return '<html>' + self._css_file + key.strip('\n\r') + '</html>'

class MerriamWebsterDict():
    def __init__(self):
        pass
    async def lookup(self, word: str)-> List[str]:
        url = "http://www.merriam-webster.com/dictionary/{word}"
        return lookup(word, url, self.__process_reponse__)
        
    def __process_reponse__(self, soup: BeautifulSoup)->List[Tag]:
        ret = []
        tag = soup.find(class_="row")
        right = tag.find(class_=re.compile(r'right.*'))
        if right != None:
            right.decompose()
        wgt = tag.find(class_="wgt-incentive-anchors")
        delete_tags = []
        if (wgt):
            for t in wgt.next_siblings:
                delete_tags.append(t)
            [t.extract() for t in delete_tags]
            wgt.decompose()
        cs = soup.find(href=re.compile(r'style.*definitions[^-]*.css$'))
        text = requests.get(cs['href']).text
        style = soup.new_tag('style')
        style.string = text
        ret.append(style)
        ret.append(tag)
        return ret


if __name__ == "__main__":
    async def func(d: Dictionary):
       ret = await d.lookup("top")
       with open('output.html', 'w+', encoding='utf8') as f:
           if len(ret) == 0:
               print("not found")
               return
           f.write(ret[0])

    asyncio.run(func((OLDict())))
    # word_file = open('word.txt', 'r')
    # css_style = ''
    # with open('style.css', 'r') as css_file:
    #     css_style = css_file.read()

    # output_file_name = 'E:/words.txt'
    # output_file = open(output_file_name, 'a')
    # numHandle = 0
    # builder = mdict_query.IndexBuilder('E:/dict/OALD9EnEn.mdx')
    # index = 1
    # for i in range(100):
    #     line = word_file.readline().strip('\n').strip()
    #     if line == "":
    #         break
    #     print(line)
    #     keys = builder.mdx_lookup(line)
    #     for key in keys:
    #         content = line + '\t' + '<html>' + css_style+key.encode('utf8').strip('\n\r') + '</html>'
    #         output_file.write(content)
    #         output_file.write('\n')
    #     numHandle += 1
    # print('handle word: ' + str(line) + ', Total: ' +  str(numHandle))
