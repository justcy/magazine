import hashlib
from magazine.items import TagItem
from scrapy_redis.spiders import RedisSpider


class RedisDzwzzzTagSpider(RedisSpider):
    name = "redis_dzwzzz_tags"
    allowed_domain = ['www.dzwzzz.com']

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
