from bs4 import BeautifulSoup


def parse_avtoelon_detail(html) -> dict:
    avto = {
        "price": "",
        "brand": "",
        "model": "",
        "position": "",
        "city": "",
        "year": "",
        "engine_capacity": "",
        "engine_fuel": "",
        "body_type": "",
        "transmission": "",
        "drive_unit": "",
        "description": "",
    }
    soup = BeautifulSoup(html, "html.parser")
    item = soup.find("div", {"class": "item product"})

    title = soup.find("h1", {"class": "a-title__text"})
    avto["brand"] = clean_str(title.find("span", {"itemprop": "brand"}).text)
    if "," in title.text:
        avto["position"] = clean_str(title.text.split(",")[1])
    avto["model"] = clean_str(title.find("span", {"itemprop": "name"}).text)

    avto["price"] = clean_number(
        item.find("span", {"class": "a-price__text"}).text)

    # DETAILS
    description_params = item.find(
        "dl", {"class": "clearfix dl-horizontal description-params"})
    params_titles = []
    for dt in description_params.find_all("dt"):
        params_titles.append(dt.text.strip())

    params_values = []
    for dd in description_params.find_all("dd"):
        params_values.append(dd.text.strip())
    for index, value in enumerate(params_titles):
        if value == "Город":
            avto["city"] = params_values[index]
        if value == "Год":
            avto["year"] = int(params_values[index])
        elif value == "Объем двигателя, л":
            avto["engine_capacity"] = (params_values[index].split("(")[
                0].strip())
            avto["engine_fuel"] = clean_str(params_values[index].split("(")[1])
        elif value == "Кузов":
            avto["body_type"] = params_values[index]
        elif value == "Коробка передач":
            avto["transmission"] = params_values[index]
        elif value == "Привод":
            avto["drive_unit"] = params_values[index]

    return avto


def clean_str(s: str) -> str:
    s = s.replace("\n", "").replace("\t", "")
    res_s = ""
    for i in s:
        if i.isalpha() or i.isdigit() or i == " ":
            res_s = "".join([res_s, i])
    return res_s.strip()


def clean_number(s: str) -> str:
    s = s.replace("\n", "").replace("\t", "")
    res_s = ""
    for i in s:
        if i.isdigit():
            res_s = "".join([res_s, i])
    return res_s.strip()
