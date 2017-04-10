class AumbryError(Exception):
    def __init__(self, message):
        self.message = message
        super(AumbryError, self).__init__(message)


class LoadError(AumbryError):
    pass


class SaveError(AumbryError):
    pass


class ParsingError(AumbryError):
    pass


class DependencyError(AumbryError):
    def __init__(self, extras_name):
        msg = (
            'Dependencies unavailable: run "pip install aumbry[{}]" to '
            'acquire to appropriate dependencies.'
        ).format(
            extras_name
        )
        super(DependencyError, self).__init__(msg)


class UnknownSourceError(AumbryError):
    def __init__(self, name):
        super(UnknownSourceError, self).__init__(
            'Couldn\'t find a source with the name: {}'.format(name)
        )
