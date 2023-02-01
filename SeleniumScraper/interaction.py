from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')

with webdriver.Firefox(options=options) as driver:
    driver.get("https://en.wikipedia.org/wiki/Main_Page")
    result = driver.find_element(By.ID, "articlecount").find_element(By.TAG_NAME,"a").get_attribute("text")
    print(result)