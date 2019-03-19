from alchemize.transmute import JsonTransmuter

from aumbry.contract import AumbryConfig
from aumbry.formats import js


class YamlHandler(js.JsonHandler):
    extras_name = 'yaml'

    @property
    def imports(self):
        return ['yaml']

    def serialize(self, config):
        import yaml

        config_dict = JsonTransmuter.transmute_to(config, to_string=False)
        return yaml.dump(config_dict, default_flow_style=False).encode('utf-8')

    def deserialize(self, raw_config, config_cls):
        config_dict = self.parse(raw_config)
        return JsonTransmuter.transmute_from(config_dict, config_cls)

    def parse(self, raw_config):
        import yaml

        return yaml.full_load(raw_config)


class YamlConfig(AumbryConfig):
    """ A type of AumbryConfig for Yaml Configurations."""
    __handler__ = YamlHandler
