import requests

from bs4 import BeautifulSoup

letter = 'S'
url = input()
# url = 'http://web.archive.org/web/20201201053628/https://www.who.int/health-topics'

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

output = []
for p in soup.find_all('a'):
    if p.text.startswith('S'):
        output.append(p.text)

output = output[output.index('Schistosomiasis'):output.index('Sustainable Development Goals')+1]
print(output)