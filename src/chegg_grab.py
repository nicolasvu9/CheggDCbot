from selenium import webdriver
from pathlib import Path
import os, sys
import json
import time
import pickle
import validators 
from urllib.parse import urlparse
from datetime import datetime

parentdir = Path(__file__).parent.absolute()
exec_path = os.path.join(parentdir, 'chromedriver.exe')
data_path = os.path.join(parentdir.parent, 'data')
selenium_cookie_file = os.path.join(parentdir.parent, 'cookies.pkl')


class Slitherer:
    def __init__(self):
        options = webdriver.ChromeOptions()

        appState = {
            "recentDestinations": [
                {
                    "id": "Save as PDF",
                    "origin": "local",
                    "account": ""
                }
            ],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        }
    
        profile = {'printing.print_preview_sticky_settings.appState': json.dumps(appState),
           'savefile.default_directory': data_path}
        options.add_experimental_option('prefs', profile)
        options.add_argument('--kiosk-printing')
        
        options.add_argument('--disable-extensions')
        options.add_argument('--profile-directory=Default')
        options.add_argument("--disable-plugins-discovery")
        options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('window-position=3000,0') 
        
        self.driver = webdriver.Chrome(executable_path=os.path.join(parentdir, 'chromedriver.exe'), options=options)


    def load_cookies(self):
        if os.path.exists(selenium_cookie_file) and os.path.isfile(selenium_cookie_file):
            print("Loading cookies from " + selenium_cookie_file)
            cookies = pickle.load(open(selenium_cookie_file, "rb"))

            # Enables network tracking so we may use Network.setCookie method
            self.driver.execute_cdp_cmd('Network.enable', {})

            # Iterate through pickle dict and add all the cookies
            for cookie in cookies:
                # Fix issue Chrome exports 'expiry' key but expects 'expire' on import
                if 'expiry' in cookie:
                    cookie['expires'] = cookie['expiry']
                    del cookie['expiry']

                # Replace domain 'apple.com' with 'microsoft.com' cookies
                cookie['domain'] = cookie['domain'].replace('apple.com', 'microsoft.com')

                # Set the actual cookie
                self.driver.execute_cdp_cmd('Network.setCookie', cookie)

            # Disable network tracking
            self.driver.execute_cdp_cmd('Network.disable', {})
            return 1

        print("Cookie file " + selenium_cookie_file + " does not exist.")
        return 0

    def remove_header(self):
        try:
            self.driver.execute_script("""
                var l = document.getElementsByClassName("chgg-hdr force-desktop kit-kat-search  type-home subtype-  loggedIn")[0];
                l.parentNode.removeChild(l);
                """)
        except:
            return 1

def validate_url(link):
    valid=validators.url(link)
    if not valid:
        return False
    domain = urlparse(link).netloc
    if domain != "www.chegg.com":
        return False
    return True

def pdf_name():
    now = datetime.now()
    date_time = now.strftime("%m%d%Y%H%M%S%f")
    return date_time + '.pdf'

def save_cookies():
    bot = Slitherer()
    bot.driver.get("https://chegg.com")

    bot.driver.implicitly_wait(10)
    time.sleep(60)
    print("------------------------------------------------------------------------- \nsaving cookies")
    pickle.dump( bot.driver.get_cookies() , open("cookies.pkl","wb"))

def get_answer(link):
    try:
        name = pdf_name()
        bot = Slitherer()
        bot.load_cookies()
        bot.driver.get(link)
        print('--------------------------------------------------------------------------\nOpening Link')
        time.sleep(4)
        bot.remove_header()
        bot.driver.execute_script('document.title="{}";'.format(name))
        bot.driver.execute_script('window.print();')
        bot.driver.close()
        print('--------------------------------------------------------------------------\nGetting PDF')
        return name

    except:
        return 1



