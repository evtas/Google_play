import scrapy
import psycopg2
from google_play_games.items import GooglePlayGamesItem
from .utils import xstr

BASE_URL = "https://play.google.com"

class RelativeCrawlerSpider(scrapy.Spider):
    name = 'relative_crawler'
    allowed_domains = ['play.google.com']
    # 获取游戏详情页url
    conn = psycopg2.connect(database="google_play", user="postgres", password="binshao123", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    sql = "select url from google_play_games limit 1762"
    cur.execute(sql)
    urls = cur.fetchall()

    start_urls = []
    for url in urls:
        start_urls.append(url[0])

    def parse(self, response):
        for each in response.xpath("//a/@href"):
            detail_url = each.extract()
            # print(each.extract())
            if detail_url[:20] == "/store/apps/details?":
                detail_url = BASE_URL + detail_url
                yield scrapy.Request(detail_url, self.parse_detail)

    def parse_detail(self, response):
        item = GooglePlayGamesItem()

        name = response.xpath("//h1[@itemprop='name']/span/text()").extract_first()
        author = response.xpath("//div[@class='Vbfug auoIOc']/a/span/text()").extract_first()
        star_rating = response.xpath("//div[@itemprop='starRating']/div/text()").extract_first()
        download_times = response.xpath("//div[@class='w7Iutd']/div[2]/div/text()").extract_first()
        content_rating = response.xpath("//span[@itemprop='contentRating']/span/text()").extract_first()[10:]
        introduction = response.xpath("//div[@class='bARER']").xpath('string(.)').extract_first()
        update_time = response.xpath("//div[@class='xg1aie']/text()").extract_first()
        genre = response.xpath("//div[@itemprop='genre']/span/text()").extract_first()
        url = response.url

        item['name'] = xstr(name)
        item['author'] = xstr(author)
        item['star_rating'] = xstr(star_rating)
        item['download_times'] = xstr(download_times)
        item['content_rating'] = xstr(content_rating)
        item['introduction'] = xstr(introduction)
        item['update_time'] = xstr(update_time)
        item['genre'] = xstr(genre)
        item['url'] = xstr(url)

        return item
