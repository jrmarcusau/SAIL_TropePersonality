### SCRIPT TO TEST PACKAGE INSTALLATION ###


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

#print("here")
#chrome_options = Options()
#print("here2")
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
#chrome_options.add_argument("--headless")
#driver = webdriver.Chrome(options=chrome_options)
###print("here3")
#start_url = "https://duckgo.com"
#driver.get(start_url)
#print(driver.page_source.encode("utf-8"))
# b'<!DOCTYPE html><html xmlns="http://www....
#driver.quit()



print("here")
firefox_options = Options()
print("here2")
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options)
print("here3")

url = "https://www.personality-database.com/profile?pid=2&cid=3"

driver.get(url)
wait = WebDriverWait(driver, 10)

source = driver.page_source
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.info-name')))

soup = BeautifulSoup(driver.page_source, 'html.parser')

info_card = soup.find('a', class_='profile-card-link')
character = info_card.find('h2', class_='info-name').text
movie_div = soup.find('div', {'class': 'profile-category arrow'})
movie = movie_div.find('h1').text

personality = soup.find_all('div', 'rc-collapse personality-vote')


print("character: " + character)
print("movie: " + movie)
print("personality: " + personality)

# b'<!DOCTYPE html><html xmlns="http://www....
driver.quit()

print("hello world")
