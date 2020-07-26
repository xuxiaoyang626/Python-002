import lxml.etree
import pandas as pd
import re
import requests
from time import sleep
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs

base_url = 'https://maoyan.com/films?showType=3'
movie_url_prefix = 'https://maoyan.com/'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
header = {'user-agent':user_agent}

def parse_cookie_file(cookiefile):
    """
    Parse a cookies.txt file and return a dictionary of key value pairs compatible with requests.
    """
    cookies = {}
    with open (cookiefile, 'r') as fp:
        for line in fp:
            if not re.match(r'^\#', line):
                lineFields = line.strip().split('\t')
                cookies[lineFields[5]] = lineFields[6]
    return cookies
cookies = parse_cookie_file('cookies.txt')

def get_movie_urls(base_url, limit):
    """
    Go through the base url and construct movie detal page urls according to the limit number. 
    """
    urls = []
    response = requests.get(base_url, headers=header, cookies=cookies)
    bs_info = bs(response.text, 'html.parser')

    for tags in bs_info.find_all('div', attrs={'class': 'channel-detail movie-item-title'}, limit=limit):
        for atag in tags.find_all('a'):
            suffix = (atag.get('href'))
            url = urljoin(movie_url_prefix, suffix)
            urls.append(url)
    return urls

def get_movie_details(url):
    """
    Get film_name, plan_date and genre for each movie.
    """
    response = requests.get(url, headers=header, cookies=cookies)
    selector = lxml.etree.HTML(response.text)

    # 电影名称
    film_name = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/h1/text()')[0]
    print(f'电影名称: {film_name}')

    # 上映日期
    plan_date = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[3]/text()')[0]
    print(f'上映日期: {plan_date}')

    # 电影类型
    i = 1
    genre = ""
    while True:
        content = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[1]/a[' + str(i) + ']/text()')
        i += 1
        if len(content) > 0:
            genre += content[0].strip() + " "
        else:
            break
    print(f'类型：{genre}')

    return [film_name, plan_date, genre]

def write_to_file(data):
    """
    Write movie details to csv file.
    """
    movie = pd.DataFrame(data = data)
    movie.to_csv('./movie.csv', encoding='utf8', mode='a', index=False, header=False)

for url in get_movie_urls(base_url, 10):
    sleep(2)
    write_to_file(get_movie_details(url))
