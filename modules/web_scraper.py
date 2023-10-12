from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class WebScraper:
    def __init__(self):
        self.driver = self.setup_driver()

    def setup_driver(self):
        driverOptions = webdriver.FirefoxOptions()
        driverOptions.set_preference('permissions.default.image', 2)
        driverOptions.set_preference('permissions.default.stylesheet', 2)
        driver = webdriver.Firefox(options=driverOptions)
        return driver

    def scroll_down(self, num_scrolls, sleep_time):
        scroll_script = "window.scrollBy(0, 500);"
        for _ in range(num_scrolls):
            self.driver.execute_script(scroll_script)
            time.sleep(sleep_time)

    def prepare_driver(self, url, wait=20, num_scroll=5, sleep_time=0.5):
        self.driver.get(url)
        try:
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'offer_title')))
        except TimeoutException:
            print("Element may not be found even after waiting, await confirmation from processing function. Please check your connection or the page structure.")
        
        self.scroll_down(num_scroll, sleep_time)

    def process_index_data(self):
        offerURLs = self.driver.find_elements(By.CLASS_NAME, "link")
        # offerTitles = self.driver.find_elements(By.CSS_SELECTOR, 'div header div')
        offerTitles = self.driver.find_elements(By.CLASS_NAME, 'offer-title')
        offerImages = self.driver.find_elements(By.CLASS_NAME, 'offer-image')
        offerPriceLefts = self.driver.find_elements(By.CLASS_NAME, 'priceLeft')

        dataPayload = []

        for url, title, image, price_left in zip(offerURLs, offerTitles, offerImages, offerPriceLefts):
            dataItem = {
                'url': url.get_attribute('href'),
                'title': title.text,
                'image': image.get_attribute('src'),
                'price': price_left.text,
            }
            dataPayload.append(dataItem)

        return dataPayload
    
    def process_children_data(self):
        offerURLs = self.driver.find_elements(By.CLASS_NAME, "offer")
        offerTitles = self.driver.find_elements(By.CLASS_NAME, 'offer-title')
        offerImages = self.driver.find_elements(By.XPATH, "//div[@class='offer-img']//img")
        offerPriceLefts = self.driver.find_elements(By.CLASS_NAME, 'alife-bc-uc-number')

        dataPayload = []

        for url, title, image, price_left in zip(offerURLs, offerTitles, offerImages, offerPriceLefts):
            dataItem = {
                'url': url.get_attribute('href'),
                'title': title.text,
                'image': image.get_attribute('src'),
                'price': price_left.text,
            }
            dataPayload.append(dataItem)

        return dataPayload

    def href_link_scraper(self):
        tagLinks = self.driver.find_elements(By.CLASS_NAME, 'c-name')

        pageLinks = []

        for tagData in tagLinks:
            tagItem = {
                'pageName': tagData.text,
                'pageURL': tagData.get_attribute('href')
            }
            pageLinks.append(tagItem)

        return pageLinks

    def scrape_data(self, url, wait=20, num_scroll=5, sleep_time=0.5):
        try:
            self.prepare_driver(url, wait, num_scroll, sleep_time)
            return self.process_children_data()
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def close(self):
        self.driver.quit()