from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def setup_driver():
    driverOptions = webdriver.FirefoxOptions()
    driverOptions.set_preference('permissions.default.image', 2)
    driver = webdriver.Firefox(options=driverOptions)
    return driver

def scroll_down(driver, num_scrolls, sleep_time):
    scroll_script = "window.scrollBy(0, 500);"
    for _ in range(num_scrolls):
        driver.execute_script(scroll_script)
        time.sleep(sleep_time)

def scrape_data(driver):
    url = 'https://www.1688.com/'
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'offer_titles')))
    except TimeoutException:
        print("Element not found even after waiting. Please check your connection or the page structure.")
        driver.quit()
        exit()

    scroll_down(driver=driver, num_scrolls=4, sleep_time=0.5)

    # Find elements
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
