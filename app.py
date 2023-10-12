from modules import web_scraper
from modules import save

if __name__ == "__main__":
    #LOAD SCRAPER MODULES AND PROCESS DATA
    driver = web_scraper.setup_driver()
    web_scraper.scrape_data(driver, 5)
    data = web_scraper.process_data(driver)
    driver.quit()
    #SAVE DATA TO JSON FILE
    save.save_to_json(data)
