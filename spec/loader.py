import os
import tempfile
from textwrap import dedent

import requests_mock
from specter import Spec, DataSpec, expect
from pike.discovery import py

from aumbry.errors import UnknownHandlerError, LoadError
from aumbry.formats import yml, js, consul
from aumbry import loader


raw_json = dedent("""
{
    "nope": "testing"
}
""")


raw_yaml = dedent("""
    ---
    nope: testing
""")


class SampleJsonConfig(js.JsonConfig):
    __mapping__ = {
        'nope': ['nope', str]
    }


class SampleYamlConfig(yml.YamlConfig):
    __mapping__ = {
        'nope': ['nope', str]
    }


def write_temp_file(raw):
    temp = tempfile.NamedTemporaryFile(delete=False)
    options = {'CONFIG_FILE_PATH': temp.name}

    with temp as fp:
        fp.write(bytes(raw.encode('utf-8')))

    return temp, options


class VerifyLoaderHandlingFileBased(DataSpec):
    DATASET = {
        'yaml': {'format': 'yaml', 'raw': raw_yaml, 'cls': SampleYamlConfig},
        'json': {'format': 'json', 'raw': raw_json, 'cls': SampleJsonConfig},
    }

    def can_load(self, format, raw, cls):
        temp, options = write_temp_file(raw)

        cfg = loader.load(format, cls, options)
        os.remove(temp.name)

        expect(cfg.nope).to.equal('testing')


class VerifyLoaderHandlingConsul(Spec):
    def can_successfully_load_from_consul(self):
        with requests_mock.Mocker() as mock:
            mock.get('http://bam/v1/kv/test_key', text=raw_yaml)

            options = {
                'CONSUL_URI': 'http://bam',
                'CONSUL_KEY': 'test_key',
            }

            cfg = loader.load('consul', SampleYamlConfig, options)
            expect(cfg.nope).to.equal('testing')

    def can_handle_404_from_consul(self):
        with requests_mock.Mocker() as mock:
            mock.get('http://bam/v1/kv/test_key', status_code=404)

            options = {
                'CONSUL_URI': 'http://bam',
                'CONSUL_KEY': 'test_key',
            }

            expect(
                loader.load,
                ['consul', SampleYamlConfig, options]
            ).to.raise_a(LoadError)

    def will_retry_on_other_codes(self):
        with requests_mock.Mocker() as mock:
            mock.get('http://bam/v1/kv/test_key', status_code=503)

            options = {
                'CONSUL_URI': 'http://bam',
                'CONSUL_KEY': 'test_key',
                'CONSUL_TIMEOUT': 1,
                'CONSUL_RETRY_INTERVAL': 1,
            }

            expect(
                loader.load,
                ['consul', SampleYamlConfig, options]
            ).to.raise_a(LoadError)

            expect(len(mock.request_history)).to.equal(2)


class CheckInvalidLoader(Spec):
    def raises_an_error(self):
        expect(loader.load, ['bam', None]).to.raise_a(UnknownHandlerError)


class CustomHanderPaths(Spec):
    def setting_a_valid_path(self):
        search_paths = py.get_module_by_name('aumbry.formats').__path__

        temp, options = write_temp_file(raw_yaml)

        cfg = loader.load(
            'yaml',
            SampleYamlConfig,
            options,
            search_paths=search_paths
        )
        os.remove(temp.name)

        expect(cfg.nope).to.equal('testing')

    def empty_list_raises_unknown_handler(self):
        expect(
            loader.load,
            ['bam', None, ['/tmp']]
        ).to.raise_a(UnknownHandlerError)




