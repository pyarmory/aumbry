import os

from aumbry.contract import AbstractSource
from aumbry.sources import SourceTypes
from aumbry.utils.file import load_file, save_file


class FernetFileSource(AbstractSource):
    extras_name = SourceTypes.fernet

    @property
    def imports(self):
        return ['cryptography']

    @property
    def environment_var_prefix(self):
        return 'CONFIG_FILE'

    def fetch_config_data(self, cfg_class):
        from cryptography.fernet import Fernet

        path = os.path.abspath(self.vars['CONFIG_FILE_PATH'])
        key = self.vars['CONFIG_FILE_FERNET_KEY']

        ct = load_file(path)

        f = Fernet(key.encode('utf-8'))
        pt = f.decrypt(ct)

        return pt

    def save_config_data(self, data, handler, cfg):
        from cryptography.fernet import Fernet

        path = os.path.abspath(self.vars['CONFIG_FILE_PATH'])
        key = self.vars['CONFIG_FILE_FERNET_KEY']

        f = Fernet(key.encode('utf-8'))
        ct = f.encrypt(data)

        return save_file(path, ct)
