from bs4 import BeautifulSoup
import requests
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import dados

headers = {"Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8",
                        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
url = r'https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22mapBounds%22%3A%7B%22west%22%3A-122.67605818701172%2C%22east%22%3A-122.19059981298828%2C%22south%22%3A37.55325083788472%2C%22north%22%3A37.99666720211685%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D'

url_form = dados.url_form

class GetterData():
    def __init__(self, headers, url) -> None:
        self.html = requests.get(url = url, headers = headers).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.data = json.loads(
                self.soup.select_one("script[data-zrr-shared-data-key]")
                .contents[0]
                .strip('!<>-'))
    
    def Address(self):
        return [address['address'] for address 
                in self.data["cat1"]['searchResults']['listResults']]

    def Links(self):
        self.links = []
        for result in self.data['cat1']['searchResults']['listResults']:
            self.links.append('https://www.zillow.com/' + result['detailUrl'])
        return self.links
    
    def Prices(self):
        re_num = re.compile(r'\d')
        self.prices = []
        for result in self.data['cat1']['searchResults']['listResults']:
            try:
                self.prices.append(result['units'][0]['price'].strip("+"))
            except KeyError:
                value = re_num.findall(str(result['unformattedPrice']))
                value.insert(1,',')
                self.prices.append('$'+''.join(value))
        return self.prices
    
    def Dados(self):
        return {'Address':self.Address(), 'Links':self.Links(), 'Prices':self.Prices()}

class Scrapper():
    def __init__(self,dados, url) -> None:
        self.url = url
        self.driver = webdriver.Firefox()
        self.dados = dados
        
        self.driver.get(url)

    
    def restart_page(self):
        self.driver.get(self.url)

    def put_data(self):
        for i in range(len(self.dados['Address'])):
            time.sleep(2)
            local1 = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            local1.send_keys(self.dados['Address'][i])
            
            local2 = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            local2.send_keys(self.dados['Prices'][i])
            
            local3 = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            local3.send_keys(self.dados['Links'][i])
            
            enter = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
            enter.click()
            
            self.restart_page()
        self.driver.quit()

if __name__ == '__main__':
    scraper_zillow = GetterData(url=url, headers=headers)
    dados_zillow = scraper_zillow.Dados()

    scrapper = Scrapper(dados_zillow, url_form)
    scrapper.put_data()
