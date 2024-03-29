### [Repeat 4] ###

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

def process_page(soup):
    mbti_vote = ''
    mbti_count = ''
    big5_vote = ''
    big5_count = ''
    
    personality = soup.find_all('div', 'rc-collapse personality-vote')
    for per in personality:
        try: 
            type = per.find('label', 'personality-vote-title').text
            count = per.find('label', 'personality-vote-count').text
            vote = per.find('div', 'personality-vote-item').label.text

            if (type == 'Four Letter'):
                mbti_vote = vote
                mbti_count = count
            elif (type == 'Big 5 (SLOAN)'):
                big5_vote = vote
                big5_count = count
        except AttributeError:
            print("no personality")


    tdata = {'mbti_vote' : mbti_vote,
            'mbti_count' : mbti_count,
            'big5_vote' : big5_vote,
            'big5_count' : big5_count}

    return tdata

def scrape_page(driver, url):
    pdata = {}
    time.sleep(5)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    try: 
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.profile-name')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        pdata = process_page(soup)
    except TimeoutException:
        print("Bad Page")
    
    return pdata

def main():
    
    mdata = []
    driver = webdriver.Firefox(options=firefox_options)
    old_data = pd.read_csv("matched_data_v2.csv")

    for index, row in old_data.iterrows():
        print("row: " + str(index) + ", " + str(row['character']) + ", " + str(row['movie']))
        
        url = row['href']
        driver.get(url)

        new_info = scrape_page(driver, url)
        print(new_info)

        all_info = row.to_dict()
        all_info.update(new_info)

        mdata.append(all_info)

        if (index % 100 == 0):
            df = pd.DataFrame(mdata)
            filename = "fixed_data_set" + str(index) + ".csv"
            df.to_csv(filename, index=False)
    

main()
