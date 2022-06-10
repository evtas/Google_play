import scrapy
import psycopg2


class DetailsCrawlerSpider(scrapy.Spider):
    name = 'details_crawler'
    allowed_domains = ['play.google.com']

    conn = psycopg2.connect(database="google_play", user="postgres", password="binshao123", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    sql = "select url from google_play_games"
    cur.execute(sql)
    urls = cur.fetchall()
    print(urls)

    start_urls = ['http://play.google.com/']

    def start_requests(self):
        pass


    def parse(self, response):
        pass
