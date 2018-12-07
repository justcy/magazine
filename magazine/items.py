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

class BookItem(scrapy.Item):
    magazine_id = scrapy.Field()
    book_name = scrapy.Field()
    book_cover = scrapy.Field()
    book_year = scrapy.Field()
    book_sno = scrapy.Field()
    book_url = scrapy.Field()
    book_url_md5 = scrapy.Field()
    pass
class ArticleItem(MagazineItem):
    title = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
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



