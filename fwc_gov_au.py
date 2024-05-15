from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

from helpers import appendJsonArray, save_downloaded_document, wait_for_download



def download_documents(driver: webdriver.Chrome, page: int, pagesize: int):
    try:
        driver.get(f"https://www.fwc.gov.au/document-search?q=*&options=SearchType_3%2CSortOrder_agreement-date-desc&facets=AgreementIndustry_Building+metal+and+civil+construction+industries&page={page}&pageSize={pagesize}")
        time.sleep(5)

        # Get the total number of pages
        total_pages = int(driver.find_elements(By.CLASS_NAME,"fwc-pager-pagination-item")[-2].text)

        results = driver.find_elements(By.CLASS_NAME, "fwc-results-item")

        info = []

        for result in results:
            title = result.find_element(By.TAG_NAME, "h3").text
            tags = [chip.text for chip in result.find_elements(By.CLASS_NAME, "fwc-chip")]
            info.append({"title": title, "tags": tags})

            # result.find_element(By.LINK_TEXT, "Download").click()
            # time.sleep(3)
            # wait_for_download()
            # save_downloaded_document(title, 'fwc')            

    except Exception as e:
        print(e)
        return 0
    finally:
        appendJsonArray(info, "fwc.json")
        time.sleep(5)
        return total_pages
    
