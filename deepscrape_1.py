### SCRIPT TO SCRAPE 16MBTI GIVEN PERSONALITY MOVIE PAGE SOURCE ###
# Project: personality
# Input: page source
# Output: data - 16MBTI

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
    cols = ['esfp', 'esfj', 'estp', 'estj', 'enfp', 'enfj', 'entp', 'entj', 'isfp', 'isfj', 'istp', 'istj', 'infp', 'infj', 'intp', 'intj']
    tdata = dict.fromkeys(cols, 0)
    
    personality = soup.find_all('div', 'rc-collapse personality-vote')
    for per in personality:
        type = per.find('label', 'personality-vote-title').text
        if (type == 'Four Letter'):
            try: 
                votes = per.find_all('div', 'personality-vote-item')

                for vote in votes:
                    v = vote.find('label').text
                    mbti, count = re.match(r"([a-zA-Z]+)\((\d+)\)", v).groups()
                    mbti = mbti.lower()  # convert to lower case
                    count = int(count)  # convert to integer
                    tdata[mbti] = count

            except AttributeError:
                print("no personality")
            break

    return tdata

def scrape_page(driver, url):
    pdata = {}
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    try: 
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.profile-name')))
        pdata = {'source': driver.page_source}
        print("Good Page")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        pdata = process_page(soup)
    except TimeoutException:
        print("Bad Page")
        time.sleep(20)
    
    return pdata



def main(start, end):
    
    old_data = pd.read_csv("deepscrape_v2_all.csv")
    print("Loaded Data")

    mdata = []
    
    for index, row in old_data.iloc[start:end].iterrows():
        print("row: " + str(index) + ", " + str(row['character']) + ", " + str(row['movie']))
        
        all_info = row.to_dict()
        cols = ['esfp', 'esfj', 'estp', 'estj', 'enfp', 'enfj', 'entp', 'entj', 'isfp', 'isfj', 'istp', 'istj', 'infp', 'infj', 'intp', 'intj']
        new_info_backup = dict.fromkeys(cols, 0)
        try: 
            source = row['source']
            soup = BeautifulSoup(source, 'html.parser')

            new_info = process_page(soup)
            print(new_info)
            
            all_info.update(new_info)
            
        except Exception as e:
            print(f"Skipping row {index} due to error: {e}")
            all_info["notes"] = str(e)
            all_info.update(new_info_backup)

        all_info.pop('source', None)    
        mdata.append(all_info)

    new_data = pd.DataFrame(mdata)
    filename = "mbti_added_" + str(end) + ".csv"
    new_data.to_csv(filename, index=False)        
    
    return mdata
    


main(0, 2000)
main(2000, 4000)
main(4000, 6000)
main(6000, 8000)
main(8000, 8400)
