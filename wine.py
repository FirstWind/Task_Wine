from collections import defaultdict
from datetime import date

import pandas

import main

BIRTHDAY_FACTORY_YEAR = 1920


def get_wines():
    xls_path = main.get_config_param("wine", "path")
    wine_category = main.get_config_param("wine", "wine_category")

    data_from_excel = pandas.read_excel(
        xls_path, sheet_name='Лист1',
        na_values=['N/A', 'NA'], keep_default_na=False
        )

    wines = data_from_excel.to_dict(orient='records')

    out_wines = defaultdict(list)
    for item in wines:
        out_wines[item[wine_category]].append(item)
    return out_wines


def get_age_factory():
    age = date.today().year - BIRTHDAY_FACTORY_YEAR

    if age % 10 == 1 and age != 11 and age % 100 != 11:
        age = f"{age} год"
    elif 1 < age % 10 <= 4 and age != 12 and age != 13 and age != 14:
        age = f"{age} года"
    else:
        age = f"{age} лет"
    return age
