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
sess.get('https://www.phys.msu.ru/rus/about/staff/', headers=headers)
all_names = []
with open('letters.txt', 'r') as f:
    letters_code = f.readlines()
name_and_link = []
for letter in letters_code:
    resp = sess.get(f'https://www.phys.msu.ru/rus/about/staff/index.php?f={letter.strip()}')
    soup = BeautifulSoup(resp.text, 'lxml')
    tables = soup.find_all('table', attrs={})
    names_and_work = tables[1].find_all('td')
    for i in range(0, len(names_and_work), 2):
        name = names_and_work[i].find('a').text
        link = f"https://www.phys.msu.ru/{names_and_work[i].find('a')['href']}"
        name_and_link.append([name, link])
df = pd.DataFrame(name_and_link, columns=['name', 'link'])
df.to_csv('names_and_links.csv')
# with open('names.txt', 'a', encoding='UTF-8') as f:
#     for name, link in name_and_link:
#         f.write(f'{name}, {link}\n')
