import scrapy
from magazine.items import ssqItem

class QuotesSpider(scrapy.Spider):
    name = "ssq"

    def start_requests(self):
        urls = [
            'https://datachart.500.com/ssq/history/newinc/history_same.php?start=03001&end=17153',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for tr in response.xpath('//tbody[@id="tdata"]/tr'):
            print tr
            item = ssqItem()

            item['number'] = tr.xpath('//td[2]/text()').extract()
            item['red'] = tr.xpath('//td[@class="t_cfont2"]/text()').extract()
            item['blue'] = tr.xpath('//td[@class="t_cfont4"]/text()').extract()
            return item
