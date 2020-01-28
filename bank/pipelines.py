# pipelines to insert the data into mongodb
import pymongo
from scrapy.conf import settings

class BankPipeline(object):
    def __init__(self):
        # connect database
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])

        # using name and password to login mongodb
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])

        # handle of the database and collection of mongodb
        self.db = self.client[settings['MONGO_DB']]
        self.coll = self.db[settings['MONGO_COLL']]

    def process_item(self, item, spider):
        postItem = dict(item)
        self.coll.insert(postItem)
        return item