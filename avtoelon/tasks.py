import requests

import json
from bs4 import BeautifulSoup
from avtoelon.parser import parse_avtoelon_detail
from django.conf import settings
from avtoelon.models import Auto


def parse_start():
    avtos = []
    for i in range(5, 15):
        res = requests.get(
            f"https://avtoelon.uz/avto/chevrolet/?page={i}")
        soup = BeautifulSoup(res.text, "html.parser")

        for ad in soup.find_all("div", {"class": "row list-item a-elem"}):
            res = requests.get(
                f"{settings.AVTOELON_DETAIL_URL}{ad['data-id']}")
            if res.status_code != 200:
                print("Something went wrong")
                print(res)
                print(res.status_code)
                continue
            # CHECK URL PAGINATION
            parse_object = parse_avtoelon_detail(res.text)
            parse_object["autoelon_id"] = ad['data-id']
            avtos.append(parse_object)
            Auto.create_or_update_auto(parse_object)
    print(avtos)
