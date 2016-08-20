class LoadError(Exception):
    pass


class ParsingError(Exception):
    pass


class DependencyError(Exception):
    def __init__(self, maul_extras_name):
        msg = (
            'Dependencies unavailable: run "pip install maul[{}]" to acquire '
            'to appropriate dependencies.'
        ).format(
            maul_extras_name
        )
        super(DependencyError, self).__init__(msg)
