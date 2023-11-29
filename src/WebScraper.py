import time
import json

from src.EmailSender import EmailSender
from src.DatabaseHandler import DatabaseHandler
from src.DataHandler import DataHandler
from src.DatabaseHandler import StateSaver

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException
import config

# driver
service = Service(config.CHROME_DRIVER_PATH)


class WebScraper:

    def __init__(self, url):
        self.url = url
        self.counter = 0
        self.MsgSender = EmailSender()
        self.DBHandler = DatabaseHandler()
        self.StateSaver = StateSaver()

        # set chrome driver settings
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")

        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # open browser and go to page
        self.driver.get(self.url)
        try:
            # close permission page
            self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
        except NoSuchElementException or ElementClickInterceptedException:
            print("Cant Find Permission Page")

    # nht
    def start_scrapping(self):
        # get current_town_code???
        current_town_code = self.StateSaver.get_last_position()
        current_page_num = self.StateSaver.get_last_page_num()

        for town_code in range(current_town_code, config.MAX_TOWN_CODE):
            print(F"Town Code...[{town_code}]")
            for page_num in range(current_page_num, config.MAX_PAGE_NUM):
                print(F"Page Num...[{page_num}]")
                # The page with the advertisements opens.
                self._open_ad_list_page(town_code=town_code, page_num=page_num)

                # save town_code to state.json file
                self.StateSaver.save_last_position(town_code=town_code, page_num=page_num, counter=self.counter)

                # Opens the advertisement pages one by one. If there is no ad on the page, it closes an inner loop.
                try:
                    # If this element is present, there is no advertisement on the page.
                    self.driver.find_element(By.CLASS_NAME, 'no-result-content')
                    print("NO RESULT")
                except NoSuchElementException:
                    print("FINDING RESULT")
                    # find all adv in page and open in order and write data to file
                    self._scrapping_ad_on_page()
                else:
                    # If no error is received, there is no advertisement on this page. Move on to another TOWN.
                    break
                # If the page is finished, send an e-mail to the users
                self.MsgSender.send_email_to_all(msg_code=config.MSG_CODE_PAGE_DONE, town_id=town_code,
                                                 page_num=page_num)
            # If the settlement is finished, send an e-mail to the users
            current_page_num = 1
            self.MsgSender.send_email_to_all(msg_code=config.MSG_CODE_TOWN_DONE, town_id=town_code)
        # If process is done, send an e-mail to the users
        self.MsgSender.send_email_to_all(msg_code=config.MSG_CODE_PROCESS_DONE)

    def _scrapping_ad_on_page(self):
        print("on_scrapping_ad_on_page")
        # find all adv in page and open in order and write data to file
        try:
            self.driver.find_element(By.CSS_SELECTOR,'.listing-table')
        except:
            print("Something happen")
            self.driver.refresh()
            self._scrapping_ad_on_page()
        else:
            ad_list = self.driver.find_elements(By.CSS_SELECTOR, '.listing-list-item')
            print(len(ad_list))
            for advertItem in ad_list:
                print("dwasdawd")
                self._get_data_from_advertisement_page(advertItem)
                self.counter = self.counter + 1

    # Opens the ad page.
    def _get_data_from_advertisement_page(self, advert_item):
        # get ad
        ad_link = advert_item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        # Since a new page needs to be opened, the home page is kept here.
        original_windows = self.driver.current_window_handle
        # A new page opens, and you enter the advertisement page.
        self.driver.switch_to.new_window('tab')
        # open ad page
        self._open_ad_page(ad_link)

        # getting and formatting data in here
        data = DataHandler(driver=self.driver).collect_data()
        self.DBHandler.add_data(data=data)
        print("------------------")

        # The ad page is closed and return to the main page.
        self.driver.close()
        self.driver.switch_to.window(original_windows)
        return 0

    def _open_ad_list_page(self, town_code, page_num):
        try:
            self.driver.get(f"{self.url}&town={town_code}&page={page_num}")
        except WebDriverException or ElementClickInterceptedException:
            print("waiting internet connection...")
            self._open_ad_list_page(town_code, page_num)
            time.sleep(10)
        else:
            print("Connection Ok...[Main Page Loaded]")
        finally:
            return

    def _open_ad_page(self, ad_link):
        while True:
            try:
                self.driver.get(ad_link)
            except WebDriverException:
                print("waiting internet connection...")
                time.sleep(10)
            else:
                print("Connection Ok...[Ad Page Loaded]")
                break
