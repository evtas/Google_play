from subprocess import call
import scrapy
import psycopg2


class ImageCrawlerSpider(scrapy.Spider):
    name = 'image_crawler'
    allowed_domains = ['play.google.com']
    start_urls = ['http://play.google.com/']

    def start_requests(self):
        # 获取游戏详情页url
        conn = psycopg2.connect(database="google_play_games", user="postgres", password="binshao123", host="127.0.0.1", port="5432")
        cur = conn.cursor()
        sql = "select url from games_games"
        cur.execute(sql)
        urls = cur.fetchall()

        for url in urls:
            url = url[0]
            yield scrapy.Request(url, callback=self.parse, meta={'url': url})

    def parse(self, response):
        print(response.meta['url'])
        image = response.xpath("//img[@class='T75of QhHVZd']/@src").extract_first()

        conn_2 = psycopg2.connect(database="google_play_games", user="postgres", password="binshao123", host="127.0.0.1", port="5432")
        cur_2 = conn_2.cursor()
        cur_2.execute("update games_games set image = %s where url = %s", (image, response.meta['url']))
        conn_2.commit()
