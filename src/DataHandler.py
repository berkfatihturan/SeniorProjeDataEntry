from selenium.webdriver.common.by import By


class DataHandler:

    def __init__(self, driver):
        self.driver = driver

    # It takes the data from the page and organizes it.
    def collect_data(self):
        json_data = {}
        try:
            json_data = self._get_overview_data(json_data)
            json_data = self._get_price_data(json_data)
            json_data = self._get_description_data(json_data)
            json_data = self._get_damage_data(json_data)
        except:
            print("HATA....[-1]")
        return json_data

    def _get_price_data(self, json_data):
        json_data["Fiyat"] = self.driver.find_element(By.CLASS_NAME, 'product-price').text[:-3]
        return json_data

    def _get_description_data(self,json_data):
        json_data["Description"] = self.driver.find_element(By.ID, 'tab-description').text
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
                    if property_item_title == "Orjinal":
                        json_data[part_name] = 0
                    elif property_item_title == "Lokal boyalı":
                        json_data[part_name] = 1
                    elif property_item_title == "Boyalı":
                        json_data[part_name] = 2
                    elif property_item_title == "Değişmiş":
                        json_data[part_name] = 3
                    elif property_item_title == "Belirtilmemiş":
                        json_data[part_name] = 4
        # get damage info /* end */
        return json_data
