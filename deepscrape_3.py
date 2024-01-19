### [selenium] SCRIPT TO SCRAPE INDIVIDUAL TROPE PAGE SOURCE GIVEN HREF LIST ###
# Project: personality
# Input: href list
# Output: page source


from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

from bs4 import BeautifulSoup
import codecs
import re
import requests
import pandas as pd
firefox_options = Options()
firefox_options.add_argument("--headless")


def scrape_page(driver, url):
    pdata = {}
    wait = WebDriverWait(driver, 10)
    try:
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='headline'].entry-title")))
        pdata = {'source': driver.page_source}
        print("Good Page")
    except TimeoutException:
        print("Bad page")
        time.sleep(5)
    except Exception as e:
        print(f"An error occurred while scraping the page: {e}")
    
    return pdata



def main_2(start, end):
    old_data = pd.read_csv("tropes_href.csv")
    
    mdata = []
    driver = webdriver.Firefox(options=firefox_options)

    for index, row in old_data.iloc[start:end].iterrows():
        print("row: " + str(index) + ", " + str(row['text']))
        url = row['href']
        new_info = scrape_page(driver, url)

        all_info = row.to_dict()
        all_info.update(new_info)

        mdata.append(all_info)

        if ((index+1) % 200 == 0):
            df = pd.DataFrame(mdata)
            filename = "tropes_deepscrape_" + str(index+1) + ".csv"
            df.to_csv(filename, index=False)


#main_1(1, 113)
main_2(3000, 4000)
main_2(4000, 5000)
main_2(5000, 5585)
#1-112 inclusive

#total 1-5584