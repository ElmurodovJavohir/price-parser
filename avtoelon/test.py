import requests

import json
from parser import parse_avtoelon_detail
from bs4 import BeautifulSoup


def test_parse_avtoelon_detail(real_data: dict, testing_data: dict) -> bool:
    for key, value in real_data.items():
        if key not in testing_data:
            print(f"KEY ERROR {key} {value}")
            return False
        if value != testing_data[key]:
            print(value, testing_data[key])
            print(f"VALUE ERROR {key} |{value}|{testing_data[key]}|")
            return False
    return True


AVTOELON_DETAIL_URL = "https://avtoelon.uz/a/show/"

json_file = open("./test.json", encoding="utf8")
adverts = json.load(json_file)
json_file.close()

avtos = []
for i in range(1, 2):
    res = requests.get(f"https://avtoelon.uz/avto/chevrolet/cobalt/?page={i}")
    soup = BeautifulSoup(res.text, "html.parser")

    for ad in soup.find_all("div", {"class": "row list-item a-elem"}):
        res = requests.get(f"{AVTOELON_DETAIL_URL}{ad['data-id']}")
        if res.status_code != 200:
            print("Something went wrong")
            print(res)
            print(res.status_code)
            continue
        # CHECK URL PAGINATION
        parse_object = parse_avtoelon_detail(res.text)
        parse_object["url"] = ""
        avtos.append(parse_object)


import pandas as pd

df = pd.DataFrame.from_dict(parse_object)


df.to_excel("cobalt.xlsx")
