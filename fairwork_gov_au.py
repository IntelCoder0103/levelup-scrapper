from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import config

from helpers import already_downloaded, save_downloaded_document, wait_for_download, wait_for_save_pdf

def download_documents(driver: webdriver.Chrome, page: int = 1, pagesize: int = 10, override: bool = False):
    try:
        driver.get(f"https://www.fairwork.gov.au/employment-conditions/awards/list-of-awards")
        time.sleep(5)

        # Get the total number of pages
        total_pages = 1

        results = driver.find_elements(By.CSS_SELECTOR, ".node__content p a")

        for result in results:
            try:
                title = result.text
                link = result.get_attribute('href')

                print(title)
                if title.find('[MA') < 0:
                    continue
                
                if not override and already_downloaded(title, 'fairwork'):
                    continue

                # Open a new tab using JavaScript
                driver.execute_script("window.open('about:blank', '_blank');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(link)

                time.sleep(3)

                driver.execute_script("window.print();")
                time.sleep(3)

                wait_for_save_pdf()
                save_downloaded_document(title, 'fairwork')

            except Exception as e:
                print(e)
                continue
            finally:
                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[1])
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
            # break
            

    except Exception as e:
        print(e)
        return 0
    finally:
        time.sleep(5)
        return total_pages
    
