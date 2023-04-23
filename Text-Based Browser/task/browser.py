import sys
import os
import requests
from collections import deque

dir_name = sys.argv[1]

if not os.path.exists(dir_name):
    os.mkdir(dir_name)

history = deque()


def get_site_content(url):
    return requests.get(url).text


def save_site_content(data, path):
    history.append(path)
    with open(os.path.join(dir_name, path), "w") as f:
        f.write(data)


def go_site(site):
    address = site if site.startswith("https://") else f"https://{site}"
    site_content = get_site_content(address)
    save_site_content(site_content, site.removeprefix('https://').split('.')[0])
    print(site_content)


def go_back():
    history.pop()
    with open(os.path.join(dir_name, history.pop()), 'r') as f:
        print(f.read())


while True:
    command = input()
    if command == "exit":
        break
    if command == "back":
        go_back()
    elif "." in command:
        go_site(command)
    else:
        print("Error: Incorrect URL")