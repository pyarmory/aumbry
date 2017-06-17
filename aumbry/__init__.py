"""
Attributes:
    FILE (str): Alias of SourceTypes.file
    CONSUL (str): Alias of SourceTypes.consul
"""
from .loader import load, save # NOQA
from .formats.js import JsonConfig # NOQA
from .formats.yml import YamlConfig # NOQA
from .sources import SourceTypes

from alchemize.mapping import Attr # NOQA

FILE = SourceTypes.file
CONSUL = SourceTypes.consul
ETCD2 = SourceTypes.etcd2


__all__ = [
    'Attr',
    'load',
    'save',
    'JsonConfig',
    'YamlConfig',
    'SourceTypes',
]
