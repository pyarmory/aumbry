import os
from aumbry.errors import LoadError, SaveError


def load_file(filename):
    if not os.path.exists(filename):
        raise LoadError('Path {}, doesn\'t exist!'.format(filename))

    try:
        with open(filename, 'rb') as fp:
            return fp.read()
    except Exception as e:
        raise LoadError(str(e))


def save_file(filename, data):
    try:
        with open(filename, 'wb') as fp:
            return fp.write(data)
    except Exception as e:
        raise SaveError(str(e))
