def find_value_in_json(data: dict, target_value: str) -> bool:
    if isinstance(data, dict):
        for key, value in data.items():
            if value == target_value:
                return True
            elif isinstance(value, dict) or isinstance(value, list):
                if find_value_in_json(value, target_value):
                    return True
    elif isinstance(data, list):
        for item in data:
            if item == target_value:
                return True
            elif isinstance(item, dict) or isinstance(item, list):
                if find_value_in_json(item, target_value):
                    return True
    return False
