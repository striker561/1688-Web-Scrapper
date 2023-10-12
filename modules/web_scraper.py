from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def setup_driver():
    #SET DRIVER PARAMETER; I USED FIREFOX
    driverOptions = webdriver.FirefoxOptions()
    driverOptions.set_preference('permissions.default.image', 2)
    driverOptions.set_preference('permissions.default.stylesheet', 2)
    #START THE WEB DRIVER
    driver = webdriver.Firefox(options=driverOptions)
    return driver

def scroll_down(driver, num_scrolls, sleep_time):
    #SCROLL DOWN THE PAGE WITH JAVASCRIPT WITH INTERVAL AND A WAIT TIME
    scroll_script = "window.scrollBy(0, 500);"
    for _ in range(num_scrolls):
        driver.execute_script(scroll_script)
        time.sleep(sleep_time)

def scrape_data(driver, wait=20):
    #LOAD URL AND WAIT FOR THE PAGE TO LOAD IN OTHER TO BE SCRAPPED
    url = 'https://www.1688.com/'
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'offer_titles')))
    except TimeoutException:
        print("Element may not be found even after waiting,  await confirmation from processing function. Please check your connection or the page structure.")

    scroll_down(driver=driver, num_scrolls=5, sleep_time=0.5)

def process_data(driver):
    # FIND ELEMENTS PROCESSES IT AND RETURN THE APPROPRIATE DATA 
    offerURLs = driver.find_elements(By.CLASS_NAME, "link")
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

    return dataPayload
