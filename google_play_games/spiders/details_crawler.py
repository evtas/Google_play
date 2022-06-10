import scrapy


class DetailsCrawlerSpider(scrapy.Spider):
    name = 'details_crawler'
    allowed_domains = ['play.google.com']
    start_urls = ['http://play.google.com/']

    def start_requests(self):
        pass


    def parse(self, response):
        pass
