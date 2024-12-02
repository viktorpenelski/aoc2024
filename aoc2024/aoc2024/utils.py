import requests
import os
from pathlib import Path

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def _in_file(day: int) -> str:
    return f'{_CURRENT_DIR}/days/in_{day}.txt'

def _download_input(day: int) -> str:
    with open(f'{_CURRENT_DIR}/.cookie', 'r') as file:
        cookie = file.read().strip()

    url = f'https://adventofcode.com/2024/day/{day}/input'
    headers = {'Cookie': cookie}
    response = requests.get(url, headers=headers)

    with open(_in_file(day), 'w') as file:
        file.write(response.text)
    return response.text

def get_input(day: int) -> str:
    try:
        with open(_in_file(day), 'r') as file:
            return file.read()
    except FileNotFoundError:
        return _download_input(day)