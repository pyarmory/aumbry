from specter import Spec, expect
from aumbry.formats import generic


class TestConfig(generic.GenericConfig):
    __mapping__ = {'nope': ['nope', str]}


class GenericHandler(Spec):
    def list_required_imports(self):
        handler = generic.GenericHandler()
        expect(handler.imports).to.equal([])

    def can_serialize(self):
        cfg = TestConfig()
        cfg.nope = 'testing'

        handler = generic.GenericHandler()
        raw = handler.serialize(cfg)

        expect(type(raw)).to.equal(dict)
        expect(raw['nope']).to.equal('testing')

    def can_deserialize(self):
        handler = generic.GenericHandler()
        cfg = handler.deserialize({'nope': 'testing'}, TestConfig)

        expect(cfg.nope).to.equal('testing')
