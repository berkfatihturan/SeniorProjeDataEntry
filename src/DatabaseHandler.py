import pymongo
import config


class DatabaseHandler:
    def __int__(self):
        self.client = pymongo.MongoClient(config.DB_URI)
        self.mydb = self.client[config.DB_NAME]
        

    def add_data(self, data):
        self.mycoll = self.mydb[config.DB_COLLECTION]
        self.mycoll.insert_one(data)
        print("Veri ekleme tamamlandı.")
