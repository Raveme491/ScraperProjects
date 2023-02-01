import requests
from bs4 import BeautifulSoup

url = r'https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/'

html = requests.get(url).text

soup = BeautifulSoup(html, 'html.parser')

results = soup.find_all(name="h3", class_="title")

movies = [title.getText() for title in results]
movies.reverse()

with open("movies.txt",mode='a') as file:
    for movie in movies:
        file.write(f"{movie} \n")