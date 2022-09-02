from selenium import webdriver
from selenium_stealth import stealth
import time
from selenium.webdriver.common.by import By

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
for metal in metals:
    url = metal.find_element(By.TAG_NAME, "a").get_attribute("href")
    driver.get(url)
time.sleep(5)
driver.quit()
