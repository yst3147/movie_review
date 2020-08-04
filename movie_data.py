import requests
from bs4 import BeautifulSoup
import csv


URL = "https://movie.naver.com/movie/running/current.nhn"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

movie = soup.select('.lst_detail_t1 > li')

movie_data = {}
for m in movie:
    code = m.select_one('.lst_dsc > .tit > a')['href']
    title = m.select_one('.lst_dsc > .tit > a').text
    codeurl, code_num = code.split("=")
    movie_data['title'] = title
    movie_data['code'] = code_num
    print(movie_data)
