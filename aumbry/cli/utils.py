import os
import tempfile

from cryptography.fernet import Fernet


def setup_up_config(func):
    def wrapper(arguments):
        _, ext = os.path.splitext(arguments.path)
        file_data = b''

        if os.path.exists(arguments.path):
            with open(arguments.path, 'rb') as fp:
                file_data = fp.read()

        if file_data and arguments.fernet_key:
            f = Fernet(arguments.fernet_key.encode('utf-8'))
            file_data = f.decrypt(file_data)

        with tempfile.NamedTemporaryFile(suffix=ext) as fp:
            fp.write(file_data)
            fp.file.flush()

            arguments.origin_path = arguments.path
            arguments.path = fp.name

            return func(arguments)

    return wrapper


def save_temporary_config(temp_file_path, output_path, fernet_key=None):
    with open(temp_file_path, 'rb') as fp:
        file_data = fp.read()

    if fernet_key:
        f = Fernet(fernet_key.encode('utf-8'))
        file_data = f.encrypt(file_data)

    with open(output_path, 'wb') as fp:
        fp.write(file_data)
