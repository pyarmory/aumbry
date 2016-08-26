import os
import tempfile
from textwrap import dedent

from specter import DataSpec, expect
from aumbry.formats import yml
from aumbry import loader


raw_yaml = dedent("""
    ---
    nope: testing
""")


class SampleYamlConfig(yml.YamlConfig):
    __mapping__ = {
        'nope': ['nope', str]
    }


class VerifyLoaderTypes(DataSpec):
    DATASET = {
        'yaml': {'format': 'yaml', 'raw': raw_yaml, 'cls': SampleYamlConfig}
    }

    def can_load(self, format, raw, cls):
        temp = tempfile.NamedTemporaryFile(delete=False)
        options = {'CONFIG_FILE_PATH': temp.name}

        with temp as fp:
            fp.write(bytes(raw.encode('utf-8')))

        cfg = loader.load(format, cls, options)
        os.remove(temp.name)

        expect(cfg.nope).to.equal('testing')
