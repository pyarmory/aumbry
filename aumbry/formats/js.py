from alchemize.transmute import JsonTransmuter

from aumbry.contract import AbstractHandler, AumbryConfig


class JsonHandler(AbstractHandler):
    extras_name = 'json'

    @property
    def imports(self):
        return ['json']

    def serialize(self, config):
        return JsonTransmuter.transmute_to(config).encode('utf-8')

    def deserialize(self, raw_config, config_cls):
        return JsonTransmuter.transmute_from(
            raw_config.decode('utf-8'),
            config_cls
        )

    def parse(self, raw_config):
        import json
        return json.loads(raw_config)


class JsonConfig(AumbryConfig):
    """ A type of AumbryConfig for JSON Configurations."""
    __handler__ = JsonHandler
