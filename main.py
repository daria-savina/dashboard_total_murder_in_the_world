import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

HOST = 'https://uk.wikipedia.org/'
HEADER = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}
CSV = 'data.csv'
URL = 'https://uk.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BA%D1%80%D0%B0%D1%97%D0%BD_%D0%B7%D0%B0_%D1%80%D1%96%D0%B2%D0%BD%D0%B5%D0%BC_%D1%83%D0%BC%D0%B8%D1%81%D0%BD%D0%B8%D1%85_%D1%83%D0%B1%D0%B8%D0%B2%D1%81%D1%82%D0%B2'

URL2 = 'https://uk.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BA%D1%80%D0%B0%D1%97%D0%BD_%D1%81%D0%B2%D1%96%D1%82%D1%83'
CSV2 = 'iso.csv'

cards = []
iso = []


# get all info about murder from wikipedia html
def get_content(url, params=''):
    r = requests.get(url, headers=HEADER, params=params).text
    soup = BeautifulSoup(r, 'html.parser')
    product = soup.find('tbody')
    global cards

    # load necessary data
    for item in product.find_all('tr')[2:]:
        items = item.find_all('td')

        cards.append(
            {
                'continents': items[3].find('a').get('title'),
                'countries': items[0].find('a').get('title'),
                'rates': items[1].text.strip(),
                'total': items[2].text.strip().replace('+', '')
            }
        )
    print(product)


# get iso-3 from wikipedia html
def get_content_iso(url2, params=''):
    r_iso = requests.get(url2, headers=HEADER, params=params).text
    soup_iso = BeautifulSoup(r_iso, 'html.parser')
    product_iso = soup_iso.find_all('tbody')[2]
    global iso

    # load necessary data
    for item in product_iso.find_all('tr')[1:]:
        items_iso = item.find_all('td')

        iso.append(
            {
                'countries': items_iso[1].find('a').get('title'),
                'iso': items_iso[8].text.strip(),
            }
        )
        # print(iso)


# save dat into csv
def save_data(items, path):
    with open(path, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['continent', 'country', 'rate', 'total_murder'])
        for item in items:
            writer.writerow([item['continents'], item['countries'], item['rates'], item['total']])


# save iso data into csv
def save_data_iso(items_, path_):
    with open(path_, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['country', 'iso'])
        for item in items_:
            writer.writerow([item['countries'], item['iso']])


get_content(URL)
save_data(cards, CSV)

get_content_iso(URL2)
save_data_iso(iso, CSV2)
