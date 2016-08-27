import os
import mock
import six
import tempfile

from specter import Spec, expect
from aumbry.errors import LoadError
from aumbry.utils.file import load_file


class VerifyFileUtils(Spec):
    def before_each(self):
        self.cfg_file = tempfile.NamedTemporaryFile(delete=False)

        with self.cfg_file as fp:
            fp.write(b'bam')

    def after_each(self):
        os.remove(self.cfg_file.name)

    def can_load_file(self):
        data = load_file(self.cfg_file.name)
        expect(data).to.equal(b'bam')

    def bad_path_raises_error(self):
        expect(load_file, ['nope']).to.raise_a(LoadError)

    def error_during_open_or_read_raises_error(self):
        def magic_open(fn, mode):
            raise LoadError()

        open_mock = mock.MagicMock()
        open_mock.side_effect = magic_open
        raised_error = False

        patch_name = '{}.open'.format(six.moves.builtins.__name__)
        with mock.patch(patch_name, open_mock):
            # Doing this manually as test suites use open()
            try:
                load_file(self.cfg_file.name)
            except LoadError:
                raised_error = True

        expect(raised_error).to.be_true()
