from bs4 import BeautifulSoup

from competitor.models import Competitor, CompetitorProduct


def parse_category(scrap: Competitor, soup: BeautifulSoup):
    # # Remove unwanted tags
    # unwanteds = soup.find_all(scrap.unwanted_tag, attrs=scrap.unwanted_dict)
    # for unwanted in unwanteds:
    #     unwanted.extract()
    exec(scrap.setting.category_parse)
    # results = soup.find("div", attrs={"class": "all-products-catalog__content"})

    # if isinstance(results, type(None)):
    #     print("Error: results is NoneType")
    #     raise Exception

    # products = results.find_all("div", attrs={"class": "product-card"})
    # if len(products) == 0:
    #     raise Exception
    # # Stopping the parsing when no images are found

    # for product in products:
    #     # Writing the Image Name, Download Count and Stars Count to File
    #     # print(product)
    #     import re

    #     CompetitorProduct.objects.update_or_create(
    #         competitor=scrap,
    #         url=product.find("a", attrs={"class": "product-card__link"})["href"],
    #         defaults={
    #             "name": product.find(
    #                 "div", attrs={"class": "product-card__brand-name"}
    #             ).text.strip(),
    #             "price": re.sub(
    #                 r"\D", "", product.find("div", attrs={"class": "price__main"}).text.strip()
    #             ),
    #             "price_for_month": product.find(
    #                 "div", attrs={"class": "price__credit"}
    #             ).text.strip(),
    #         },
    #     )
