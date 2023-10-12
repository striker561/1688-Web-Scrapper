from modules.web_scraper import WebScraper
from modules.save import save_to_json as save

url = 'https://www.1688.com/'

if __name__ == "__main__":
    #INIT CLASS
    scraper = WebScraper()

    #INIT DRIVER
    scraper.prepare_driver(url, 5)

    #SAVE DATA 

    #------------Save Initial Product on Home Page--------
    save(scraper.process_index_data(), 'init_product.json')

    #------------Save Categorical Data on Home Page---------
    linkData = scraper.href_link_scraper()
    save(linkData, 'hrefData.json')

    #------------Scrap and save link data ----------
    for linkIndex, link in enumerate(linkData):
        link_data = scraper.scrape_data(link['pageURL'], 5, 40)
        save(link_data, 'link-index-' + str(linkIndex) + '.json')
