import scrapy
import hashlib
import re
import os
from magazine.items import ContetItem
from scrapy_redis.spiders import RedisSpider
from scrapy.utils.response import get_base_url


class RedisDzwzzzDetailsSpider(RedisSpider):
    name = "redis_dzwzzz_details"
    allowed_domain = ['www.dzwzzz.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'magazine.dzwzzzPipelines.ContentPipeline': 300,
        }
    }

    def parse(self, response):
        meta = {"url": response.url}

        contentList = response.xpath('//dd/span/a/@href').extract()
        if len(contentList) == 0:
            contentList = response.xpath('//td/a/@href').extract();
        for book in contentList:
            yield response.follow(book, self.parse_book, meta=meta)

    def parse_book(self, response):
        bookUrl = response.meta['url']
        content = ContetItem()

        bookUrlMd5 = hashlib.md5()
        bookUrlMd5.update(bookUrl)
        content['book_id'] = bookUrlMd5.hexdigest()
        content['magazine_id'] = 1
        tag = response.xpath('//div[@class="showList"]/h2/text()').extract()
        if len(tag) == 0:
            content['tag_id'] = response.xpath('//div[@class="openlist"]/span/text()').extract()[0];
        else:
            content['tag_id'] = tag[0]
        tagNameMd5 = hashlib.md5()
        tagNameMd5.update(content['tag_id'])
        content['tag_name_md5'] = tagNameMd5.hexdigest()

        content['cont_url'] = response.url
        content['cont_title'] = response.xpath('//h1/text()').extract()[0]

        menuList = response.xpath('//div[@class="sidebarBlock menuLayer"]/div/div/a/@href').extract()
        if len(menuList) == 0:
            menuList = response.xpath('//div[@id="smalllist"]/div/span/a/@href').extract()

        nowUrl = response.url[response.url.rfind('/', 1) + 1:]

        content['cont_sno'] = menuList.index(nowUrl) + 1

        newTypeAuther = response.xpath('//span[@id="pub_date"]/text()').extract()
        if len(newTypeAuther) == 0 :
            print response.xpath('//div[@class="title tcright"]/text()').extract()[0].replace("\n", " ").replace("\r", " ")
            autherSource = response.xpath('//div[@class="title tcright"]/text()').extract()[0].replace("\n", " ").replace("\r", " ").split(u'\xa0\xa0\xa0\xa0')
            print autherSource

            auther = autherSource[0]
            soutrce = autherSource[1]
        else:
            auther = response.xpath('//span[@id="pub_date"]/text()').extract()[0].replace("\n", " ").replace("\r", " ")
            soutrce = response.xpath('//span[@id="media_name"]/text()').extract()[0].replace("\n", " ").replace("\r",
                                                                                                                " ")
        content['cont_author'] = auther
        content['cont_source'] = soutrce
        content['cont_detail'] = response.xpath('//div[@class="blkContainerSblkCon"]/p').extract()

        contUrlMd5 = hashlib.md5()
        contUrlMd5.update(content['cont_url'])
        content['cont_url_md5'] = contUrlMd5.hexdigest()
        yield content

        #     book['url'] = response.url
        #     title = response.xpath('//h1/text()').extract()
        #     book['title'] = title
        #     # book.year = title
        #     # book.number = title
        #     book['img'] = response.xpath('//div[contains(@class,"center")]/img/@src').extract()
        #     book['articleList'] = list()
        #
        #     for article in response.xpath('//td/a/@href').extract():
        #         return Request(response.urljoin(article), meta={'book': book}, callback=self.parse_article)
        #
        #         # yield {
        #         #         'title': response.xpath('//td[@class="title"]/a/text()').extract(),
        #         #         'author': response.xpath('//td[@class="author"]/text()').extract(),
        #         #         'source': response.xpath('//td[@class="source"]/text()').extract(),
        #         #     }
        #
        # def parse_article(self, response):
        #     book = response.meta['book']
        #
        #     articleList = list(book['articleList'])
        #
        #     article = ArticleItem()
        #     article['title'] = response.xpath('//h1/text()').extract()
        #     article['author'] = response.xpath("//span[@id='pub_date']/text()").extract()
        #     # article['category'] = response.xpath().extract()
        #     article['source'] = response.xpath("//span[@id='pub_date']/text()").extract()
        #     article['content'] = response.xpath("//p").extract()
        #
        #     articleList.append(article)
        #     book['articleList'] =articleList
        #     return book
