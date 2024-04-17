from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import config
import os
import glob

from fwc_gov_au import download_documents

def clear_download_directory():
    files = glob.glob(config.download_directory + '/*')
    files = [f for f in files if os.path.isfile(f)]
    for f in files:
          os.remove(f)

try:
        
    # Configure Chrome WebDriver options
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": config.download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    clear_download_directory()
    
    pagesize = 10
    page = 1
    total_pages = page
    max_pages = 2

    while page <= total_pages and page <= max_pages:
      total_pages = download_documents(driver, page, pagesize)
      page += 1
      time.sleep(1)
    
except Exception as e:
    print(e)

finally:
    time.sleep(10)
    driver.quit()