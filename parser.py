import random
import requests
from bs4 import BeautifulSoup


def parser():
    request = requests.get(f'https://rt.pornhub.com/video?page={random.choice(range(1, 10))}')
    soap = BeautifulSoup(request.text, 'html.parser')
    all_links = soap.findAll('a', class_='linkVideoThumb')
    return 'https://rt.pornhub.com' + all_links[random.choice(range(1, 15))].get('href')


def search_parser(search):
    arr = []
    request = requests.get(f'https://rt.pornhub.com/video/search?search={search}&page={1}')
    soap = BeautifulSoup(request.text, 'html.parser')
    all_links = soap.findAll('a', class_='linkVideoThumb')
    for link in all_links:
        arr.append('https://rt.pornhub.com' + link.get('href'))
    print(len(arr))
    return arr[4: 30]





