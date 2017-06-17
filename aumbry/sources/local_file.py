from aumbry.contract import AbstractSource
from aumbry.sources import SourceTypes
from aumbry.utils.file import load_file, save_file


class FileSource(AbstractSource):
    extras_name = SourceTypes.file

    @property
    def imports(self):
        return []

    @property
    def environment_var_prefix(self):
        return 'CONFIG_FILE'

    def fetch_config_data(self):
        path = self.vars['CONFIG_FILE_PATH']
        return load_file(path)

    def save_config_data(self, data, handler):
        path = self.vars['CONFIG_FILE_PATH']
        return save_file(path, data)
