import scrapy
import hashlib
import re
from magazine.items import ContetItem
from scrapy_redis.spiders import RedisSpider


class RedisDzwzzzDetailsSpider(RedisSpider):
    name = "redis_dzwzzz_details"
    allowed_domain = ['www.dzwzzz.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'magazine.dzwzzzPipelines.ContentPipeline': 300,
        }
    }

    def parse(self, response):
        meta={"url":response.url}
        for book in response.xpath('//dd/span/a/@href').extract():
            yield response.follow(book, self.parse_book, meta=meta)

    def parse_book(self, response):
        bookUrl = response.meta['url']
        content = ContetItem()

        bookUrlMd5 = hashlib.md5()
        bookUrlMd5.update(bookUrl)
        content['book_id'] = bookUrlMd5.hexdigest()
        content['tag_id'] = 1
        content['cont_url'] = response.url
        content['cont_title'] = response.xpath('//h1/text()').extract()[0]
        contentList = response.xpath('//div[@id="smalllist"]/div/span/a/text()').extract()

        pattern = re.compile(ur'\d{2}\.')
        snoList = pattern.findall(content['cont_url'])
        content['cont_sno'] = snoList[0].replace('.', '')
        content['cont_author'] = response.xpath('//span[@id="pub_date"]/text()').extract()[0].replace("\n",
                                                                                                      " ").replace("\r",
                                                                                                                   " ")
        content['cont_source'] = response.xpath('//span[@id="media_name"]/text()').extract()[0].replace("\n",
                                                                                                        " ").replace(
            "\r", " ")
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
