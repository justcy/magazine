# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MagazineItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class ssqItem(scrapy.Item):
    _id = scrapy.Field()
    number = scrapy.Field()
    opentime = scrapy.Field()
    red1 = scrapy.Field()
    red2 = scrapy.Field()
    red3 = scrapy.Field()
    red4 = scrapy.Field()
    red5 = scrapy.Field()
    red6 = scrapy.Field()
    blue = scrapy.Field()
