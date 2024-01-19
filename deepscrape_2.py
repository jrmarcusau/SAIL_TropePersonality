### [selenium] SCRIPT TO SCRAPE ALL INDIVIDUAL TROPE HREF GIVEN INDEX LIST PAGE ###
# Project: trope
# Input: index page list
# Output: href list

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



def scrape_index(driver, url):
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    twikilink_tags = soup.find_all('a', class_='twikilink')
    base_trope = "https://tvtropes.org"
    pdata = [{'text': tag.text.strip(), 'href': (base_trope + tag.get('href'))} for tag in twikilink_tags]
    return pdata



def main_1(start, end):
    data = []
    driver = webdriver.Firefox(options=firefox_options)
    url_base = "https://tvtropes.org/pmwiki/index_report.php?filter=&groupname=Main&page="

    for i in range(start, end):
        print("Page: " + str(i))
        data += scrape_index(driver, url_base + str(i))
    
    df = pd.DataFrame(data)
    print(df)
    df.to_csv("tropes_href.csv")



main_1(1, 113)


#1-112 inclusive

#total 1-5584

#0-600
#600-