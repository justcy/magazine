import scrapy


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
    def parse_book(self,response):
        print response.url
        yield {
                'title': response.xpath('//td[@class="title"]/a/text()').extract(),
                'author': response.xpath('//td[@class="author"]/text()').extract(),
                'source': response.xpath('//td[@class="source"]/text()').extract(),
            }
