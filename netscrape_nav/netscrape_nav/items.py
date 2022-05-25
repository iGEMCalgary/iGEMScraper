# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class WikiPage(scrapy.Item):
    url = scrapy.Field()
    pagetype = scrapy.Field()
    teamname = scrapy.Field()
    year = scrapy.Field()
    pagetext = scrapy.Field()


class NetscrapeNavItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
