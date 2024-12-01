import requests
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

def _download_input(day: int):
    with open(f'{current_dir}/.cookie', 'r') as file:
        cookie = file.read().strip()

    url = f'https://adventofcode.com/2024/day/{day}/input'
    headers = {'Cookie': cookie}
    response = requests.get(url, headers=headers)

    with open(f'in_{day}.txt', 'w') as file:
        file.write(response.text)
    return response.text

def get_input(day: int):
    try:
        with open(f'in_{day}.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return _download_input(day)