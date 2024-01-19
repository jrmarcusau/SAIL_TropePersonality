### SCRIPT TO SCRAPE MENTIONED TROPES GIVEN INDIVIDUAL TROPE PAGE SOURCE ###
# Project: trope
# Input: page source
# Output: data - tagged tropes


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
    h2_tag = soup.find('h2', string='Examples:')
    if h2_tag is not None:
        for sibling in h2_tag.find_next_siblings():
            sibling.extract()

    div_tag = soup.find('div', {'class': 'section-links'})
    if div_tag is not None:
        div_tag.extract()


    cols = ['mentions']
    tdata = dict.fromkeys(cols, 0)
    mentions = []
    base_trope = "https://tvtropes.org"
    twikilink_tags = soup.find_all('a', class_='twikilink')
    for tag in twikilink_tags:
        
        mention = {}
        href = base_trope + tag.get('href')
        trope = href.split("/")[-1]
        trope = re.sub(r"(?<!^)(?=[A-Z])", " ", trope)

        if "Main" in href:
            mention['trope'] = trope
            mention['href'] = href

        if mention:
            mentions.append(mention)

    tdata['mentions'] = mentions

    return tdata


def main(start, end):
    
    old_data = pd.read_csv("tropes_deepscrape_all.csv")
    print("Loaded Data")

    mdata = []
    
    for index, row in old_data.iloc[start:end].iterrows():
        print("row: " + str(index) + ", " + row['text'])
        
        all_info = row.to_dict()
        cols = ['mentions']
        new_info_backup = dict.fromkeys(cols, 0)
        try: 
            source = row['source']
            soup = BeautifulSoup(source, 'html.parser')

            new_info = process_page(soup)
            
            all_info.update(new_info)
            
        except Exception as e:
            print(f"Skipping row {index} due to error: {e}")
            all_info.update(new_info_backup)

        all_info.pop('source', None)    
        
        mdata.append(all_info)

        


    new_data = pd.DataFrame(mdata)
    filename = "mentions_added_" + str(end) + ".csv"
    new_data.to_csv(filename, index=False)        
    
    return mdata
    


main(0, 1000)
main(1000, 2000)

