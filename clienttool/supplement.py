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
    parser.add_argument('--file', required=True, help='input file')
    parser.add_argument('--server', default='127.0.0.1:8080')
    parser.add_argument('--output', default='D:/tmp.txt')
    ns = parser.parse_args()
    output = open(ns.output, 'w+', encoding='utf-8')
    n = 0
    with open(ns.file, 'r', encoding='utf-8') as file:
        for line in file:
            vocabulary = line.rstrip().split('\t', 1)[0]
            chinese = query_word(vocabulary, ns.server)
            output.write(f'{line.rstrip()}\t{chinese}\n')
            n += 1
            print(n)
    output.close()

