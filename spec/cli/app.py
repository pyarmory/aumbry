import subprocess

import mock
from pretend import stub
from specter import Spec, expect

import aumbry
from aumbry.cli import app
from aumbry.formats.js import JsonHandler
from aumbry.formats.yml import YamlHandler
from spec.utils import OutputCapture


class CLIBehaviors(Spec):
    def before_each(self):
        self.load_patch = mock.patch.object(aumbry, 'load')
        self.save_patch = mock.patch.object(aumbry, 'save')

        self.load_mock = self.load_patch.start()
        self.save_mock = self.save_patch.start()

    def after_each(self):
        self.load_patch.stop()
        self.save_patch.stop()

    def can_upload(self):
        with OutputCapture():
            app.main([
                'upload',
                '--file-type', 'yml',
                './spec/cli/sample.yml',
                'spec.cli.app:SampleConfig',
                aumbry.PARAM_STORE,
                '--param-store-region', 'us-east-1',
                '--param-store-prefix', 'aumbry/testing'
            ])

        expect(self.load_mock.call_count).to.equal(1)
        expect(self.save_mock.call_count).to.equal(1)

        args, kwargs = self.load_mock.call_args

        assert SampleConfig.__name__ == args[1].__name__
        assert 'CONFIG_FILE_PATH' in args[2]
        assert type(kwargs['handler']) == YamlHandler

    def file_type_defaults_to_json(self):
        with OutputCapture():
            app.main([
                'upload',
                './spec/cli/sample.js',
                'spec.cli.app:SampleConfig',
                aumbry.PARAM_STORE,
                '--param-store-region', 'us-east-1',
                '--param-store-prefix', 'aumbry/testing'
            ])

        expect(self.load_mock.call_count).to.equal(1)
        expect(self.save_mock.call_count).to.equal(1)

        args, kwargs = self.load_mock.call_args

        assert SampleConfig.__name__ == args[1].__name__
        assert 'CONFIG_FILE_PATH' in args[2]
        assert type(kwargs['handler']) == JsonHandler

    def output_handler_defaults_to_none(self):
        with OutputCapture():
            app.main([
                'upload',
                './spec/cli/sample.js',
                'spec.cli.app:SampleConfig',
                aumbry.CONSUL,
                '--consul-uri', 'https://locahost:10000/nope',
                '--consul-key', 'aumbry/testing'
            ])

        expect(self.load_mock.call_count).to.equal(1)
        expect(self.save_mock.call_count).to.equal(1)

        args, kwargs = self.load_mock.call_args

        assert SampleConfig.__name__ == args[1].__name__
        assert 'CONFIG_FILE_PATH' in args[2]
        assert type(kwargs['handler']) == JsonHandler

        args, kwargs = self.save_mock.call_args
        assert kwargs['handler'] is None

    def missing_options_fails(self):
        with OutputCapture() as output:
            app.main([
                'upload',
                '--file-type', 'yml',
                './spec/cli/sample.yml',
                'spec.cli.app:SampleConfig',
                aumbry.PARAM_STORE,
            ])

        assert output == ['Missing required options for destination type']

    def malformed_package_name_fails(self):
        with OutputCapture() as output:
            app.main([
                'upload',
                '--file-type', 'yml',
                './spec/cli/sample.yml',
                'spec.cli.nope',
                aumbry.PARAM_STORE,
                '--param-store-region', 'us-east-1',
                '--param-store-prefix', 'aumbry/testing'
            ])

        assert output == [
            'config_class: requires a package and class reference',
            'Example: my_package.sub:AppConfig'
        ]

    def edit_executes_against_a_file(self):
        with mock.patch.object(subprocess, 'call') as call_mock:
            with OutputCapture() as output:
                app.main(['edit', './spec/cli/sample.yml'])

        cmd, path = call_mock.call_args[0][0]

        assert call_mock.called
        assert cmd == 'vim'
        assert path is not None
        assert output == ['Saved configuration to "./spec/cli/sample.yml"...']

    def invalid_command_returns_none(self):
        with mock.patch.object(app, 'parse_arguments') as parse_mock:
            parse_mock.return_value = stub(command='nope')

            assert app.main(['nope']) is None


class SampleConfig(aumbry.YamlConfig):
    __mapping__ = {
        'thing': aumbry.Attr('thing', str),
        'other': aumbry.Attr('other', str),
    }
