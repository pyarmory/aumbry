import tempfile

from cryptography.fernet import Fernet
from pretend import stub
from specter import Spec, expect
import yaml

from aumbry.cli.utils import setup_up_config, save_temporary_config

test_key = 'xngKx2POHOCQrmNjAli9A2yiZB55BfJrzm6bYB6oTQM='


def build_stub(path, key=None):
    return stub(path=path, fernet_key=key)


class CLIUtilities(Spec):
    def can_setup_an_encryped_config(self):
        arguments = build_stub('./spec/cli/encrypted_sample.yml', test_key)

        @setup_up_config
        def test(args):
            return yaml.full_load(open(args.path))

        data = test(arguments)
        expect(data['thing']).to.equal('other')
        expect(data['other']).to.equal('thing')

    def can_setup_an_empty_file(self):
        arguments = build_stub('./spec/cli/nope.yml')

        @setup_up_config
        def test(args):
            return yaml.full_load(open(args.path))

        data = test(arguments)
        assert data is None

    def can_save_an_encrypted_file(self):
        with tempfile.NamedTemporaryFile() as tp:
            save_temporary_config(
                './spec/cli/sample.yml',
                tp.name,
                test_key
            )

            with open(tp.name, 'rb') as fp:
                ct = fp.read()

        f = Fernet(test_key.encode('utf-8'))
        data = yaml.full_load(f.decrypt(ct))

        expect(data['thing']).to.equal('bam')
        expect(data['other']).to.equal('thing')
