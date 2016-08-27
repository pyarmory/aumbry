from alchemize.transmute import JsonTransmuter
from alchemize.mapping import JsonMappedModel

from aumbry.contract import AbstractHandler
from aumbry.utils.file import load_file


class JsonHandler(AbstractHandler):
    extras_name = 'json'

    @property
    def imports(self):
        return ['json']

    @property
    def environment_var_prefix(self):
        return 'CONFIG_FILE'

    def fetch_config_data(self):
        path = self.vars['CONFIG_FILE_PATH']
        return load_file(path)

    def serialize(self, config):
        return JsonTransmuter.transmute_to(config)

    def deserialize(self, raw_config, config_cls):
        return JsonTransmuter.transmute_from(
            raw_config.decode('utf-8'),
            config_cls
        )


class JsonConfig(JsonMappedModel):
    __handler__ = JsonHandler
