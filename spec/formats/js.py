import json

from specter import Spec, expect
from aumbry.formats.js import JsonConfig, JsonHandler

class TestConfig(JsonConfig):
    __mapping__ = {'nope': ['nope', str]}

class JsonSerialization(Spec):
    def can_serialize(self):
        cfg = TestConfig()
        cfg.nope = 'testing'

        handler = JsonHandler()
        raw = handler.serialize(cfg)

        res = json.loads(raw)
        expect(res['nope']).to.equal('testing')
