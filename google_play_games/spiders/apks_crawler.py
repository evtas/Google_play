from tracemalloc import start
import scrapy
import psycopg2
from google_play_games.items import GooglePlayGamesItem

# BASE_URL = "https://apkpure.com/cn/search?q="
BASE_URL = "https://apkpure.com/cn/"

class ApksCrawlerSpider(scrapy.Spider):
    name = 'apks_crawler'
    allowed_domains = ['apkpure.com']

    # 获取游戏名
    conn = psycopg2.connect(database="google_play", user="postgres", password="binshao123", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    sql = "select name from google_play_games"
    cur.execute(sql)
    names = cur.fetchall() 
    conn.close()

    def start_requests(self):
        yield scrapy.Request(BASE_URL, self.parse, meta={'name': self.names}, dont_filter=True)

    def parse(self, response):
        pass
