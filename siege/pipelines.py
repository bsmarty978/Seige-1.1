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
    CMcollection_name = "AllMatches"

    New_Completedmatch = 0
    New_UpcomingMatch  = 0
    Updated_Match      = 0 

    ListOfNew = []
    ListOfUpdated = []


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
            lg.warning(f'----------------------------[ 🕷           Current            🕷 ]-----------------------------')
        elif spider.name == "allmatches":
            lg.warning(f'----------------------------[ 🕷 Match Result Will be updated 🕷 ]-----------------------------')
            lg.warning(f'----------------------------[ 🕷             All              🕷 ]-----------------------------')
        else:
            lg.warning(f'----------------------------[ 😐 Spider is DEAD 😐 ]------------------------------------------')

    def close_spider(self, spider):
        self.client.close()
        lg.info('--------------------------------------------------------------------------------------')
        lg.info(f'#############[ Upcoming Match : {self.New_UpcomingMatch} ]####################')
        lg.info(f'#############[ Completed Match : {self.New_Completedmatch} ]####################')
        lg.info(f'{self.ListOfNew}')
        lg.info(f'#############[ Updated Match : {self.Updated_Match} ]####################')
        lg.info(f'{self.ListOfUpdated}')
        lg.info('--------------------------------------------------------------------------------------')
        self.New_UpcomingMatch  = 0
        self.Updated_Match      = 0 
        self.New_Completedmatch = 0
        self.ListOfNew = []
        self.ListOfUpdated = []

    def process_item(self, item, spider):
        if spider.name=="upcomingm":
            upcomingCollection = self.db[self.UPcollection_name]
            upcomingCollection.insert(item)
            self.New_UpcomingMatch +=1
            return item

        elif spider.name in ["matches","allmatches"]:
            completedCollection = self.db[self.CMcollection_name]
            match_looup = completedCollection.find({"match_id":item["match_id"]})
            if match_looup.count()==1:
                if item["stats"]:
                    if not match_looup[0]["stats"]:
                        # match_looup.update_one({"match_id":item["match_id"]},{"$set":{"stats": item["stats"]}})  #NOTE: Updating on by one

                        #NOTE: Updating whole by deleting old and inserting new doc.
                        completedCollection.delete_one({"match_id":item["match_id"]})
                        completedCollection.insert(item)

                        lg.warning(f'[{item["match_id"]}]: Stats Updated')
                        self.ListOfUpdated.append(item["match_id"])

                        self.Updated_Match += 1
                    else:
                        lg.warning(f'[{item["match_id"]}]: Already in collection')
                else:
                    lg.warning(f'[{item["match_id"]}]: Already in collection')

            else:
                completedCollection.insert(item)
                self.New_Completedmatch += 1
                self.ListOfNew.append(item["match_id"])
            return item

        else:
            return item
