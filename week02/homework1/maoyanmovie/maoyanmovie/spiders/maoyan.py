# -*- coding: utf-8 -*-
import re
import scrapy
import lxml.etree
from urllib.parse import urljoin
from maoyanmovie.items import MaoyanmovieItem
from scrapy.selector import Selector

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    movie_url_prefix = 'https://maoyan.com'
    start_urls = ['https://maoyan.com/films?showType=3']
    num_of_movies = 10

    def parse_cookie_file(self, cookiefile):
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

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        cookies = self.parse_cookie_file('cookies.txt')
        yield scrapy.Request(url=url, cookies=cookies, callback=self.parse)

    def get_movie_urls(self, response, limit):
        """
        Go through the base url and construct movie detal page urls according to the limit number. 
        """
        urls = []
        movies = Selector(response=response).xpath('//div[@class="channel-detail movie-item-title"]')
        for movie in movies:
            if len(urls) >= limit:
                break
            suffix = movie.xpath('./a/@href').get()
            url = urljoin(self.movie_url_prefix, str(suffix))
            urls.append(url)
        
        return urls

    def get_movie_details(self, response):
        movie = Selector(response=response).xpath('//div[@class="movie-brief-container"]')

        film_name = movie.xpath('./h1[@class="name"]/text()').get()
        print(f'电影名称: {film_name}')

        plan_date = movie.xpath('./ul/li[last()]/text()').get()
        print(f'上映日期: {plan_date}')

        genre = ""
        genres = movie.xpath('./ul/li/a/text()').getall()
        for g in genres:
            genre += g + " "
        print(f'类型：{genre}')

        return [film_name, plan_date, genre]

    def parse(self, response):
        urls = self.get_movie_urls(response, self.num_of_movies)
        for url in urls:
            item = MaoyanmovieItem()
            yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse2)

    def parse2(self, response):
        item = response.meta['item']
        details = self.get_movie_details(response)
        item['title'] = details[0]
        item['date'] = details[1]
        item['genre'] = details[2]
        yield item




