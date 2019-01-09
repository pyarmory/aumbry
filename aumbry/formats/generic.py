from alchemize.transmute import JsonTransmuter

from aumbry.contract import AbstractHandler, AumbryConfig


class GenericHandler(AbstractHandler):
    extras_name = 'generic'

    @property
    def imports(self):
        return []

    def serialize(self, config):
        return JsonTransmuter.transmute_to(config, to_string=False)

    def deserialize(self, raw_config, config_cls):
        return JsonTransmuter.transmute_from(raw_config, config_cls)

    def parse(self, raw_config):
        return raw_config


class GenericConfig(AumbryConfig):
    """ A type of AumbryConfig for Generic Dict Configurations."""
    __handler__ = GenericHandler
