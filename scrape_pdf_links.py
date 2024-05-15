from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
import time
import requests
import config

def scrape_pdf_links_recursive(driver: webdriver.Chrome, url: str, selector: str, matchFn: callable):
    try:
        pdf_links = scrape_pdf_links(driver, url)

        results = driver.find_elements(By.CSS_SELECTOR, selector)


        sub_links = []

        for result in results:
            try:
                link = result.get_attribute('href')
                if link:
                    # Convert relative URLs to absolute URLs
                    link = urljoin(url, link)
                    if matchFn(link):
                        sub_links.append(link)

            except Exception as e:
                print(e)
                continue
        
        for sub_link in sub_links:            
            # scrape child link
            print('Scraping:', sub_link)
            pdf_links += scrape_pdf_links_recursive(driver, sub_link, selector, matchFn)

    except Exception as e:
        print(e)
        return 0
    finally:
        return pdf_links

def scrape_pdf_links(driver: webdriver.Chrome, url: str):
    try:
        driver.get(url)
        time.sleep(5)

        results = driver.find_elements(By.TAG_NAME, "a")

        links = []

        for result in results:
            try:
                link = result.get_attribute('href')
                if link:
                    # Convert relative URLs to absolute URLs
                    link = urljoin(url, link)
                    if link.find('.pdf') >= 0:
                        print('Found PDF:', link, result.text)
                        links.append((link, result.text))
            except Exception as e:
                print(e)
                continue

    except Exception as e:
        print(e)
        return 0
    finally:
        return links

def download_pdf_links(links: list):
    # We don't need chrome browser anymore
    # Let's use requests to download the pdf files
    for link in links:
        try:
            print('Downloading:', link[1])
            response = requests.get(link[0])
            with open(config.save_directory + '/' + link[1] + '.pdf', 'wb') as f:
                f.write(response.content)
                print('Downloaded:', link[1])
        except Exception as e:
            print(e)
            continue

def scrape_all_pdfs_in_page(driver: webdriver.Chrome, url: str, recursive = False, selector = 'a', matchFn = lambda x: True):
    if recursive:
        links = scrape_pdf_links_recursive(driver, url, selector, matchFn)
    else:
        links = scrape_pdf_links(driver, url)
    download_pdf_links(links)