#-*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy
from magazine.items import ssqItem
import hashlib
class ssqSpider(scrapy.Spider):
    name = "ssq3"

    def start_requests(self):
        urls = [
            'http://kaijiang.500.com/ssq.shtml',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for page in response.xpath('//span[@class="iSelectBox"]/div/a/@href').extract():
            yield response.follow(page, self.parse_number)
    def parse_number(self,response):
        item = ssqItem()
        opentime = response.xpath('//span[@class="span_right"]/text()').extract_first()
        item['number'] = response.xpath('//span/a/font/strong/text()').extract_first()
        item['opentime'] = opentime.decode('utf-8')[5:15].encode('utf-8').replace('年',"-").replace('月',"-").replace('日',"")
        item['red1'] = response.xpath('//div[@class="ball_box01"]/ul/li[1]/text()').extract_first()
        item['red2'] = response.xpath('//div[@class="ball_box01"]/ul/li[2]/text()').extract_first()
        item['red3'] = response.xpath('//div[@class="ball_box01"]/ul/li[3]/text()').extract_first()
        item['red4'] = response.xpath('//div[@class="ball_box01"]/ul/li[4]/text()').extract_first()
        item['red5'] = response.xpath('//div[@class="ball_box01"]/ul/li[5]/text()').extract_first()
        item['red6'] = response.xpath('//div[@class="ball_box01"]/ul/li[6]/text()').extract_first()
        item['blue'] = response.xpath('//div[@class="ball_box01"]/ul/li[7]/text()').extract_first()
        m = hashlib.md5()
        m.update(item['number'])
        item['_id'] = m.hexdigest()
        return item

