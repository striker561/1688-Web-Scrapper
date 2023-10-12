from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json

#DEFINE BROWSER CONFIGURATIONS
driverOptions = webdriver.FirefoxOptions()
driverOptions.set_preference('permissions.default.image', 2)
driver = webdriver.Firefox(options=driverOptions)


url = 'https://www.1688.com/'

driver.get(url)
    
try:
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'offer_titles')))
except TimeoutException:
    print("Element not found even after waiting. Please check your connection or the page structure.")
    # driver.quit()
    # exit()


scroll_script = "window.scrollBy(0, 500);"
driver.execute_script(scroll_script)
time.sleep(1.5)

scroll_script = "window.scrollBy(0, 500);"
driver.execute_script(scroll_script)
time.sleep(1.5)

scroll_script = "window.scrollBy(0, 500);"
driver.execute_script(scroll_script)
time.sleep(1.5)

#FIND ELEMENTS
offerURLs = driver.find_elements(By.CLASS_NAME, "link")
# offerURLs = driver.find_elements(By.XPATH, "//a[@data-spm-anchor-id and @target='_blank']")
# offerTitles = driver.find_elements(By.CLASS_NAME, 'offer_titles')
offerTitles = driver.find_elements(By.CSS_SELECTOR, 'div header div')
offerImages = driver.find_elements(By.CLASS_NAME, 'offer-image')
offerPriceLefts = driver.find_elements(By.CLASS_NAME, 'priceLeft')


dataPayload = []

for url, title, image, price_left in zip(offerURLs, offerTitles, offerImages, offerPriceLefts):
    dataItem = {
        'url': url.get_attribute('href'),
        'title': title.text,
        'image': image.get_attribute('src'),
        'price': price_left.text,
    }
    dataPayload.append(dataItem)

#CLOSE DRIVER
driver.quit()

with open('data.json', 'w', encoding='utf-8') as json_file:
    json.dump(dataPayload, json_file, ensure_ascii=False, indent=2)
    
print("Data scraped and saved to 'data.json'.")