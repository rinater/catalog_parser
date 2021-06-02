# prerequisites : python 3.6.1 or higher

import csv
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from datetime import datetime

art = ''
CSV = art + '_parsed.csv'
HOST = 'https://lunda.ru/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}


def new_url(art=''):
    URL = 'https://lunda.ru/search/?textPattern=' + art
    return URL


URL = new_url()


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params,timeout=(3.05, 500))
    return r

def get_content(html):
    html = get_html(html)
    soup = BeautifulSoup(html.text, features='lxml')
    table = soup.find_all('table')[1]

    output_rows = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text.strip())
            output_row = list(filter(None, output_row))
        output_rows.append(output_row)
    # remove empty lists from nested list
    output_rows = [x for x in output_rows if x]
    print(output_rows)
    # sort by min price
    max(output_rows, key=lambda x: float(x[4].replace(',', '.').replace(' ', '')))
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['Артикул', 'Код', 'Ду, мм', 'Рабочее давление, бар', 'Цена сайта с НДС, руб/шт', 'На складе, шт'])
        for i in range(len(output_rows)):
            if art in output_rows[i]:
                minimal_price =min(output_rows, key=lambda x: float(x[4].replace(',', '.').replace(' ', '')))
        writer.writerow(minimal_price)

        now = datetime.now()
        writer.writerow(['Минимиальная цена на:', now.strftime("%d/%m/%Y %H:%M:%S"), ])

# КШТ 60.103.065.А


art = input('введите артикул: ')
art = art.strip()
URL = new_url(art)

html = get_html(URL)


s = HTMLSession()
response = s.get(URL)
response.html.render()
to_parse =''
for link in response.html.links:
    if 'product' in link and 'c9768' not in link and 'c11456' not in link:
        to_parse = link[1:]
link_to_parse = HOST+to_parse
print(link_to_parse)
#get_content(link_to_parse)
get_content(link_to_parse)