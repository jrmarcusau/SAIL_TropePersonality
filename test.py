### SCRIPT TO TEST REMOTE SSH INSTALLATION ###


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

print("here me")
firefox_options = Options()
print("here2")
firefox_options.add_argument("--headless")
print("here2.5")
driver = webdriver.Firefox(options=firefox_options)
print("here3")

url = "https://www.personality-database.com/profile?pid=2&cid=3"
driver.get(url)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.info-name')))

soup = BeautifulSoup(driver.page_source, 'html.parser')
print("souping")

info_card = soup.find('a', class_='profile-card-link')

character = info_card.find('h2', class_='info-name').text

print("character: " + character)

# b'<!DOCTYPE html><html xmlns="http://www....
driver.quit()

print("hello world")
