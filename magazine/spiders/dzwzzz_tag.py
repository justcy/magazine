import scrapy
import hashlib
import re
from magazine.items import TagItem

from scrapy.http import Request


class DzwzzzTagSpider(scrapy.Spider):
    name = "dzwzzz_tags"
    allowed_domain = ['www.dzwzzz.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'magazine.dzwzzzPipelines.TagPipeline': 300,
        }
    }
    def start_requests(self):
        urls = [
            'https://www.dzwzzz.com/2018_21/index.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        tagItem = TagItem()
        tagList = response.xpath('//dt/span/text()').extract()
        for tag in tagList:
            tagItem['magazine_id'] = 1
            tagItem['tag_name'] = tag.strip()
            tagMd5 = hashlib.md5()
            tagMd5.update(tagItem['tag_name'])
            tagItem['tag_name_md5'] = tagMd5.hexdigest()
            yield tagItem
