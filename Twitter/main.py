from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import dados
from time import sleep

class InternetSpeedTwitterBot:
    def __init__(self) -> None:
        self.driver = webdriver.Firefox()
        self.down = dados.down
        self.up = dados.up
    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        sleep(3)
        value = self.driver.find_element(By.CLASS_NAME, 'start-text')
        value.click()
        sleep(90)
        down_lido = self.driver.find_element(By.CSS_SELECTOR,'.download-speed').get_attribute('innerHTML')
        up_lido = self.driver.find_element(By.CSS_SELECTOR,'.upload-speed').get_attribute('innerHTML')
        return float(down_lido), float(up_lido)

    def tweet_at_provider(self, down_lido, up_lido):
        self.driver.get("https://twitter.com/i/flow/login")
        sleep(3)
        nick_name = self.driver.find_element(By.CSS_SELECTOR,'input.r-t60dpp')
        nick_name.send_keys(dados.email)
        enter = self.driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')
        enter.click()
        sleep(3)
        pass_word = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        pass_word.send_keys(dados.senha)
        
        enter_account = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div')
        enter_account.click()

if __name__ == '__main__':
    driver = InternetSpeedTwitterBot()
    down_lido, up_lido = driver.get_internet_speed()
    driver.tweet_at_provider(down_lido, up_lido)