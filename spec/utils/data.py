import base64

from specter import Spec, expect

from aumbry.utils.data import b64decode_if_possible


class CheckOptionalBase64Decode(Spec):
    def decode_works(self):
        expected = b'something'
        encoded = base64.b64encode(expected)

        expect(b64decode_if_possible(encoded)).to.equal(expected)

    def invalid_data_returns_the_input(self):
        expected = {}
        expect(b64decode_if_possible(expected)).to.equal(expected)
