import requests, re
import json
from multiprocessing import Pool
from bs4 import BeautifulSoup
import time

MULTI = True
DATA_FILENAME = 'data.json'

STEP = 50
MAX_COUNT = 50
'''
Url is typically like https://myanimelist.net/topanime.php?limit=50
'''
SELECTOR =  ".ranking-list td.title.al.va-t.word-break .detail .hoverinfo_trigger"
BASE_URL = 'https://myanimelist.net/topanime.php?limit='
GENRE_ITEMPROP = 'genre'
anime_data = {}


def load_data(filename):
    with open(filename) as data_file:
        json_data = json.load(data_file)
    return json_data['content']


def scrape_top_entries(data):
    count = 0
    results = []
    while count <= MAX_COUNT:
        current_url = f'{data["url"]}{count}'
        current_selector = data['selector']
        res = requests.get(current_url)
        soup = BeautifulSoup(res.content, 'lxml')
        tmp = soup.select(current_selector)
        results.append(tmp)
        count += STEP

    flat_list = [item for sublist in results for item in sublist]

    for t in flat_list:
        print(t.string)


def scrape_batch_top_entires(url):

    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    tmp = soup.select(SELECTOR)
    for t in tmp:
        page = requests.get(t['href'])
        soup = BeautifulSoup(page.content, 'lxml')
        genres_raw = soup.findAll('span', itemprop=GENRE_ITEMPROP)
        genres = list(map(lambda x: x.string, genres_raw))
        print(f'url: {t["href"]} # name: {t.string} # genres:{",".join(genres)}')
        print('#########################')


def multi():
    start = time.time()
    count = 0
    urls_arr = []
    while count <= MAX_COUNT:
        urls_arr.append(f'{BASE_URL}{count}')
        count += 50

    p = Pool(4)
    p.map(scrape_batch_top_entires, urls_arr)
    p.terminate()
    p.join()
    end = time.time()
    print(f'time is {end - start}')


def single():
    start = time.time()
    data = load_data(DATA_FILENAME)[0]
    scrape_top_entries(data)
    end = time.time()
    print(f'time is {end - start}')


def main():

    if MULTI:
        multi()
    else:
        single()


if __name__ == "__main__":

    main()