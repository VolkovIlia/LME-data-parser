from selenium import webdriver
from selenium_stealth import stealth
import time
from datetime import datetime
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

# options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path="chromedriver")

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Linux",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

url = f"https://www.lme.com/en/"
driver.get(url)
block = driver.find_element(By.CLASS_NAME, "meganav-parent-item__children")
names = block.find_element(By.TAG_NAME, "ul")
metals = names.find_elements(By.TAG_NAME, "li")
urls = []
names = []
bids = []
offers = []
for metal in metals:
    urls.append(metal.find_element(By.TAG_NAME, "a").get_attribute("href"))
time.sleep(1)
for i in urls:
    try:
        driver.get(i)
        time.sleep(1)
        names.append(driver.find_element(By.CLASS_NAME, "data-set-table__title").text)
        bids.append(driver.find_element(By.CLASS_NAME, "data-set-table__body").find_element(By.XPATH, "//*[@id=\"dataset-tab-0\"]/div/div[2]/div[2]/div[1]/div/div[1]/table/tbody/tr[1]/td[1]").text)
        offers.append(driver.find_element(By.CLASS_NAME, "data-set-table__body").find_element(By.XPATH, "//*[@id=\"dataset-tab-0\"]/div/div[2]/div[2]/div[1]/div/div[1]/table/tbody/tr[1]/td[2]").text)
    except:
        pass
driver.quit()
d = dict({"names" : names, "bids" : bids, "offers" : offers})
df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in d.items() ]))
file_name = str(datetime.now().date())+".csv"
df.to_csv(file_name, index=False)
