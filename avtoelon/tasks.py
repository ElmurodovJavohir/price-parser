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
    links = AutoLink.objects.filter(is_parsed=False).order_by("?")[:100]
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
        Auto.create_or_update_auto(parse_object, link)
        link.is_parsed = True
        link.save()


@shared_task()
def parse_links_with_selenium():
    # BS4 IMPORTS
    import time
    from selenium.common.exceptions import WebDriverException
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    for i in range(1, 1001):
        options = Options()
        options.add_argument("--headless")

        options.add_argument("--no-sandbox")

        options.add_argument("--disable-dev-shm-usage")

        chrome_prefs = {}

        options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}

        # MAKE DICT COMPETITOR SETTINGS

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get(f"https://avtoelon.uz/avto/chevrolet/?page={i}")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        links = set()
        for ad in soup.find_all("div", {"class": "row list-item a-elem"}):
            links.add(f"{settings.AVTOELON_DETAIL_URL}{ad['data-id']}")
        # BULK CREATE or UPDATE AUTOLINK OBJECTS
        used_links = set(AutoLink.objects.filter(link__in=links).values_list("link", flat=True))
        new_links = links - used_links
        AutoLink.objects.bulk_create([AutoLink(link=link) for link in new_links])
        # Delay to load the contents of the HTML FIle
        time.sleep(2)
        # Parse processed webpage with BeautifulSoup

        print(f"Page {i} done")
