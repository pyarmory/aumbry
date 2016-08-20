import abc
import copy
import os
import six


@six.add_metaclass(abc.ABCMeta)
class AbstractHandler(object):
    def __init__(self, options=None):
        self.options = options or {}

        self.vars = {}
        self.vars.update(self.environmental_vars)
        self.vars.update(self.options)

    @abc.abstractmethod
    def fetch_config_data(self):
        """ Retrieves configuration data from pre-configured location. """

    @abc.abstractmethod
    def deserialize(self, raw_config, config_cls):
        """ Method to handle deserialization to a Config object. """

    @abc.abstractmethod
    def serialize(self, config):
        """ Method to handle serialization to a string. """

    @abc.abstractproperty
    def environment_var_prefix(self):
        """ The prefix of all environmental variables to fetch. """

    @property
    def environmental_vars(self):
        keys_to_fetch = [
            key for key in os.environ.keys()
            if key.startswith(self.environment_var_prefix)
        ]

        return {key: os.environ[key] for key in keys_to_fetch}
