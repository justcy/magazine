import pymongo
import json
import pymysql
from pymysql import connections

from scrapy.conf import settings

class MongoDBPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient(host=settings['MONGODB_SERVER'], port=settings['MONGODB_PORT'])
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGODB_DB']]
        self.coll = self.db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        isExist = self.coll.find_one(item)
        if isExist is None:
            postItem = dict(item)
            self.coll.insert(postItem)
            return item
class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='http://www.58ajp.com',user='root',passwd='FmODJhqZAzigvV%Wjp$1nkVknL9uq2HcV!f!O6Zl',db ='magazine')
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        print spider
        # name = item['name'][0]
        # kws = item['kws'][0]
        # sql ="insert into hehe(title,kws) VALUES(%s,%s)"
        # self.cursor.execute(sql,(name,kws,))
        # self.conn.commit()
        # return item
    def close_spider(self,spider):
        self.conn.close()
class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ",\n"
        self.file.write(line)
        return item