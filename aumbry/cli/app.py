import argparse

from aumbry.cli import upload, edit


def parse_arguments(argv=None):
    parser = argparse.ArgumentParser(
        'aumbry',
        description='CLI Tool for Aumbry'
    )

    subparsers = parser.add_subparsers()

    upload.setup_arguments(subparsers)
    edit.setup_arguments(subparsers)

    return parser.parse_args(argv)


def main(argv=None):
    arguments = parse_arguments(argv)
    code = None

    if arguments.command == 'upload':
        code = upload.command(arguments)

    elif arguments.command == 'edit':
        code = edit.command(arguments)

    return code
