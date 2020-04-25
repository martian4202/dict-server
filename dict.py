import mdict_query
from typing import (
    List
)
from debug import debugger

class MDict():
    def __init__(self, mdx_file: str=None, css_file: str=None)-> None:
        with open(css_file, 'r', encoding='utf8') as css:
           self._css_file = css.read()
        self._builder = mdict_query.IndexBuilder(mdx_file)

    @debugger
    async def lookup(self, word: str) -> List[str]:
        keys = self._builder.mdx_lookup(word)
        ret = []
        for key in keys:
            content: str = '<html>' + self._css_file + key.strip('\n\r') + '</html>'
            ret.append(content)
        return ret

if __name__ == "__main__":
    word_file = open('word.txt', 'r')
    css_style = ''
    with open('style.css', 'r') as css_file:
        css_style = css_file.read()

    output_file_name = 'E:/words.txt'
    output_file = open(output_file_name, 'a')
    numHandle = 0
    builder = mdict_query.IndexBuilder('E:/dict/OALD9EnEn.mdx')
    index = 1
    for i in range(100):
        line = word_file.readline().strip('\n').strip()
        if line == "":
            break
        print(line)
        keys = builder.mdx_lookup(line)
        for key in keys:
            content = line + '\t' + '<html>' + css_style+key.encode('utf8').strip('\n\r') + '</html>'
            output_file.write(content)
            output_file.write('\n')
        numHandle += 1
    print('handle word: ' + str(line) + ', Total: ' +  str(numHandle))
