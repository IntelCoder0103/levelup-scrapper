from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import config
import os
import glob
import json
import fwc_gov_au
from scrape_pdf_links import scrape_all_pdfs_in_page
from scrape_links_tree_view import scrape_links_in_tree_view

from fairwork_gov_au import download_documents

def clear_download_directory():
    files = glob.glob(config.download_directory + '/*')
    files = [f for f in files if os.path.isfile(f)]
    for f in files:
          os.remove(f)

try:
    if not os.path.exists(config.download_directory):
        os.makedirs(config.download_directory)
    # Configure Chrome WebDriver options
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": config.download_directory,
        "savefile.default_directory": config.download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "printing.print_preview_sticky_settings.appState": json.dumps({
            "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local",
                "account": ""
            }],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        })
    })
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--kiosk-printing')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    clear_download_directory()
    
    #scrape_all_pdfs_in_page(driver, "https://www.fwc.gov.au/hearings-decisions/decisions-and-orders/significant-decisions-and-summaries")

    # pagesize = 10
    # page = 1
    # total_pages = page
    # max_pages = 5

    # while page <= total_pages and page <= max_pages:
    #   total_pages = fwc_gov_au.download_documents(driver, page, pagesize)
    #   page += 1
    #   time.sleep(1)

    links = scrape_all_pdfs_in_page(driver, 'https://www.fairwork.gov.au/tools-and-resources/best-practice-guides', True, 
                                    'a[data-entity-substitution=canonical]',
                                    lambda x: x.find('https://www.fairwork.gov.au/tools-and-resources/best-practice-guides/') >= 0)
    print(links)
    
except Exception as e:
    print(e)

finally:
    time.sleep(10)
    driver.quit()