import json
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
            print(f"Data has been successfully scraped...[{data['İlan No']}]")
            self.mycoll.insert_one(data)
        except:
            self._send_err()
        else:
            print(F"Data retrieval successful...[COMPLETED]")

    def _send_err(self):
        err_str = "[DATA EKLENEMEDİ]"
        print(err_str)
        self.MsgSender.send_email_to_all(msg_code=config.MSG_CODE_DATA_ERR, err_msg=str(err_str))


class StateSaver:
    def __init__(self):
        self.file_path = config.SAVE_FILE_PATH

    def get_last_position(self):
        global last_position
        try:
            with open(self.file_path, "r") as file:
                last_position = int(json.load(file)["town_code"])
        except FileNotFoundError:
            # If the file is not found or it's the first run, set the last_position to 0
            last_position = 0
        finally:
            return last_position

    def save_last_position(self, town_code,counter):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)

            # If no error occurs, update the last_position
            with open(self.file_path, "w") as file:
                data["town_code"] = town_code
                data["counter"] = counter
                json.dump(data, file)
        except Exception as e:
            print(f"An error occurred: {e}")
