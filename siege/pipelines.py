# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import logging as lg

class UpcomingMatchPipeline:
    UPcollection_name = "UpcomingMatches"
    CMcollection_name = "Matches"

    New_Completedmatch = 0
    New_UpcomingMatch  = 0
    Updated_Match      = 0 


    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri
        # self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI')
            # mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )
        

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client["SiegeTest"]
        lg.warning(f'----------------------------[ 🕷 {spider.name} 🕷 ]-----------------------------')
        if spider.name == "upcomingm":
            try:
                self.db[self.UPcollection_name].drop()
            except:
                # lg.warning(f'----------------------------[Started >> {spider.name}]-----------------------------')
                pass
        elif spider.name == "matches":
            lg.warning(f'----------------------------[ 🕷 Match Result Will be updated 🕷 ]-----------------------------')
        else:
            lg.warning(f'----------------------------[ 😐 Spider is DEAD 😐 ]------------------------------------------')

    def close_spider(self, spider):
        self.client.close()
        lg.info('--------------------------------------------------------------------------------------')
        lg.info(f'#############[ Upcoming Match : {self.New_UpcomingMatch} ]####################')
        lg.info(f'#############[ Completed Match : {self.New_Completedmatch} ]####################')
        lg.info(f'#############[ Updated Match : {self.Updated_Match} ]####################')
        lg.info('--------------------------------------------------------------------------------------')
        self.New_UpcomingMatch  = 0
        self.Updated_Match      = 0 
        self.New_Completedmatch = 0

    def process_item(self, item, spider):
        if spider.name=="upcomingm":
            upcomingCollection = self.db[self.UPcollection_name]
            upcomingCollection.insert(item)
            self.New_UpcomingMatch +=1
            return item

        elif spider.name == "matches":
            completedCollection = self.db[self.CMcollection_name]
            if completedCollection.find({"match_id":item["match_id"]}).count()==1:
                lg.warning(f'[{item["match_id"]}]: Already in collection')
            else:
                completedCollection.insert(item)
                self.New_Completedmatch += 1
            return item

        else:
            return item
class CompletedMatchPipeline:
    UPcollection_name = "UpcomingMatches"
    CMcollection_name = "Matches"

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri
        # self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI')
            # mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )
        

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client["SiegeTest"]
        # lg.warning(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>[{spider}]')
        # print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>[{spider}]')
        # try:
        #     self.db[self.UPcollection_name].drop()
        # except:
        #     pass

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        try:
            spiderconditions = item["stats"]
            return item
        except KeyError:
            upcomingCollection = self.db[self.UPcollection_name]
            if upcomingCollection.find({"match_id":item["match_id"]}).count:
                lg.warning(f'[{item["match_id"]}]: Already in collection')
            else:
                upcomingCollection.insert(item)
            return item
