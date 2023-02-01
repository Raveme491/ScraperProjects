from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')

with webdriver.Firefox(options=options) as driver:
    driver.get("https://www.python.org/")

    htmls = driver.find_elements(By.TAG_NAME, 'time')
    datas = [html.get_attribute("datetime")[:10] for html in htmls[5:]]

    refs = driver.find_elements(By.CLASS_NAME, "shrubbery")[1].find_elements(By.CSS_SELECTOR, "li a")
    events = [ref.get_attribute("text") for ref in refs]

py_events = {data:event for data,event in zip(datas,events)}
print(py_events)
