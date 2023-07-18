import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'cookie': '',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/111.0.0.0 Safari/537.36'
}

sess = requests.Session()
names_and_nicknames = []
for i in range(1, 44):
    resp = sess.get(f'https://istina.msu.ru/organizations/department/276546/workers/?p={i}', headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')
    cards = soup.find_all('div', attrs={'class': "worker_short span-24 last"})
    for card in cards:
        name = card.find('h3').find('a').text
        try:
            nickname = card.find('span', attrs={'class': "detail_label"}).text
        except:
            nickname = card.find('h3').find('a')['href']
        names_and_nicknames.append([name, nickname])
df = pd.DataFrame(names_and_nicknames, columns=['names', 'nicknames'])
df.to_csv('names_and_links_istina_workers.csv')
