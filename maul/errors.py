class MaulError(Exception):
    def __init__(self, message):
        self.message = message


class LoadError(MaulError):
    pass


class ParsingError(MaulError):
    pass


class DependencyError(MaulError):
    def __init__(self, maul_extras_name):
        msg = (
            'Dependencies unavailable: run "pip install maul[{}]" to acquire '
            'to appropriate dependencies.'
        ).format(
            maul_extras_name
        )
        super(DependencyError, self).__init__(msg)


class UnknownHandlerError(MaulError):
    def __init__(self, name):
        super(UnknownHandlerError, self).__init__(
            'Couldn\'t find a handler with the name: {}'.format(name)
        )
