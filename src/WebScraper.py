import time
import json
import pandas as pd
from src.EmailSender import EmailSender

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# driver
chrome_driver_path = "/usr/lib/chromium-browser/chromedriver"
service = Service(chrome_driver_path)

MAX_TOWN_CODE = 970
MAX_PAGE_NUM = 51

MSG_CODE_PAGE_DONE = 0
MSG_CODE_TOWN_DONE = 1
MSG_CODE_PROCESS_DONE = 2


def json_to_excel(json_data, excel_file):
    try:
        # Excel dosyasını oku (varsa) veya yeni bir dosya oluştur
        try:
            df = pd.read_excel(excel_file)
        except FileNotFoundError:
            df = pd.DataFrame()

        # JSON verisini bir DataFrame'e çevir
        new_data = json.loads(json_data)
        new_df = pd.json_normalize(new_data)

        # DataFrame'i genişleterek birleştir
        df = pd.concat([df, new_df], axis=0, ignore_index=True)

        # DataFrame'i Excel dosyasına yaz
        df.to_excel(excel_file, index=False)

        print("Veri başarıyla Excel dosyasına eklendi.")

    except Exception as e:
        print(f"Hata oluştu: {str(e)}")


class WebScraper:

    def __init__(self, url):
        # open browser and go to page
        self.url = url
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get(self.url)
        
        self.MsgSender = EmailSender()

        try:
            # close permission page
            self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
        except NoSuchElementException:
            print("Cant Find Permission Page")

    #
    def startScrapping(self):
        for town_code in range(1, MAX_TOWN_CODE):
            for page_num in range(1, MAX_PAGE_NUM):
                # The page with the advertisements opens.
                self.driver.get(f"{self.url}&town={town_code}&page={page_num}")

                # She opens the advertisement pages one by one. If there is no ad on the page, it closes an inner loop.
                try:
                    # If this element is present, there is no advertisement on the page.
                    self.driver.find_element(By.CLASS_NAME, 'no-result-content')
                except NoSuchElementException:
                    # find all adv in page and open in order and write data to file
                    for advertItem in self.driver.find_elements(By.CSS_SELECTOR, '[id^="listing"]'):
                        self._openAdvertisementPage(advertItem)
                else:
                    # If no error is received, there is no advertisement on this page. Move on to another TOWN.
                    break
                # If the page is finished, send an e-mail to the users
                self.MsgSender.send_email_to_all(msg_code=MSG_CODE_PAGE_DONE)
            # If the settlement is finished, send an e-mail to the users
            self.MsgSender.send_email_to_all(msg_code=MSG_CODE_TOWN_DONE)
        # If process is done, send an e-mail to the users
        self.MsgSender.send_email_to_all(msg_code=MSG_CODE_PROCESS_DONE)


    # Opens the ad page.
    def _openAdvertisementPage(self, advertItem):
        # get ad
        ad_link = advertItem.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        # Since a new page needs to be opened, the home page is kept here.
        original_windows = self.driver.current_window_handle
        # A new page opens and you enter the advertisement page.
        self.driver.switch_to.new_window('tab')
        self.driver.get(ad_link)

        # getting and formatting data in here
        data = self._getData()
        print(data)
        json_to_excel(json.dumps(data), 'data/veri.xlsx')
        print("------------------")
        time.sleep(1)

        # The ad page is closed and return to the main page.
        self.driver.close()
        self.driver.switch_to.window(original_windows)
        return 0


    # It takes the data from the page and organizes it.
    def _getData(self):
        jsonData = {}
        # get overview info /* start */
        for propertyItem_overview in self.driver.find_elements(By.CSS_SELECTOR, '[class*="property-item"]'):
            propertyItem_Title = propertyItem_overview.find_element(By.CLASS_NAME, 'property-key').text
            propertyItem_Value = propertyItem_overview.find_element(By.CLASS_NAME, 'property-value').text
            jsonData[propertyItem_Title] = propertyItem_Value
        # get overview info /* end */

        # get damage info /* start */
        # Check the items in the damage list on the page
        for propertyItem_damageInfo in self.driver.find_elements(By.CSS_SELECTOR, '[class*="car-damage-info"]'):

            propertyItem_Title = propertyItem_damageInfo.find_element(By.CSS_SELECTOR, 'p').text

            # sort car parts by damage category
            for carParts in propertyItem_damageInfo.find_elements(By.CSS_SELECTOR, 'ul li'):
                partName = carParts.text
                # If category is null - sends it back to avoid being added to the list
                if partName != '-':
                    jsonData[partName] = propertyItem_Title
        # get damage info /* end */

        return jsonData
