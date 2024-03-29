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
    pattern = r'<(?P<word>[\w ]+)>'
    output = open(ns.output, 'w+', encoding='utf-8')
    manual_output = open(f'{ns.output}.manual', 'w+', encoding='utf-8')
    for path, dirs, files in os.walk(ns.dir):
        for filename in files:
            if filename.endswith('.nl'):
                file = os.path.join(path, filename)
                with open(file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip('\r').strip('\n').strip()
                        if not line:
                            continue
                        matched = re.findall(pattern, line)
                        if not matched:
                            continue
                        word = None
                        for m in matched:
                            if m != 'br':
                                word = m
                                break
                        explanation = query_word(word, ns.server)
                        splits = explanation.split('\n', 1)
                        if explanation == 'can not find definitions':
                            manual_output.write(f'{word}\n')
                        else:
                            context = line.replace(f'<{word}>', word)
                            output.write(f'{word}\t{splits[-1]}\t{splits[0]}\n')
            print(f'process file {filename} done!')
        break

