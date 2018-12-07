import scrapy
import hashlib
import re
from magazine.items import BookItem

from scrapy.http import Request


class DzwzzzSpider(scrapy.Spider):
    name = "dzwzzz"
    allowed_domain = ['www.dzwzzz.com']

    def start_requests(self):
        urls = [
            'https://www.dzwzzz.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for book in response.xpath('//td[@class="time"]/a/@href').extract():
            yield response.follow(book, self.parse_book)

    def parse_book(self, response):
        book = BookItem()

        book['magazine_id']  = 1
        book['book_url'] = response.url
        book['book_name'] =response.xpath('//h1/text()').extract()[0]
        cover = response.xpath('//div[@class="sidebar"]/div/img/@src').extract()
        if len(cover) == 0:
            cover = response.xpath('//div[@id="content"]/div/div/img/@src').extract()[0]
            book['book_cover'] = self.allowed_domain[0]+"/"+cover
        else:
            book['book_cover'] = cover[0].replace('..', self.allowed_domain[0])

        pattern = re.compile(ur'(\d{4})')
        year = pattern.findall(book['book_url'])
        book['book_year'] = year[0]
        pattern = re.compile(ur'_\d{2}')
        sno = pattern.findall(book['book_url'])
        book['book_sno'] = sno[0].replace('_','')

        bookUrlMd5 = hashlib.md5()
        bookUrlMd5.update(book['book_url'])
        book['book_url_md5'] = bookUrlMd5.hexdigest()
        return book

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
