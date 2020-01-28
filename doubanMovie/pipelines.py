# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request 

class DoubanmoviePipeline(object):
    def process_item(self, item, spider):
        return item

class MyImagesPipeline(ImagesPipeline):
    # yield meta for file_path() function
    def get_media_requests(self, item, info): 
        for url in item['url']: 
            yield Request(url, meta={'item': item, 'index':item['url'].index(url)})

    # rename the image
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        index = request.meta['index']

        image_name = item['img_name'][index]
        return 'full/%s.jpg' % (image_name)


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