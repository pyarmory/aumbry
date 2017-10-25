from pike.discovery import py
from pike.manager import PikeManager

import aumbry
from aumbry.cli.utils import setup_up_config
from aumbry.formats.generic import GenericHandler
from aumbry.formats.yml import YamlHandler
from aumbry.formats.js import JsonHandler


@setup_up_config
def command(arguments):
    options = build_options(arguments)
    file_path = arguments.path
    input_handler = JsonHandler()
    output_handler = None

    if arguments.file_type == 'yml':
        input_handler = YamlHandler()

    if arguments.dest == aumbry.PARAM_STORE:
        output_handler = GenericHandler()

    if not has_required(arguments.dest, options):
        print('Missing required options for destination type')
        return 1

    package_ref, _, name = arguments.config_class.partition(':')
    if not name:
        print('config_class: requires a package and class reference')
        print('Example: my_package.sub:AppConfig')
        return 1

    with PikeManager([arguments.package_root]):
        module = py.get_module_by_name(package_ref)
        config_cls = getattr(module, name)

        print('Loading Config File...')
        cfg = aumbry.load(
            aumbry.FILE,
            config_cls,
            {'CONFIG_FILE_PATH': file_path},
            handler=input_handler
        )

        print('Uploading Config...')
        aumbry.save(
            arguments.dest,
            cfg,
            options,
            handler=output_handler
        )


def setup_arguments(subparsers):
    upload = subparsers.add_parser(
        'upload',
        help='Uploads a configuration file'
    )
    upload.set_defaults(command='upload')

    upload.add_argument('--package-root', type=str, default='./')
    upload.add_argument('--fernet-key', type=str)

    upload.add_argument('--consul-uri', type=str)
    upload.add_argument('--consul-key', type=str)

    upload.add_argument('--etcd2-uri', type=str)
    upload.add_argument('--etcd2-key', type=str)

    upload.add_argument('--param-store-region', type=str)
    upload.add_argument('--param-store-prefix', type=str)
    upload.add_argument('--param-store-access-id', type=str)
    upload.add_argument('--param-store-secret-key', type=str)
    upload.add_argument('--param-store-kms-key-id', type=str)

    upload.add_argument(
        '--file-type',
        type=str,
        help='Input File Type',
        choices=['yml', 'json'],
        default='json'
    )

    upload.add_argument('path', type=str, help='Config file path')
    upload.add_argument('config_class', type=str, help='Configuration Class')
    upload.add_argument(
        'dest',
        type=str,
        help='Destination Type',
        choices=[
            aumbry.ETCD2,
            aumbry.CONSUL,
            aumbry.PARAM_STORE
        ]
    )


def build_options(arguments):
    full_options = {
        'CONSUL_URI': arguments.consul_uri,
        'CONSUL_KEY': arguments.consul_key,
        'ETCD2_URI': arguments.etcd2_uri,
        'ETCD2_KEY': arguments.etcd2_key,
        'PARAMETER_STORE_AWS_REGION': arguments.param_store_region,
        'PARAMETER_STORE_PREFIX': arguments.param_store_prefix,
        'PARAMETER_STORE_AWS_ACCESS_ID': arguments.param_store_access_id,
        'PARAMETER_STORE_AWS_ACCESS_SECRET': arguments.param_store_secret_key,
        'PARAMETER_STORE_AWS_KMS_KEY_ID': arguments.param_store_kms_key_id,
    }

    return {k: v for k, v in full_options.items() if v}


def has_required(dest_type, options):
    required = {
        aumbry.PARAM_STORE: [
            'PARAMETER_STORE_AWS_REGION',
            'PARAMETER_STORE_PREFIX'
        ],
        aumbry.CONSUL: [
            'CONSUL_URI',
            'CONSUL_KEY'
        ],
        aumbry.ETCD2: [
            'ETCD2_URI',
            'ETCD2_KEY'
        ],
    }

    return all(key in options for key in required[dest_type])
