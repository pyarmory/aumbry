import base64
import json
import os
import tempfile
from textwrap import dedent

from cryptography.fernet import Fernet
import requests_mock
from specter import Spec, DataSpec, expect
from six.moves import urllib
from moto import mock_ssm
from pike.discovery import py

import aumbry
from aumbry.errors import LoadError, SaveError, UnknownSourceError
from aumbry.formats.generic import GenericHandler


raw_json = dedent("""
{
    "nope": "testing"
}
""")


raw_yaml = dedent("""
    nope: testing
""")


partial_yaml1 = dedent("""
    nope: testing
    sample_list:
      - list1
""")


partial_yaml2 = dedent("""
    sample_list:
      - list2
    sample_dict:
        which: 2
        a: b
""")


partial_yaml3 = dedent("""
    sample_dict:
        which: 3
        c: d
""")


class SampleJsonConfig(aumbry.JsonConfig):
    __mapping__ = {
        'nope': ['nope', str]
    }


class SampleYamlConfig(aumbry.YamlConfig):
    __mapping__ = {
        'nope': ['nope', str]
    }


class SampleExtendedYamlConfig(aumbry.YamlConfig):
    __mapping__ = {
        'nope': ['nope', str],
        'sample_list': ['sample_list', list],
        'sample_dict': ['sample_dict', dict],
    }


class SampleGenericConfig(aumbry.GenericConfig):
    __mapping__ = {
        'nope': ['nope', str],
        'sample_list': ['sample_list', list],
        'sample_dict': ['sample_dict', dict],
        'sample_model': ['sample_model', SampleJsonConfig],
    }


def write_temp_file(raw):
    temp = tempfile.NamedTemporaryFile(delete=False)
    options = {'CONFIG_FILE_PATH': temp.name}

    with temp as fp:
        fp.write(bytes(raw.encode('utf-8')))

    return temp, options


class VerifyLoaderHandlingFileBased(DataSpec):
    DATASET = {
        'yaml': {'raw': raw_yaml, 'cls': SampleYamlConfig},
        'json': {'raw': raw_json, 'cls': SampleJsonConfig},
    }

    def can_load(self, raw, cls):
        temp, options = write_temp_file(raw)

        cfg = aumbry.load(aumbry.FILE, cls, options)
        os.remove(temp.name)

        expect(cfg.nope).to.equal('testing')

    def can_save(self, raw, cls):
        cfg = cls()
        cfg.nope = 'testing'

        with tempfile.NamedTemporaryFile() as temp:
            options = {'CONFIG_FILE_PATH': temp.name}
            aumbry.save(aumbry.FILE, cfg, options)

            # Load up the saved file
            loaded_cfg = aumbry.load(aumbry.FILE, cls, options)
            expect(loaded_cfg.nope).to.equal(cfg.nope)

    def can_use_preprocessors(self, raw, cls):
        cfg = cls()
        cfg.nope = 'testing'

        with tempfile.NamedTemporaryFile() as temp:
            options = {'CONFIG_FILE_PATH': temp.name}
            aumbry.save(
                aumbry.FILE,
                cfg,
                options,
                preprocessor=lambda data: base64.b64encode(data)
            )

            expect('testing').not_to.be_in(temp.file.read().decode('utf-8'))

            # Load up the saved file
            loaded_cfg = aumbry.load(
                aumbry.FILE,
                cls,
                options,
                preprocessor=lambda data: base64.b64decode(data)
            )
            expect(loaded_cfg.nope).to.equal(cfg.nope)


class VerifyLoaderHandlingFernetFile(Spec):
    def can_save_and_load(self):
        cfg = SampleYamlConfig()
        cfg.nope = 'testing'

        with tempfile.NamedTemporaryFile() as temp:
            options = {
                'CONFIG_FILE_PATH': temp.name,
                'CONFIG_FILE_FERNET_KEY': Fernet.generate_key().decode('utf-8')
            }
            aumbry.save(aumbry.FERNET, cfg, options)

            # Load up the saved file
            loaded_cfg = aumbry.load(aumbry.FERNET, SampleYamlConfig, options)
            expect(loaded_cfg.nope).to.equal(cfg.nope)


class VerifyLoaderHandlingConsul(Spec):
    def can_successfully_load_from_consul(self):
        with requests_mock.Mocker() as mock:
            value = base64.b64encode(raw_yaml.encode('utf-8'))
            resp = [{
                'Value': value.decode('utf-8')
            }]
            mock.get('http://bam/v1/kv/test_key', text=json.dumps(resp))

            options = {
                'CONSUL_URI': 'http://bam',
                'CONSUL_KEY': 'test_key',
            }

            cfg = aumbry.load(aumbry.CONSUL, SampleYamlConfig, options)
            expect(cfg.nope).to.equal('testing')

    def can_handle_404_from_consul(self):
        with requests_mock.Mocker() as mock:
            mock.get('http://bam/v1/kv/test_key', status_code=404)

            options = {
                'CONSUL_URI': 'http://bam',
                'CONSUL_KEY': 'test_key',
            }

            expect(
                aumbry.load,
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
                aumbry.load,
                ['consul', SampleYamlConfig, options]
            ).to.raise_a(LoadError)

            expect(len(mock.request_history)).to.equal(2)

    def save_raises_a_not_implemented_error(self):
        cfg = SampleYamlConfig()
        cfg.nope = 'testing'
        expect(
            aumbry.save,
            [aumbry.CONSUL, cfg, {}]
        ).to.raise_a(NotImplementedError)


class VerifyLoaderHandlingEtcd2(Spec):
    def can_successfully_load_yaml_from_etcd(self):
        with requests_mock.Mocker() as mock:
            value = base64.b64encode(raw_yaml.encode('utf-8'))
            resp = {
                'node': {
                    'value': value.decode('utf-8'),
                },
            }
            mock.get('http://bam/v2/keys/test_key', text=json.dumps(resp))

            options = {
                'ETCD2_URI': 'http://bam',
                'ETCD2_KEY': 'test_key',
            }

            cfg = aumbry.load(aumbry.ETCD2, SampleYamlConfig, options)
            expect(cfg.nope).to.equal('testing')

    def can_successfully_save_to_etcd(self):
        with requests_mock.Mocker() as mock:
            mock_save = mock.put(
                'http://bam/v2/keys/test_key',
                status_code=201,
                text='{}'
            )

            cfg = SampleYamlConfig()
            cfg.nope = 'testing'

            aumbry.save(
                aumbry.ETCD2,
                cfg,
                options={
                    'ETCD2_URI': 'http://bam',
                    'ETCD2_KEY': 'test_key',
                }
            )

            body = urllib.parse.unquote(mock_save.last_request.text)
            expect(body).to.equal('value=bm9wZTogdGVzdGluZwo=')

    def can_successfully_update_existing_in_etcd(self):
        with requests_mock.Mocker() as mock:
            mock_save = mock.put(
                'http://bam/v2/keys/test_key',
                status_code=200,
                text='{}'
            )

            cfg = SampleYamlConfig()
            cfg.nope = 'testing'

            aumbry.save(
                aumbry.ETCD2,
                cfg,
                options={
                    'ETCD2_URI': 'http://bam',
                    'ETCD2_KEY': 'test_key',
                }
            )

            body = urllib.parse.unquote(mock_save.last_request.text)
            expect(body).to.equal('value=bm9wZTogdGVzdGluZwo=')

    def handles_save_failure(self):
        with requests_mock.Mocker() as mock:
            mock.put(
                'http://bam/v2/keys/test_key',
                status_code=400,
                text='{}'
            )

            args = [
                aumbry.ETCD2,
                SampleYamlConfig(),
                {
                    'ETCD2_URI': 'http://bam',
                    'ETCD2_KEY': 'test_key',
                }
            ]

            expect(aumbry.save, args).to.raise_a(SaveError)

    def can_handle_404_from_consul(self):
        with requests_mock.Mocker() as mock:
            mock.get('http://bam/v2/keys/test_key', status_code=404)

            options = {
                'ETCD2_URI': 'http://bam',
                'ETCD2_KEY': 'test_key',
            }

            expect(
                aumbry.load,
                ['etcd2', SampleYamlConfig, options]
            ).to.raise_a(LoadError)

    def will_retry_on_other_codes(self):
        with requests_mock.Mocker() as mock:
            mock.get('http://bam/v2/keys/test_key', status_code=503)

            options = {
                'ETCD2_URI': 'http://bam',
                'ETCD2_KEY': 'test_key',
                'ETCD2_TIMEOUT': 1,
                'ETCD2_RETRY_INTERVAL': 1,
            }

            expect(
                aumbry.load,
                ['etcd2', SampleYamlConfig, options]
            ).to.raise_a(LoadError)

            expect(len(mock.request_history)).to.equal(2)


class VerifyLoaderHandlingParameterStore(Spec):
    def can_successfully_save_and_load(self):
        with mock_ssm():
            options = {
                'PARAMETER_STORE_AWS_REGION': 'us-west-2',
                'PARAMETER_STORE_PREFIX': '/aumbry-test',
            }
            expected_cfg = SampleGenericConfig()
            expected_cfg.nope = 'testing'
            expected_cfg.sample_list = ['trace']
            expected_cfg.sample_dict = {'trace': 'boom'}
            expected_cfg.sample_model = SampleJsonConfig()
            expected_cfg.sample_model.nope = 'testing2'

            # Save Sample Config
            aumbry.save(
                aumbry.PARAM_STORE,
                expected_cfg,
                options
            )

            # Retrieve back the config
            cfg = aumbry.load(
                aumbry.PARAM_STORE,
                SampleGenericConfig,
                options
            )

        expect(cfg.nope).to.equal(expected_cfg.nope)
        expect(cfg.sample_dict).to.equal({'trace': 'boom'})
        expect(cfg.sample_list).to.equal(expected_cfg.sample_list)
        expect(cfg.sample_model.nope).to.equal(expected_cfg.sample_model.nope)

    def can_use_yaml_cfg_with_handler_override(self):
        with mock_ssm():
            options = {
                'PARAMETER_STORE_AWS_REGION': 'us-west-2',
                'PARAMETER_STORE_PREFIX': '/aumbry-test',
            }

            expected_cfg = SampleYamlConfig()
            expected_cfg.nope = 'testing'

            handler = GenericHandler()

            # Save Sample Config
            aumbry.save(
                aumbry.PARAM_STORE,
                expected_cfg,
                options,
                handler=handler
            )

            # Retrieve back the config
            cfg = aumbry.load(
                aumbry.PARAM_STORE,
                SampleGenericConfig,
                options,
                handler=handler
            )

        expect(cfg.nope).to.equal(expected_cfg.nope)


class CheckInvalidLoader(Spec):
    def raises_an_error(self):
        expect(aumbry.load, ['bam', None]).to.raise_a(UnknownSourceError)
        expect(aumbry.save, ['bam', None]).to.raise_a(UnknownSourceError)


class CustomSourcePluginPaths(Spec):
    def setting_a_valid_path(self):
        search_paths = py.get_module_by_name('aumbry.sources').__path__

        temp, options = write_temp_file(raw_yaml)

        cfg = aumbry.load(
            'file',
            SampleYamlConfig,
            options,
            search_paths=search_paths
        )
        os.remove(temp.name)

        expect(cfg.nope).to.equal('testing')

    def empty_list_raises_unknown_source(self):
        expect(
            aumbry.load,
            ['bam', None, ['/tmp']]
        ).to.raise_a(UnknownSourceError)


class VerifyMergingMultipleConfigs(Spec):
    def can_merge_multiple_yaml(self):
        temp1, options1 = write_temp_file(partial_yaml1)
        temp2, options2 = write_temp_file(partial_yaml2)
        temp3, options3 = write_temp_file(partial_yaml3)

        cfg = aumbry.merge(SampleExtendedYamlConfig, (
            {
                'source_name': 'file',
                'options': options1,
            },
            {
                'source_name': 'file',
                'options': options2,
            },
            {
                'source_name': 'file',
                'options': options3,
            },
        ))

        os.remove(temp1.name)
        os.remove(temp2.name)
        os.remove(temp3.name)

        expect(cfg.nope).to.equal('testing')
        expect(cfg.sample_list).to.equal(['list2'])
        expect(cfg.sample_dict).to.equal({'which': 3, 'a': 'b', 'c': 'd'})
