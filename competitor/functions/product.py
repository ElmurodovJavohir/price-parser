from math import prod

from competitor.models import Competitor


def parse_products(site: Competitor):
    # Base Libraries
    import csv
    import time

    # BeautifulSoup Library used for Parsing the HTML
    from bs4 import BeautifulSoup

    # Selenium 4 for loading the Browser Driver
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    # Web Driver Manager
    from webdriver_manager.chrome import ChromeDriverManager

    from competitor.models import PRODUCT_URL, Competitor, CompetitorUrls
    from competitor.parser.product import parse_product

    # Initialising the Chrome Driver
    options = Options()
    options.add_argument("--headless")

    options.add_argument("--no-sandbox")

    options.add_argument("--disable-dev-shm-usage")

    chrome_prefs = {}

    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    products = CompetitorUrls.objects.filter(competitor=site, type=PRODUCT_URL)
    for product in products:
        # if str(scrap.category_slug) in str(url):
        # Load the Docker Hub HTML page
        driver.get(product.url)
        # Delay to load the contents of the HTML FIle
        time.sleep(2)
        # Parse processed webpage with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        try:
            parse_product(site, soup, product.url)
        except Exception as e:
            print(product.url)
            print(e)

    # Closing of the Chrome Driver
    driver.quit()
