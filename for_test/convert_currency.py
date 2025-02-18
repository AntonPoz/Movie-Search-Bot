from currency_converter import CurrencyConverter

def convert_currencys(amount, from_currency, to_currency):
    с = CurrencyConverter()
    try:
        converted_amount = с.convert(amount, from_currency, to_currency)
        return converted_amount
    except Exception as e:
        return f"Ошибка при конвертации валют: {e}"
