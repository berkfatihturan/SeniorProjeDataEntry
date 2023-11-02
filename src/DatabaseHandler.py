import pymongo
import config
from src.EmailSender import EmailSender

class DatabaseHandler:

    def __init__(self):
        self.client = pymongo.MongoClient(config.DB_URI)
        self.mydb = self.client[config.DB_NAME]
        self.mycoll = self.mydb[config.DB_COLLECTION]
        self.MsgSender = EmailSender()

    def add_data(self, data):
        try:
            self.mycoll.insert_one(data)
        except:
            self._send_err()
        else:
            print(F"Data retrieval successful...[COMPLETED]")

    def _send_err(self):
        err_str = "[DATA EKLENEMEDİ]"
        print(err_str)
        self.MsgSender.send_email_to_all(msg_code=4, err_msg=str(err_str))