import json
from pathlib import Path
import os, sys
from base64 import b64decode
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from datetime import datetime

from selenium import webdriver
parentdir = Path(__file__).parent.absolute()
exec_path = os.path.join(parentdir, 'chromedriver.exe')
data_path = os.path.join(parentdir.parent, 'data')
data_path2 = "c:\\Users\\nick4\\Personal_projects\\CheggDcBot\\data"
selenium_cookie_file = "c:\\Users\\nick4\\Personal_projects\\CheggDcBot\\cookies.pkl"


options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(executable_path="c:\\Users\\nick4\\Personal_projects\\CheggDcBot\\src\\chromedriver.exe", options=options)
driver.get("https://stackoverflow.com/questions/41721734/take-screenshot-of-full-page-with-selenium-python-with-chromedriver")
el = driver.find_element_by_tag_name('body')
el.screenshot("c:\\Users\\nick4\\Personal_projects\\CheggDcBot\\data\\a.png")
driver.quit()