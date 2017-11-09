from aumbry.cli.utils import setup_up_config


def setup_arguments(subparsers):
    view = subparsers.add_parser(
        'view',
        help='Displays a configuration file'
    )
    view.set_defaults(command='view')

    view.add_argument('--fernet-key', type=str)
    view.add_argument('path', type=str, help='Config file path')


@setup_up_config
def command(arguments):
    with open(arguments.path, 'r') as fp:
        print(fp.read())
