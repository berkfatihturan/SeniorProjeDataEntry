from src.WebScraper import WebScraper
from src.EmailSender import EmailSender

url = "https://www.arabam.com/ikinci-el?take=50"
CarScraper = WebScraper(url=url)
try:
    CarScraper.start_scrapping()
except Exception as e:
    print(f"[ERR_0]: {str(e)}")
    EmailSender().send_email_to_all(msg_code=0,err_msg=str(e))
