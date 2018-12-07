from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print os.path.dirname(os.path.abspath(__file__))

execute(['scrapy','crawl','redis_dzwzzz_tags'])
execute(['scrapy','crawl','dzwzzz_details'])
execute(['scrapy','crawl','dzwzzz'])
