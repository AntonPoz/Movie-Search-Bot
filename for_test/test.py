def extract_json_value(item, keys: list, default_value='-') -> str:
    try:
        for key in keys:
            item = item[key]
            if type(item) == list:
                result_string = str()
                for extract_item in item:
                    if result_string:
                        result_string += ', '
                    result_string += str(list(extract_item.values())[0])
                return result_string
        if item:
            return item
    except Exception:
        pass
    return default_value

genres = {'genres': [{'name': 'документальный'}, {'name': 'история'}]}
print(extract_json_value(genres, ['genres']))