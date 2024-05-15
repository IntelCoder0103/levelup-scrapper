from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
import time
import requests
import config

def scrape_links_in_tree_view(driver: webdriver.Chrome, url: str, rootSelector: str, activeSelector: str):
    try:
        driver.get(url)
        time.sleep(2)

        root = driver.find_element(By.CSS_SELECTOR, rootSelector)
        active = root.find_element(By.CSS_SELECTOR, activeSelector)
        
        # get sub menu of active menu, next element of active
        sub_menu = active.parent.find_element(By.TAG_NAME, "ul")
        # get all links in sub menu
        if sub_menu is None:
            return []
        results = sub_menu.find_elements(By.TAG_NAME, "a")

        links = []

        for result in results:
            try:
                link = result.get_attribute('href')
                if link:
                    # Convert relative URLs to absolute URLs
                    link = urljoin(url, link)
                    links.append(link)

                    # scrape child link
                    child_links = scrape_links_in_tree_view(driver, link, rootSelector, activeSelector)
                    links.extend(child_links)

            except Exception as e:
                print(e)
                continue

    except Exception as e:
        print(e)
        return 0
    finally:
        return links