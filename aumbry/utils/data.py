import base64


def b64decode_if_possible(value):
    try:
        return base64.b64decode(value)
    except Exception:
        return value
