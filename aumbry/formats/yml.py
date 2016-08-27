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
        return yaml.dump(config_dict)

    def deserialize(self, raw_config, config_cls):
        import yaml

        config_dict = yaml.load(raw_config)
        return JsonTransmuter.transmute_from(config_dict, config_cls)


class YamlConfig(AumbryConfig):
    """ A type of AumbryConfig for Yaml Configurations."""
    __handler__ = YamlHandler
