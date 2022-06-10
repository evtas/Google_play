# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GooglePlayGamesItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    star_rating = scrapy.Field()
    download_times = scrapy.Field()
    content_rating = scrapy.Field()
    introduction = scrapy.Field()
    update_time = scrapy.Field()
    genre = scrapy.Field()
    url = scrapy.Field()





