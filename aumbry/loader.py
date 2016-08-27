from aumbry.contract import AbstractSource
from aumbry.errors import UnknownSourceError
from pike.discovery import py
from pike.manager import PikeManager


def find_plugin(name, base_cls, search_paths):
    with PikeManager(search_paths) as mgr:
        handlers = mgr.get_all_inherited_classes(base_cls)

        for handler in handlers:
            if handler.extras_name == name:
                return handler


def find_source(name, search_paths=None):
    if not search_paths:
        search_paths = py.get_module_by_name('aumbry.sources').__path__

    return find_plugin(name, AbstractSource, search_paths)


def load(source_name, config_class, options=None, search_paths=None):
    source_cls = find_source(source_name, search_paths)
    if not source_cls:
        raise UnknownSourceError(source_name)

    source = source_cls(options)
    handler = config_class.__handler__()

    source.import_requirements()
    handler.import_requirements()

    cfg_data = source.fetch_config_data()
    return handler.deserialize(cfg_data, config_class)
