#-*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy
from magazine.items import ssqItem
class ssqSpider(scrapy.Spider):
    name = "ssq2"

    def start_requests(self):
        urls = [
            'http://www.cwl.gov.cn/kjxx/ssq/hmhz/index.shtml',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for page in response.xpath('//td/a[@class="z_num"]/@href').extract():
            yield response.follow(page, self.parse_page)
    def parse_page(self, response):
        for page in response.xpath('//td/a[@class="z_num"]/@href').extract():
            yield response.follow(page, self.parse_page)
        for number in response.xpath('//table[@class="hz"]/tbody/tr/td/a/@href').extract():
            yield response.follow(number, self.parse_number)
    def parse_number(self,response):
        item = ssqItem()
        # item['number'] = response.xpath('//li[@class="caizhong"]/span[1]/text()').extract()
        # item['opentime'] = response.xpath('//li[@class="caizhong"]/span[2]/text()').extract()

        number = response.xpath('//li[@class="caizhong"]/span[1]/text()').extract()
        opentime = response.xpath('//li[@class="caizhong"]/span[2]/text()').extract()
        item['number'] = number[0].decode('utf-8')[1:-1].encode('utf-8')
        item['opentime'] = opentime[0].decode('utf-8')[5:].encode('utf-8')
        item['red1'] = response.xpath('//li[@class="haoma3"]/span[1]/text()').extract()
        item['red2'] = response.xpath('//li[@class="haoma3"]/span[2]/text()').extract()
        item['red3'] = response.xpath('//li[@class="haoma3"]/span[3]/text()').extract()
        item['red4'] = response.xpath('//li[@class="haoma3"]/span[4]/text()').extract()
        item['red5'] = response.xpath('//li[@class="haoma3"]/span[5]/text()').extract()
        item['red6'] = response.xpath('//li[@class="haoma3"]/span[6]/text()').extract()
        item['blue'] = response.xpath('//li[@class="haoma3"]/span[7]/text()').extract()
        return item
