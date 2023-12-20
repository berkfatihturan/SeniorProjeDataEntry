from src.WebScraper import WebScraper
from src.EmailSender import EmailSender
import config

url = config.BASE_URL
print(open('data/header.txt','r').read())
CarScraper = WebScraper(url=url)
try:
    CarScraper.start_scrapping()
except Exception as e:
    print(f"[ERR_0]: {str(e)}")
    EmailSender().send_email_to_all(msg_code=config.MSG_CODE_ERR,err_msg=str(e))