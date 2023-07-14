import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, parse_qs
import pandas as pd

PARSER_URL = "https://avtoelon.uz/a/show/3512303"


res = requests.get(PARSER_URL)
if res.status_code != 200:
    print("Something went wrong")
    print(res)
    print(res.status_code)
# CHECK URL PAGINATION

soup = BeautifulSoup(res.text, "html.parser")
item = soup.find("div", {"class": "item product"})

title = soup.find("h1", {"class": "a-title__text"})
brand = title.find("span", {"itemprop": "brand"}).text
name = title.find("span", {"itemprop": "name"}).text
position = title.text.split(",")[1].strip()
print(brand)
print(name)
print(position)
