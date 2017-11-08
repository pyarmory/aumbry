import argparse

from aumbry.cli import upload, edit, view


def parse_arguments(argv=None):
    parser = argparse.ArgumentParser(
        'aumbry',
        description='CLI Tool for Aumbry'
    )

    subparsers = parser.add_subparsers()

    upload.setup_arguments(subparsers)
    edit.setup_arguments(subparsers)
    view.setup_arguments(subparsers)

    return parser.parse_args(argv)


def main(argv=None):
    arguments = parse_arguments(argv)
    commands = {
        'upload': upload.command,
        'edit': edit.command,
        'view': view.command,
    }

    return commands[arguments.command](arguments)
