from aumbry import contract, errors
from specter import Spec, expect


class TestContract(contract.AbstractHandler):
    extras_name = 'tester'
    imports = ['nope_nope_nope']

    def fetch_config_data(self):
        pass

    def deserialize(self, raw_config, config_cls):
        pass

    def serialize(self, config):
        pass

    @property
    def environment_var_prefix(self):
        return 'bam'


class CheckContract(Spec):
    def attempting_to_inst_without_impl_raises_error(self):
        # Random Test Handler
        class Test(contract.AbstractHandler):
            pass

        expect(Test, []).to.raise_a(TypeError)

    def bad_import_raises_dep_error(self):
        ct = TestContract()
        expect(ct.import_requirements, []).to.raise_a(errors.DependencyError)

    def handle_tuple_imports(self):
        ct = TestContract()
        ct.imports = [('nope_nope_nope', 'the_nope_package')]
        expect(ct.import_requirements, []).to.raise_a(errors.DependencyError)


class CheckConfigExtras(Spec):
    def is_iterable(self):
        class TestConfig(contract.AumbryConfig):
            __mapping__ = {
                'test': ['test', str],
                'another': ['another', str],
            }

        tester = TestConfig()
        tester.test = 'thing'

        expect('test').to.be_in(tester)
        expect(['test']).to.equal(list(tester))
