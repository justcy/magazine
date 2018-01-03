import scrapy
import hashlib
from magazine.items import MagazineItem
from magazine.items import ArticleItem

from scrapy.http import Request


class QuotesSpider(scrapy.Spider):
    name = "duzhe"

    def start_requests(self):
        urls = [
            'http://www.52duzhe.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for book in response.xpath('//td[@class="time"]/a/@href').extract():
            yield response.follow(book, self.parse_book)

    def parse_book(self, response):
        book = MagazineItem()
        book['url'] = response.url
        title = response.xpath('//h1/text()').extract()
        book['title'] = title
        # book.year = title
        # book.number = title
        book['img'] = response.xpath('//div[contains(@class,"center")]/img/@src').extract()
        book['articleList'] = list()

        for article in response.xpath('//td/a/@href').extract():
            return Request(response.urljoin(article), meta={'book': book}, callback=self.parse_article)

            # yield {
            #         'title': response.xpath('//td[@class="title"]/a/text()').extract(),
            #         'author': response.xpath('//td[@class="author"]/text()').extract(),
            #         'source': response.xpath('//td[@class="source"]/text()').extract(),
            #     }

    def parse_article(self, response):
        book = response.meta['book']

        articleList = list(book['articleList'])

        article = ArticleItem()
        article['title'] = response.xpath('//h1/text()').extract()
        article['author'] = response.xpath("//span[@id='pub_date']/text()").extract()
        # article['category'] = response.xpath().extract()
        article['source'] = response.xpath("//span[@id='pub_date']/text()").extract()
        article['content'] = response.xpath("//p").extract()

        articleList.append(article)
        book['articleList'] =articleList
        return book
