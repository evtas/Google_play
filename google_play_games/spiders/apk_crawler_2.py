import scrapy
import psycopg2

BASE_URL = "https://apkcombo.com/zh/"

class ApkCrawler2Spider(scrapy.Spider):
    name = 'apk_crawler_2'
    allowed_domains = ['apkcombo.com']
    start_urls = ['https://apkcombo.com/zh/']

    # # 获取游戏名 被网站ban了
    # conn = psycopg2.connect(database="google_play", user="postgres", password="binshao123", host="127.0.0.1", port="5432")
    # cur = conn.cursor()
    # sql = "select name from google_play_games"
    # cur.execute(sql)
    # names = cur.fetchall() 
    # conn.close()

    # 获取url
    conn = psycopg2.connect(database="google_play", user="postgres", password="binshao123", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    sql = "select url from google_play_games"
    cur.execute(sql)
    urls = cur.fetchall() 
    conn.close()


    def start_requests(self):
        for url in self.urls:
            origin_url = url
            url = "https://apkcombo.com/zh/" + url[0][46:]
            yield scrapy.Request(url, callback=self.parse, meta={'origin_url': origin_url})

    def parse(self, response):
        pass