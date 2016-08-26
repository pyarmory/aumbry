from aumbry import contract
from specter import Spec, expect


class CheckContract(Spec):
    def attempting_to_inst_without_impl_raises_error(self):
        # Random Test Handler
        class Test(contract.AbstractHandler):
            pass

        expect(Test, []).to.raise_a(TypeError)
