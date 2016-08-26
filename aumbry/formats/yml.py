from alchemize.transmute import JsonTransmuter
from alchemize.mapping import JsonMappedModel

from aumbry.formats import json


class YamlHandler(json.JsonHandler):
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


# NOTE: The JsonMappedModel type should be sufficent for what we're doing;
# However, we're setting up a different type in-case it isn't, so we don't
# break a contract.
class YamlConfig(JsonMappedModel):
    pass
