import argparse
import os
from collections import deque
import requests

class Browser:
    """Surf the internet"""
    cache_dir = ''
    cached_pages = []
    # add a page history stack
    backstack = deque()

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("dir")
        args = parser.parse_args()
        self.cache_dir = args.dir

        if not os.access(self.cache_dir, os.F_OK):
            os.mkdir(self.cache_dir)

        while True:
            url = input()
            if url == 'exit':
                break
            elif url == 'back':
                self.handle_back()
            elif not self.valid_url(url):
                print('Invalid URL')
            else:
                self.handle_page(url)

    def valid_url(self, url):
        return True if '.' in url else False

    def handle_page(self, url):
        try:
            if not 'https://' in url:
                https_url = 'https://' + url
            else:
                https_url = url
                url = url.strip('https://')

            r = requests.get(https_url)
        except:
            print('Houston... we have a problem')
            return

        page = url.split('.')[0]

        with open(self.cache_dir + '/' + page, 'w+') as file:
            if page not in self.cached_pages:
                self.cached_pages.append(page)
                content = r.text
                file.write(content)
                print(content)
            else:
                print(file.read())
        # also append to history stack
        self.backstack.append(page)

    def handle_back(self):
        # check if there is any history
        # which means there should be at least 2 in the stack, because we choose
        # to append each handled page to history
        if len(self.backstack) < 2:
            return
        else:
            # pop current page
            self.backstack.pop()

        # ... pick the last page from the stack and open it from cache
        with open(self.cache_dir + '/' + self.backstack.pop()) as file:
            print(file.read())

run_a_browser = Browser()
