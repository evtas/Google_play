from curses import meta
from gc import callbacks
from urllib.request import Request
import scrapy
import re
from google_play_games.items import GooglePlayGamesItem
import logging
from .utils import xstr
from google_play_games.settings import REGION

BASE_URL = "https://play.google.com"

class GamesCrawlerSpider(scrapy.Spider):
    name = 'games_crawler'
    allowed_domains = ['play.google.com']

    def start_requests(self):
        urls = ['https://play.google.com/store/games?gl=' + country for country in REGION]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'gl': url[-2:]})

    # 爬取详情页的代码demo
    def parse(self, response):
        print(response.text)
        genre_urls = []
        for each in response.xpath("//div[@class='ULeU3b']/a/@href"):
            genre_urls.append(BASE_URL + each.extract() + "&gl=" + response.meta['gl'])
            # genre_urls.append(BASE_URL + each.extract())

        for genre_url in genre_urls:
            yield scrapy.Request(genre_url, self.parse_genre)
    
    def parse_genre(self, response):
        for each in response.xpath("//a/@href"):
            detail_url = each.extract()
            # print(each.extract())
            if detail_url[:20] == "/store/apps/details?":

                detail_url = BASE_URL + detail_url
                yield scrapy.Request(detail_url, self.parse_detail)

    def parse_detail(self, response):
        print(response.text)

        item = GooglePlayGamesItem()

        name = response.xpath("//h1[@itemprop='name']/span/text()").extract_first()
        author = response.xpath("//div[@class='Vbfug auoIOc']/a/span/text()").extract_first()
        star_rating = response.xpath("//div[@itemprop='starRating']/div/text()").extract_first()
        download_times = response.xpath("//div[@class='w7Iutd']/div[2]/div/text()").extract_first()
        content_rating = response.xpath("//span[@itemprop='contentRating']/span/text()").extract_first()[10:]
        introduction = response.xpath("//div[@class='bARER']").xpath('string(.)').extract_first()
        update_time = response.xpath("//div[@class='xg1aie']/text()").extract_first()
        genre = response.xpath("//div[@itemprop='genre']/span/text()").extract_first()

        item['name'] = xstr(name)
        item['author'] = xstr(author)
        item['star_rating'] = xstr(star_rating)
        item['download_times'] = xstr(download_times)
        item['content_rating'] = xstr(content_rating)
        item['introduction'] = xstr(introduction)
        item['update_time'] = xstr(update_time)
        item['genre'] = xstr(genre)

        # print(name)
        return item      
