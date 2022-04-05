import undetected_chromedriver.v2 as uc
import time
driver = uc.Chrome(use_subprocess=True)
driver.get('https://www.chegg.com/')  # known url using cloudflare's "under attack mode"
time.sleep(20)