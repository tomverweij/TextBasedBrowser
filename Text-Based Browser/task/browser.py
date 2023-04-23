import sys
import os
import shutil
import requests
from collections import deque
from bs4 import BeautifulSoup

dir_name = sys.argv[1]

if os.path.exists(dir_name):
    shutil.rmtree(dir_name)
os.mkdir(dir_name)

history = deque()


def get_site_content(url):
    try:
        r = requests.get(url)
        r.encoding = 'UTF-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        return '\n'.join([text for text in soup.stripped_strings])

    except requests.exceptions.ConnectionError:
        print("Invalid URL")
        return '-1'


def save_site_content(data, path):
    history.append(path)
    with open(os.path.join(dir_name, path), "w") as f:
        f.write(data)


def try_site(site):
    # try reading from cache first
    site_cache = site.removeprefix('https://').split('.')[0]
    if site_cache in os.listdir(dir_name):
        return read_site_from_cache(site_cache)

    # no cache
    url = site if site.startswith("https://") else f"https://{site}"

    site_content = get_site_content(url)
    if site_content != '-1':
        save_site_content(site_content, site_cache)
        print(site_content)


def go_back():
    if len(history) < 2:
        pass
    else:
        history.pop()
        print(read_site_from_cache(history.pop()))


def read_site_from_cache(site_cache):
    with open(os.path.join(dir_name, site_cache), 'r') as f:
        return f.read()


while True:
    command = input()
    if command == "exit":
        break
    if command == "back":
        go_back()
    else:
        try_site(command)
