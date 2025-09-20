# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PlaywrightScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    _id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    subtitle = scrapy.Field()

#test