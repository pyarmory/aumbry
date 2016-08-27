import yaml

from specter import Spec, expect
from aumbry.formats.yml import YamlConfig, YamlHandler

class TestConfig(YamlConfig):
    __mapping__ = {'nope': ['nope', str]}

class YamlSerialization(Spec):
    def can_serialize(self):
        cfg = TestConfig()
        cfg.nope = 'testing'

        handler = YamlHandler()
        raw = handler.serialize(cfg)

        res = yaml.load(raw)
        expect(res['nope']).to.equal('testing')
