import requests

import json
from bs4 import BeautifulSoup
from avtoelon.parser import parse_avtoelon_detail
from django.conf import settings
from avtoelon.models import Auto, AutoLink
from celery import shared_task


@shared_task
def parse_links():
    for i in range(1, 1001):
        res = requests.get(f"https://avtoelon.uz/avto/chevrolet/?page={i}")
        soup = BeautifulSoup(res.text, "html.parser")
        links = set()
        for ad in soup.find_all("div", {"class": "row list-item a-elem"}):
            links.add(f"{settings.AVTOELON_DETAIL_URL}{ad['data-id']}")
        # BULK CREATE or UPDATE AUTOLINK OBJECTS
        used_links = set(AutoLink.objects.filter(link__in=links).values_list("link", flat=True))
        new_links = links - used_links
        AutoLink.objects.bulk_create([AutoLink(link=link) for link in new_links])
        print(f"Page {i} done")


@shared_task
def parse_start():
    links = (
        AutoLink.objects.filter(is_parsed=False).order_by("?")[:100]
    )
    for link in links:
        res = requests.get(link.link)
        if res.status_code != 200:
            print("Something went wrong")
            print(res)
            print(res.status_code)
            continue
        # CHECK URL PAGINATION
        parse_object = parse_avtoelon_detail(res.text)
        parse_object["autoelon_id"] = link.link.replace(settings.AVTOELON_DETAIL_URL, "")
        Auto.create_or_update_auto(parse_object)
        link.is_parsed = True
        link.save()
