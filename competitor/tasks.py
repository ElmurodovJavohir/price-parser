from math import prod

from celery import shared_task

# @shared_task()
# def parse_site_sitemaps_urls():
#     from competitor.functions.sitemap import get_site_robots_sitemap_urls
#     from competitor.models import Competitor, CompetitorSetting

#     parse_sites = CompetitorSetting.objects.filter(competitor__is_active=True)
#     for site in parse_sites:
#         site.sitemaps_urls = get_site_robots_sitemap_urls(f"{site.competitor.url}/robots.txt")
#         site.save()


@shared_task()
def parse_site_products():
    from competitor.functions.category import parse_category_products
    from competitor.functions.product import parse_products
    from competitor.models import Competitor

    parse_sites = Competitor.objects.filter(is_active=True)
    for site in parse_sites:
        # parse_products(site)
        parse_category_products(site)


@shared_task()
def google_search_competitor():
    # BS4 IMPORTS

    from urllib.parse import urlparse

    import requests

    from competitor.models import Competitor, CompetitorSetting
    from product.models import Product

    # MAKE DICT COMPETITOR SETTINGS
    settings = CompetitorSetting.objects.all().select_related("competitor")
    competitor_settings = {}
    for s in settings:
        competitor_settings[s.competitor.url] = s
    # GET COMPETITOR LINKS and ADD TO NAME
    competitor_urls = CompetitorSetting.objects.all(
    ).values_list("competitor__url", flat=True)
    products = Product.objects.all().order_by("-updated_at")
    for product in products:
        print(product)
        # product.competitor_products.clear()
        # SEARCH AND GET URLS OF COMPETITORS
        competitor_urls_text = " OR ".join(
            [f"site:{url_}" for url_ in competitor_urls])
        query = f"{product.name} {competitor_urls_text}"
        links = {}
        print("GOOGLE SEARCH START -----------")
        print(
            f"https://www.googleapis.com/customsearch/v1?key=AIzaSyCD3GPGZ6UF-Q6T2qZdNajaBpMxNp2EecM&cx=240f292dc318c4d6b&q={query}"
        )
        res = requests.get(
            f"https://www.googleapis.com/customsearch/v1?key=AIzaSyCD3GPGZ6UF-Q6T2qZdNajaBpMxNp2EecM&cx=240f292dc318c4d6b&q={query}"
        ).json()
        print("GOOGLE SEARCH FINISH -----------")
        if "items" in res:
            for item in res["items"]:
                # PARSE URL AND CHECK
                parsed_url = urlparse(item["link"])
                site_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                if site_url not in links and site_url in competitor_urls:
                    path_ = (
                        parsed_url.path.replace("/ru/", "/")
                        .replace("/uz/", "/")
                        .replace("/en/", "/")
                    )
                    links[site_url] = f"{site_url}{path_}"
            print(links)
            product.competitor_json = links
            product.save()


@shared_task()
def parse_start():
    # BS4 IMPORTS
    import time
    from selenium.common.exceptions import WebDriverException
    from competitor.models import Competitor, CompetitorSetting
    from competitor.parser.product import parse_product
    from product.models import Product
    settings = CompetitorSetting.objects.all().select_related("competitor")
    competitor_settings = {}
    for s in settings:
        competitor_settings[s.competitor.url] = s
    # GET COMPETITOR LINKS and ADD TO NAME
    products = Product.objects.all().order_by("?")
    for product in products:
        while True:
            try:
                from bs4 import BeautifulSoup
                from selenium import webdriver
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.chrome.service import Service
                from webdriver_manager.chrome import ChromeDriverManager

                options = Options()
                options.add_argument("--headless")

                options.add_argument("--no-sandbox")

                options.add_argument("--disable-dev-shm-usage")

                chrome_prefs = {}

                options.experimental_options["prefs"] = chrome_prefs
                chrome_prefs["profile.default_content_settings"] = {
                    "images": 2}

            # MAKE DICT COMPETITOR SETTINGS

                driver = webdriver.Chrome(service=Service(
                    ChromeDriverManager().install()), options=options)

                for key, value in product.competitor_json.items():
                    setting = competitor_settings[key]
                    driver.get(value)
                    # Delay to load the contents of the HTML FIle
                    time.sleep(4)
                    # Parse processed webpage with BeautifulSoup
                    soup = BeautifulSoup(driver.page_source,
                                         features="html.parser")
                    try:
                        parse_product(setting, soup, value, product)
                    except Exception as e:
                        print(value)
                        print(e)

                # Closing of the Chrome Driver
                driver.quit()
            except WebDriverException:
                continue
            break


@shared_task()
def parse_start_not_parsed():
    # BS4 IMPORTS
    import time
    from selenium.common.exceptions import WebDriverException
    from competitor.models import Competitor, CompetitorSetting
    from competitor.parser.product import parse_product
    from product.models import Product
    settings = CompetitorSetting.objects.all().select_related("competitor")
    competitor_settings = {}
    for s in settings:
        competitor_settings[s.competitor.url] = s
    # GET COMPETITOR LINKS and ADD TO NAME
    products = (
        Product.objects.all()
        .filter(competitor_json__isnull=False, competitor_products__isnull=True)
        .order_by("?")
    )
    for product in products:
        while True:
            try:
                from bs4 import BeautifulSoup
                from selenium import webdriver
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.chrome.service import Service
                from webdriver_manager.chrome import ChromeDriverManager

                from competitor.models import Competitor, CompetitorSetting
                from competitor.parser.product import parse_product
                from product.models import Product

                options = Options()
                options.add_argument("--headless")

                options.add_argument("--no-sandbox")

                options.add_argument("--disable-dev-shm-usage")

                chrome_prefs = {}

                options.experimental_options["prefs"] = chrome_prefs
                chrome_prefs["profile.default_content_settings"] = {
                    "images": 2}

                driver = webdriver.Chrome(service=Service(
                    ChromeDriverManager().install()), options=options)
                for key, value in product.competitor_json.items():
                    setting = competitor_settings[key]
                    driver.get(value)
                    # Delay to load the contents of the HTML FIle
                    time.sleep(4)
                    # Parse processed webpage with BeautifulSoup
                    soup = BeautifulSoup(
                        driver.page_source, features="html.parser")
                    try:
                        parse_product(setting, soup, value, product)
                    except Exception as e:
                        print(value)
                        print(e)

                # Closing of the Chrome Driver
                driver.quit()
            except WebDriverException:
                continue
            break


@shared_task()
def update_product_prices():
    # BS4 IMPORTS
    import time

    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    from competitor.models import Competitor, CompetitorProduct, CompetitorSetting
    from competitor.parser.product import update_price
    from product.models import Product

    options = Options()
    options.add_argument("--headless")

    options.add_argument("--no-sandbox")

    options.add_argument("--disable-dev-shm-usage")

    chrome_prefs = {}

    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    products = (
        CompetitorProduct.objects.all()
        .filter(price=0)
        .select_related("competitor")
        .select_related("competitor__setting")
    )
    for product in products:
        driver.get(product.url)
        # Delay to load the contents of the HTML FIle
        time.sleep(20)
        # Parse processed webpage with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        try:
            update_price(product.competitor.setting, soup, product.url)
        except Exception as e:
            print(product.url)
            print(e)

    # Closing of the Chrome Driver
    driver.quit()
