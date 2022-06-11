import scrapy


class ApkCrawlerSpider(scrapy.Spider):
    name = 'apk_crawler'
    allowed_domains = ['apkleecher.com']
    start_urls = ['http://apkleecher.com/']

    def start_requests(self):
        return super().start_requests()

    def parse(self, response):
        pass
