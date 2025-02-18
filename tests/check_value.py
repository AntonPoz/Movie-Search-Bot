from config_data.config import DATE_FORMAT
from datetime import datetime


def check_date(date: str) -> [str, bool]:
    formatted_date = date
    separators = [' ', '/', '\\', '.', ':', ',']
    for symbol in formatted_date:
        if symbol in separators:
            formatted_date = formatted_date.replace(symbol, '-')
            break
    try:
        datetime.strptime(formatted_date, DATE_FORMAT)
        return [formatted_date, True]
    except ValueError:
        raise ValueError([date, False])
