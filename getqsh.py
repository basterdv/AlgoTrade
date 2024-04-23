import requests
from bs4 import BeautifulSoup as BS
from fastapi import FastAPI

app = FastAPI()

r = requests.get("http://erinrv.qscalp.ru/")
html = BS(r.content, 'html.parser')

r2 = str(r)

if r2 == '<Response [200]>':
    print('connect OK')

listDir = []
listSec = []

allDir = html.findAll('a')  # soup.findAll('a', class_='lenta')

for data in allDir:
    listDir.append(data.text)

dir = listDir[len(listDir) - 1]

r_dir = requests.get(f'http://erinrv.qscalp.ru/{dir}/')
html = BS(r_dir.content, 'html.parser')
allSec = html.findAll('a')

for data in allSec:
    listSec.append(data.text)

for link in html.find_all('a'):
    if link.get('href') != '/':
        print(link.get('href'))

# Скачиваем файл
file1 = requests.get('http://erinrv.qscalp.ru/2024-04-19/VTBR.2024-04-19.Deals.qsh')

with open('Test_QSH/VTBR.2024-04-19.Deals.qsh', 'wb') as file:
    file.write(file1.content)

