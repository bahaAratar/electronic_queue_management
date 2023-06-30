import requests
from bs4 import BeautifulSoup as BS
import csv

url = 'https://www.rsk.kg/load_points'
respons = requests.get(url).json()
print(respons[1]['ServicePoint'][0]['mode'])
# soup = BS(respons, 'lxml')
# print(soup)
# data = soup.find_all('div', id='markers')
# print(data)
