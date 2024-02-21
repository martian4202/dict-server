from bs4 import BeautifulSoup
import argparse
import os
import codecs
import sys
import shutil

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True, help='input a html file fron OneNoted')
    ns = parser.parse_args()
    of = f'{ns.input}.txt'
    try:
        os.remove(of)
    except FileNotFoundError as e:
        pass
    with open(ns.input, encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        body = soup.body
        top_div = body.div.div
        divs = top_div.find_all('div')
        with open(of, mode='+a', encoding='utf-8') as output:
            for div in divs[2:]:
                p = div.find('p') or div.find('h2')
                theme = p.get_text(strip=True)
                p.string = theme
                back = str(div).replace('\n', '')
                output.writelines(f'{theme}\t{back}\n')

if __name__ == '__main__':
    main()