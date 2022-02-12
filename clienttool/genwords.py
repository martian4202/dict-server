import logging
import argparse
import requests
import pathlib
import os
import re


def query_word(word: str, server: str) -> str:
    url = f'http://{server}/?word={word.strip()}'
    res = requests.get(url)
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error(f'query word failed, error: {e}')
    return res.text


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', required=True, help='input dir')
    parser.add_argument('--server', default='127.0.0.1:8080')
    parser.add_argument('--output', default='D:/tmp.txt')
    ns = parser.parse_args()
    pattern = r'.*<(?P<word>.*)>.*'
    output = open(ns.output, 'w+', encoding='utf-8')
    for path, dirs, files in os.walk(ns.dir):
        for filename in files:
            if filename.endswith('.nl'):
                file = os.path.join(path, filename)
                with open(file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip('\r').strip('\n').strip()
                        if not line:
                            continue
                        mg = re.match(pattern, line)
                        if mg is None:
                            continue
                        word = mg.group('word')
                        explanation = query_word(word, ns.server)
                        context = line.replace('<', '').replace('>', '')
                        output.write(f'{word}\t{context}\t{explanation}\n')
            print(f'process file {filename} done!')
        break

