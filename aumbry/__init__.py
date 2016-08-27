"""
Attributes:
    FILE (str): Alias of SourceTypes.file
    CONSUL (str): Alias of SourceTypes.consul
"""
from .loader import load # NOQA
from .formats.js import JsonConfig # NOQA
from .formats.yml import YamlConfig # NOQA
from .sources import SourceTypes

FILE = SourceTypes.file
CONSUL = SourceTypes.consul


__all__ = [
    'load',
    'JsonConfig',
    'YamlConfig',
    'SourceTypes',
]
