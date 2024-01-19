### SCRIPT TO SCRAPE MOVIES GIVEN INDIVIDUAL TROPE PAGE SOURCE ###
# Project: Tropes
# Input: page source
# Output: list of movies

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


def get_next_sibling(soup):
    
    def contains_target_string(tag):
        return tag.name == 'div' and tag.get('class') == ['folderlabel'] and 'Film' in tag.get_text() and ('Live-Action' in tag.get_text() or 'Animation' in tag.get_text())

    target_nodes = soup.find_all(contains_target_string)
    sibling_nodes = []

    if target_nodes:
        for target_node in target_nodes:
            sibling_node = target_node.find_next_sibling()
            if sibling_node:
                sibling_nodes.append(sibling_node)
        return sibling_nodes
    return None

def get_li_data(film_nodes):
    
    data = []
    base_trope = "https://tvtropes.org"
    for film_node in film_nodes:
        li_nodes = film_node.find_all('li')
        for l in li_nodes:
            example = {}
            a = l.find('a', class_='twikilink')
            if a:
                href = base_trope + a['href']
                movie = href.split("/")[-1]
                movie = re.sub(r"(?<!^)(?=[A-Z])", " ", movie)
                example['movie'] = movie
                example['href'] = href
                example['text'] = l.text.strip()
                data.append(example)
    return data

def is_overflow(soup):
    title = soup.find('h1', itemprop='headline', class_='entry-title')
    if title is not None:
        trope = title.get_text(strip=True).replace(' ', '')
    href_values = re.compile(rf"/pmwiki/pmwiki.php/{trope}/(.*Animat.*|.*Film.*)", re.IGNORECASE)
    return bool(soup.find('a', href=href_values))

def process_page(soup):
    cols = ['examples']
    tdata = dict.fromkeys(cols, [])

    if is_overflow(soup):
        tdata['examples'] = [{'movie': "OVERFLOW", 'href': "https://tvtropes.org", "text": ""}]

    film_nodes = get_next_sibling(soup) #LIST for live action and animation
    if film_nodes:
        examples = get_li_data(film_nodes) #handles list
        tdata['examples'] = examples
    return tdata


def main(start, end):
    
    old_data = pd.read_csv("tropes_deepscrape_all.csv")
    print("Loaded Data")

    mdata = []
    
    for index, row in old_data.iloc[start:end].iterrows():
        print("row: " + str(index) + ", " + row['text'])
        
        all_info = row.to_dict()
        cols = ['examples']
        new_info_backup = dict.fromkeys(cols, 0)
        try: 
            source = row['source']
            soup = BeautifulSoup(source, 'html.parser')
            new_info = process_page(soup)
        
            if (new_info['examples'] == []):
                print("  Example: None")
            else:
                print("  Example: " + new_info['examples'][0]['movie'] + ", ... , " + str(len(new_info['examples'])))
            
            all_info.update(new_info)

        except Exception as e:
            print(f"Skipping row {index} due to error: {e}")
            all_info.update(new_info_backup)

        all_info.pop('source', None)    
        
        mdata.append(all_info)

        


    new_data = pd.DataFrame(mdata)
    filename = "tropes_examples_" + str(end) + ".csv"
    new_data.to_csv(filename, index=False)        
    
    return mdata
    

main(0, 1000)
main(1000, 2000)
main(2000, 3000)
