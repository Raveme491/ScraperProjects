import requests
from bs4 import BeautifulSoup

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
url = f'https://www.billboard.com/charts/hot-100/{date}/'

html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')

results = soup.select(selector="li h3")

songs = [result.getText().strip() for result in results][:100]

with open("Musics.txt", mode='a') as file:
    for song in songs:
        file.write(song)
        file.write("\n")