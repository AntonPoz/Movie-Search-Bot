from typing import List
import pycountry
from for_test.translate_string import translate_to_english
from for_test.convert_currency import convert_currencys

def convert_amount(curency: List, country: str) -> List:
    country_name = translate_to_english(country)
    convert_list = []
    try:
        country = pycountry.countries.search_fuzzy(country_name)[0]
        currency = pycountry.currencies.get(numeric=country.numeric).alpha_3
        for amount in curency:
            convert_currency = round(convert_currencys(amount, currency, 'USD'))
            convert_list.append(convert_currency)
        return convert_list
    except LookupError:
        return "Страна не найдена"
    except Exception as e:
        return f"Ошибка: {e}"

result = convert_amount([50000000, 1000000000], 'Russian Federation')
print(result)