from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import config
import os
import glob
import shutil


def download_documents(driver: webdriver.Chrome, page: int, pagesize: int):
    try:
        driver.get(f"https://www.fwc.gov.au/document-search?q=*&options=SearchType_3%2CSortOrder_agreement-date-desc&facets=AgreementIndustry_Building+metal+and+civil+construction+industries&page={page}&pageSize={pagesize}")
        time.sleep(5)

        # Get the total number of pages
        total_pages = int(driver.find_elements(By.CLASS_NAME,"fwc-pager-pagination-item")[-2].text)

        results = driver.find_elements(By.CLASS_NAME, "fwc-results-item")

        for result in results:
            title = result.find_element(By.TAG_NAME, "h3").text
            result.find_element(By.LINK_TEXT, "Download").click()
            time.sleep(3)
            wait_for_download()
            save_downloaded_document(title)            

    except Exception as e:
        print(e)
        return 0
    finally:
        time.sleep(5)
        return total_pages
    

def wait_for_download():
    download_directory = config.download_directory
    timeout = config.download_timeout

    while timeout > 0:
        if any(filename.endswith(".crdownload") for filename in os.listdir(download_directory)):
            time.sleep(1)
            timeout -= 1
        else:
            break
    pass

def save_downloaded_document(name: str):
    download_directory = config.download_directory
    save_directory = config.save_directory + '/fwc'

    # Create the save directory if it does not exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Move the downloaded file (not directory) to the save directory
    files = glob.glob(download_directory + '/*')
    for f in files:
        if os.path.isfile(f):
            file = f
            ext = file.split('.')[-1]
            shutil.move(file, save_directory + '/' + name + '.' + ext)

    pass