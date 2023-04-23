import requests


def get_response(url):
    try:
        response = requests.get(url)
        print(response.status_code)
    except requests.exceptions.InvalidSchema:
        print('No response')

# get_response('https://google.com')