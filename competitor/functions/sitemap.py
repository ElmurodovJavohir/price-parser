from competitor.models import Competitor, CompetitorSetting


def get_site_robots_sitemap_urls(url):
    from urllib.request import Request, urlopen

    # import pandas as pd
    from bs4 import BeautifulSoup

    response = urlopen(Request(url, headers={"User-Agent": "Mozilla"}))
    soup = BeautifulSoup(
        response, "html.parser", from_encoding=response.info().get_param("charset")
    )

    data = []
    lines = str(soup).splitlines()

    for line in lines:
        if line.startswith("Sitemap:"):
            split = line.split(":", maxsplit=1)
            data.append(split[1].strip())
    return data


def get_sitemap_urls(url, setting: CompetitorSetting):
    import urllib.request
    from urllib.parse import urlparse

    from bs4 import BeautifulSoup
    from django.db.models import Q

    from competitor.models import CATEGORY_URL, PRODUCT_URL, CompetitorUrls

    response = urllib.request.urlopen(url)
    xml = BeautifulSoup(response, "lxml", from_encoding=response.info().get_param("charset"))
    urls = xml.find_all("url")

    category_urls = set()
    product_urls = set()
    for url in urls:
        if xml.find("loc"):
            loc = url.findNext("loc").text
            link = urlparse(loc)
            if any(category in link.path for category in setting.category_slug):
                category_urls.add(loc)
            if any(product in link.path for product in setting.product_slug):
                product_urls.add(loc)
    category_urls = list(category_urls)
    product_urls = list(product_urls)

    created_urls = CompetitorUrls.objects.filter(
        Q(url__in=product_urls) | Q(url__in=category_urls)
    ).values_list("url", flat=True)
    # CREATED CATeEGORY URLS
    create_category_urls = [c_url for c_url in category_urls if c_url not in created_urls]
    category_Competitor_urls = []
    for category_url in list(set(create_category_urls)):
        category_Competitor_urls.append(
            CompetitorUrls(competitor=setting.competitor, type=CATEGORY_URL, url=category_url)
        )
    # CREATED CATEGORY URLS
    create_product_urls = [p_url for p_url in product_urls if p_url not in created_urls]
    product_Competitor_urls = []
    for product_url in list(set(create_product_urls)):
        product_Competitor_urls.append(
            CompetitorUrls(competitor=setting.competitor, type=PRODUCT_URL, url=product_url)
        )
    CompetitorUrls.objects.bulk_create(product_Competitor_urls)
    CompetitorUrls.objects.bulk_create(category_Competitor_urls)
