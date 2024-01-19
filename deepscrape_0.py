### [selenium] SCRIPT TO SCRAPE INDIVUDAL PERSONALITY PAGE SOURCE GIVEN HREF LIST ###
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
    driver.get(url)
    try: 
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.profile-name')))
        pdata = {'source': driver.page_source}
        print("Good Page")
        #soup = BeautifulSoup(driver.page_source, 'html.parser')
        #pdata = process_page(soup)
    except TimeoutException:
        print("Bad Page")
        time.sleep(20)
    
    return pdata


def main(start, end):
    
    old_data = pd.read_csv("matched_data_v2.csv")


    mdata = []
    driver = webdriver.Firefox(options=firefox_options)
    

    for index, row in old_data.iloc[start:end].iterrows():
        print("row: " + str(index) + ", " + str(row['character']) + ", " + str(row['movie']))
        
        url = row['href']
        driver.get(url)

        new_info = scrape_page(driver, url)

        all_info = row.to_dict()
        all_info.update(new_info)

        mdata.append(all_info)

        if ((index+1) % 200 == 0):
            df = pd.DataFrame(mdata)
            filename = "deepscrape_v2_" + str(index+1) + ".csv"
            df.to_csv(filename, index=False)
    

#main(2700, 3000)
#main(4000, 5000)
#main(6000, 7000)
#main(8000, 8500)

main(3600, 4000)
main(8400, 8680)