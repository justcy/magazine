# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MagazineItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    img = scrapy.Field()
    year = scrapy.Field()
    number = scrapy.Field()
    pass

class ArticleItem(MagazineItem):
    title = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    pass



