import pymongo
import config

client = pymongo.MongoClient(config.DB_URI)
mydb = self.client[config.DB_NAME]
mycoll = mydb[config.DB_COLLECTION]
class DatabaseHandler:
    def __int__(self):
        pass

    def add_data(self, data):
        mycoll.insert_one(data)
        print("Veri ekleme tamamlandı.")
