import requests


def get_content_type(url):
    return requests.get(url).headers['content-type']