from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time
import re

class Scrapper():
    def __init__(self, url) -> None:
        self.driver = webdriver.Firefox()
        self.driver.get(url)
        time.sleep(2)
        self.html = self.driver.page_source
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def Collector_titles(self):
        self.titles = [title.getText() for title in self.soup.select('ul li h3 a')]

    def Collector_prices(self):
        price_re = re.compile(r'\$\d+\.\d{2}')
        self.prices = price_re.findall(self.html)
    
    def Collector_links(self):
        self.links = ['https://www.audible.com'+link['href'] for link in self.soup.select('ul li h3 a')]
    
    def Collector_summary(self):
        results = self.soup.find_all('span', {'class':'bc-text bc-size-base bc-color-secondary'})
        self.summary = [result.getText() for result in results]
    
    def ScrapperMaster(self):
        self.Collector_titles()
        self.Collector_prices()
        self.Collector_links()
        self.Collector_summary()

        self.data = [{'Titles':x[0],
                 'Prices':x[1],
                 'Links':x[2],
                 'Summary':x[3]} for x in zip(self.titles, self.prices, self.links, self.summary)]

        with open('Books.csv',mode='a',newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.data[0].keys())
            writer.writeheader()
            writer.writerows(self.data)
        self.driver.quit()

headers = {"Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8",
                        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
url = r'https://www.audible.com/search?keywords=book&node=18573211011'

if __name__ == '__main__':
    driver = Scrapper(url)
    driver.ScrapperMaster()