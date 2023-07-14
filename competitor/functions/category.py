def parse_category_products(site):
    # Base Libraries
    import time
    import traceback

    # BeautifulSoup Library used for Parsing the HTML
    from bs4 import BeautifulSoup

    # Selenium 4 for loading the Browser Driver
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    # Web Driver Manager
    from webdriver_manager.chrome import ChromeDriverManager

    from competitor.models import CATEGORY_URL, CompetitorUrls
    from competitor.parser.category import parse_category

    # Initialising the Chrome Driver
    options = Options()
    options.add_argument("--headless")

    options.add_argument("--no-sandbox")

    options.add_argument("--disable-dev-shm-usage")

    chrome_prefs = {}

    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    categories = CompetitorUrls.objects.filter(competitor=site, type=CATEGORY_URL)
    for category in categories:
        counter = 1
        while True:
            # if str(scrap.category_slug) in str(url):
            # Load the Docker Hub HTML page
            driver.get(f"{category.url}?{site.setting.page_pagination_slug}={counter}")
            # Delay to load the contents of the HTML FIle
            time.sleep(2)
            # Parse processed webpage with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, features="html.parser")
            try:
                parse_category(site, soup)
            except Exception as e:
                print(e)
                print(f"{category.url}?{site.setting.page_pagination_slug}={counter}")
                print(traceback.format_exc())
                print(site)
                break
            print(f"{category.url}?{site.setting.page_pagination_slug}={counter}")

            counter += 1

    # Closing of the Chrome Driver
    driver.quit()
