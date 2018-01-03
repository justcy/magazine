import pymongo

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
