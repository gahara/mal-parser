import requests
import json
from multiprocessing import Pool
from bs4 import BeautifulSoup

MULTI = False
DATA_FILENAME = 'data.json'

BASE_URL = 'https://myanimelist.net/topanime.php'
STEP = 50
MAX_COUNT = 300
'''
Url is typically like https://myanimelist.net/topanime.php?limit=50
'''


def load_data(filename):
    with open(filename) as data_file:
        json_data = json.load(data_file)
    return json_data['content']


def scrape(url):
    count = 0
    results = []
    while count <= MAX_COUNT:
        current_url = f'{url["url"]}{count}'
        current_selector = url['selector']
        res = requests.get(current_url)
        soup = BeautifulSoup(res.content, 'lxml')
        tmp = soup.select(current_selector)
        results.append(tmp)
        count += STEP
    flat_list = [item for sublist in results for item in sublist]

    for t in flat_list:
        print(t.string)


def main():
    if MULTI:
        urls_from_file = load_data(DATA_FILENAME)
        p = Pool(4)
        p.map(scrape, urls_from_file)
        p.terminate()
        p.join()
    else:
        urls_from_file = load_data(DATA_FILENAME)
        for url in urls_from_file:
            scrape(url)


if __name__ == "__main__":

    main()