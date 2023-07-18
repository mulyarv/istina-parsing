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
name_and_link = []
sess = requests.Session()
resp = sess.get('http://www.dubinushka.ru/plist.php?pred=1', headers=headers)
soup = BeautifulSoup(resp.text, 'lxml')
names = soup.find('div', attrs={'class': 'entry'}).find_all('a', href=True)
for name in names:
    name_and_link.append([name.text,name["href"]])
df = pd.DataFrame(name_and_link, columns=['name', 'link'])
df.to_csv('names_and_links_dub.csv')
