import pymongo
import config


class DatabaseHandler:
    def __int__(self):
        self.client = pymongo.MongoClient(config.DB_URI)
        self.mydb = self.client[config.DB_NAME]
        self.mycoll = self.mydb[config.DB_COLLECTION]

    def add_data(self, data):
        self.mycoll.insert_one(data)
        print("Veri ekleme tamamlandı.")
