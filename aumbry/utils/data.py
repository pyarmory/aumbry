import base64


def b64decode_if_possible(value):
    try:
        return base64.b64decode(value)
    except Exception:
        return value


def nested_dict_set(input_dict, level_keys, val):
    for key in level_keys[:-1]:
        input_dict = input_dict.setdefault(key, {})

    input_dict[level_keys[-1]] = val
