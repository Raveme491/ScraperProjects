from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from time import sleep, time
import re


with webdriver.Firefox() as driver:
    driver.get(r"https://orteil.dashnet.org/cookieclicker/")
    sleep(2)
    speak = driver.find_element(By.ID, "langSelect-EN")
    speak.click()
    sleep(2)
    num_cook = 0
    inicio = time()
    pattern = re.compile(r'(\d{1,3}\.?\d{1,3}(?=(\scookie)|(?=\")))')
    cookie_price = re.compile(r'((\d{1,3}.)*\d{1,3})(?=(\<)|(\smillion)|(\sbillion))')
    clicks_list = []
    for i in range(0,19):
        clicks_list.append(driver.find_element(By.ID, f"product{i}"))
    while True:
        fim = time()
        cook = driver.find_element(By.ID, "bigCookie")
        cook.click()

        if (fim-inicio) >= 5:
            result = driver.find_element(By.ID, "cookies").get_attribute("outerHTML")
            num_cook = int(next(pattern.finditer(result)).group())
            inicio = fim
            ruido = []
            for i in range(19):
                opcoes = driver.find_element(By.ID, f"productPrice{i}")
                ruido.append(opcoes.get_attribute("outerHTML"))

            values = []
            for idx, i in enumerate(cookie_price.finditer(''.join(ruido))):
                if idx>=5 and idx<=7:
                    values.append(float(i.group().replace(".",""))*10**6)
                elif idx>=8 and idx<=10:
                    values.append(float(i.group().replace(".",""))*10**9)
                else:
                    try:
                        values.append(float(i.group().replace(",","")))
                    except:
                        values.append(float(i.group()))
            print(values)
            for idx in range(len(values)-1,-1,-1):
                print(values[idx])
                if num_cook>=values[idx]:
                    try:
                        clicks_list[idx].click()
                        num_cook-=values[idx]
                    except:
                        clicks_list[0].click()
                        num_cook-=values[0]

