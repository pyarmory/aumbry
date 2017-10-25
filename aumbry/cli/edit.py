import os
import subprocess

from aumbry.cli.utils import setup_up_config, save_temporary_config


def setup_arguments(subparsers):
    edit = subparsers.add_parser(
        'edit',
        help='Edits a configuration file'
    )
    edit.set_defaults(command='edit')

    edit.add_argument('--editor', type=str, help='Editor command to use')
    edit.add_argument('--fernet-key', type=str)
    edit.add_argument('path', type=str, help='Config file path')


@setup_up_config
def command(arguments):
    editor = arguments.editor or os.environ.get('EDITOR', 'vim')

    subprocess.call([editor, arguments.path])

    save_temporary_config(
        arguments.path,
        arguments.origin_path,
        arguments.fernet_key
    )
    print('Saved configuration to "{}"...'.format(arguments.origin_path))
