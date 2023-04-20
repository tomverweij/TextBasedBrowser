import argparse
import os

nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created "soft" magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''

supported_urls = {'bloomberg.com': bloomberg_com, 'nytimes.com': nytimes_com}


class Browser:
    """Surf the internet"""
    cache_dir = ''
    cached_pages = []

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
            elif not self.valid_url(url) or supported_urls.get(url) is None:
                print('Invalid URL')
            else:
                self.handle_page(url)

    def valid_url(self, url):
        return True if '.' in url else False

    def handle_page(self, url):
        page = url.split('.')[0]

        with open(self.cache_dir + '/' + page, 'w+') as file:
            if page not in self.cached_pages:
                self.cached_pages.append(page)
                content = supported_urls.get(url)
                file.write(content)
                print(content)
            else:
                print(file.read())


run_a_browser = Browser()
