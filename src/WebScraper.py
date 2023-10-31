import time
import json

from src.EmailSender import EmailSender
from src.DatabaseHandler import DatabaseHandler

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import config

# driver
chrome_driver_path = "/usr/lib/chromium-browser/chromedriver"
service = Service(chrome_driver_path)


class WebScraper:

    def __init__(self, url):
        self.url = url
        self.MsgSender = EmailSender()
        self.DBHandler = DatabaseHandler()

        # set chrome driver settings
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("start-maximized");
        chrome_options.add_argument("disable-infobars");
        chrome_options.add_argument("--disable-extensions"); 
        chrome_options.add_argument("--disable-gpu"); 
        chrome_options.add_argument("--disable-dev-shm-usage"); 
        chrome_options.add_argument("--no-sandbox");
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # open browser and go to page
        self.driver.get(self.url)
        try:
            # close permission page
            self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
        except NoSuchElementException:
            print("Cant Find Permission Page")

    #
    def start_scrapping(self):
        for town_code in range(1, config.MAX_TOWN_CODE):
            for page_num in range(1, config.MAX_PAGE_NUM):
                # The page with the advertisements opens.
                self._open_ad_list_page(town_code=town_code, page_num=page_num)

                # She opens the advertisement pages one by one. If there is no ad on the page, it closes an inner loop.
                try:
                    # If this element is present, there is no advertisement on the page.
                    self.driver.find_element(By.CLASS_NAME, 'no-result-content')
                except NoSuchElementException:
                    # find all adv in page and open in order and write data to file
                    for advertItem in self.driver.find_elements(By.CSS_SELECTOR, '[id^="listing"]'):
                        self._get_data_from_advertisement_page(advertItem)
                else:
                    # If no error is received, there is no advertisement on this page. Move on to another TOWN.
                    break
                # If the page is finished, send an e-mail to the users
                self.MsgSender.send_email_to_all(msg_code=config.MSG_CODE_PAGE_DONE, town_id=town_code,
                                                 page_num=page_num)
            # If the settlement is finished, send an e-mail to the users
            self.MsgSender.send_email_to_all(msg_code=config.MSG_CODE_TOWN_DONE, town_id=town_code)
        # If process is done, send an e-mail to the users
        self.MsgSender.send_email_to_all(msg_code=config.MSG_CODE_PROCESS_DONE)

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
        data = self._collect_data
        print(data)
        self.DBHandler.add_data(data=data)
        print("------------------")

        # The ad page is closed and return to the main page.
        self.driver.close()
        self.driver.switch_to.window(original_windows)
        return 0

    def _open_ad_list_page(self, town_code, page_num):
        try:
            self.driver.get(f"{self.url}&town={town_code}&page={page_num}")
        except WebDriverException:
            print("waiting internet connection...")
            self._open_ad_list_page(town_code, page_num)
            time.sleep(10)
        else:
            print("Connection Ok...[Main Page Loaded]")

    def _open_ad_page(self, ad_link):
        try:
            self.driver.get(ad_link)
        except WebDriverException:
            print("waiting internet connection...")
            time.sleep(10)
            self._open_ad_page(ad_link)
        else:
            print("Connection Ok...[Ad Page Loaded]")

    # It takes the data from the page and organizes it.
    @property
    def _collect_data(self):
        json_data = {}
        json_data = self._get_overview_data(json_data)
        json_data = self._get_price_data(json_data)
        json_data = self._get_damage_data(json_data)
        return json_data

    def _get_price_data(self, json_data):
        json_data["Fiyat"] = self.driver.find_element(By.CLASS_NAME, 'product-price-container').text[:-3]
        return json_data

    def _get_overview_data(self, json_data):
        # get overview info /* start */
        for propertyItem_overview in self.driver.find_elements(By.CSS_SELECTOR, '[class*="property-item"]'):
            property_item_title = propertyItem_overview.find_element(By.CLASS_NAME, 'property-key').text
            property_item_value = propertyItem_overview.find_element(By.CLASS_NAME, 'property-value').text
            json_data[property_item_title] = property_item_value
        # get overview info /* end */
        return json_data

    def _get_damage_data(self, json_data):
        # get damage info /* start */
        # Check the items in the damage list on the page
        for propertyItem_damageInfo in self.driver.find_elements(By.CSS_SELECTOR, '[class*="car-damage-info"]'):

            property_item_title = propertyItem_damageInfo.find_element(By.CSS_SELECTOR, 'p').text

            # sort car parts by damage category
            for carParts in propertyItem_damageInfo.find_elements(By.CSS_SELECTOR, 'ul li'):
                part_name = carParts.text
                # If category is null - sends it back to avoid being added to the list
                if part_name != '-':
                    json_data[part_name] = property_item_title
        # get damage info /* end */
        return json_data
