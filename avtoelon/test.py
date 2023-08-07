import requests

import json
from bs4 import BeautifulSoup
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

