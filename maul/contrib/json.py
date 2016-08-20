from alchemize.transmute import JsonTransmuter
from alchemize.mapping import JsonMappedModel

from maul.contract import AbstractHandler
from maul.utils.file import load_file


class JsonHandler(AbstractHandler):
    @property
    def environment_var_prefix(self):
        return 'CONFIG_FILE'

    def fetch_config_data(self):
        path = self.vars['CONFIG_FILE_PATH']
        return load_file(path)

    def serialize(self, config):
        return JsonTransmuter.transmute_to(config)

    def deserialize(self, raw_config, config_cls):
        return JsonTransmuter.transmute_from(raw_config, config_cls)


class JsonConfig(JsonMappedModel):
    pass
