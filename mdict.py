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


class Dict:
    def __init__(self, mdx: str, style: str):
        with open(style, 'r', encoding='utf8') as css:
            self._css = css.read()

        self._builder = mdict_query.IndexBuilder(mdx)

    async def lookup(self, word):
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

    def lookup_must_success(self, word: str) -> str:
        keys = self._builder.mdx_lookup(word, ignorecase=True)
        key = keys[0]
        return key

    def __build_content(self, key: str) -> str:
        return '<html>' + self._css + key.replace('\n\r', '').replace('\t', '').replace('\n', '').replace('\r',
                                                                                                          '') + '</html>'


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


if __name__ == "__main__":
    async def func(d: Dict):
        ret = await d.lookup("carry out")
        with open('output.html', 'w+', encoding='utf8') as f:
            if len(ret) == 0:
                print("not found")
                return
            f.write(ret[0])


    asyncio.run(func(Dict(mdx='E:/dict/Idioms.mdx', style='E:/dict/Idioms.css')))
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
