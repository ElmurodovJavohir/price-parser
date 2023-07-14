import re

from bs4 import BeautifulSoup

from competitor.models import Competitor
from product.models import Product


def parse_product(scrap: Competitor, soup: BeautifulSoup, url):

    exec(scrap.setting.category_parse)

    # Product.objects.update_or_create(
    #     parse=scrap,
    #     url=url,
    #     defaults={
    #         "name": title,
    #         "image": image,
    #         "price": price,
    #         "price_for_month": price_month,
    #     },
    # )
