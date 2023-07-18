import requests
from bs4 import BeautifulSoup
import pandas as pd
from threading import Thread
import time

info_about_student = []
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


def do_flag_2(name, nickname):
    global info_about_student
    global headers
    sess = requests.Session()
    if 'workers' not in nickname:
        all_articles = ''
        resp = sess.get(f'https://istina.msu.ru/profile/{nickname}', headers=headers)
        try:
            soup = BeautifulSoup(resp.text, 'lxml')
            activity = soup.find('div', attrs={'class': 'span-24 last'}).find('ul', attrs={'class': 'clear'})
            sections = activity.find_all('li')
            for section_index in range(0, 1):
                years = sections[section_index].find_all('ul', attrs={'class': 'activity'})
                for year in years:
                    if int(year['data-year']) > 2021:
                        articles_rows = year.find_all('li')
                        article = f"{year['data-year']} "
                        for row in articles_rows:
                            article += f"{row.find('a').text} "
                        all_articles += f'{article}\n'
        except:
            pass
        if all_articles != '':
            info_about_student.append([name, nickname, all_articles])


df = pd.read_csv('names_and_links_istina_workers.csv')
nicknames = df['nicknames']
threads = []
index = 0
number_of_threads = 10

max_len = len(df['names'])
for i in range(0, max_len, number_of_threads):
    if i + number_of_threads < max_len:
        num_of_tr_val = number_of_threads
    else:
        num_of_tr_val = max_len - i

    for j in range(0, num_of_tr_val):
        try:
            th = Thread(target=do_flag_2,
                        args=(df['names'][i + j], df['nicknames'][i + j]))
            th.start()
            th.join()
        except Exception as ex:
            print(ex)
            print(f"Ошибка: номер работника: {i+j},имя работника: {df['names'][i + j]}")
    index += num_of_tr_val
    print(f"{index}/{len(df['names'])}")
df2 = pd.DataFrame(info_about_student, columns=['names', 'nicknames', 'articles'])
df2.to_csv('istina_workers_enhanced.csv')

