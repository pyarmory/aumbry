from aumbry.contract import AbstractHandler
from aumbry.errors import UnknownHandlerError
from pike.discovery import py
from pike.manager import PikeManager


def find_handler(name, search_paths=None):
    if not search_paths:
        search_paths = py.get_module_by_name('aumbry.formats').__path__

    with PikeManager(search_paths) as mgr:
        handlers = mgr.get_all_inherited_classes(AbstractHandler)

        for handler in handlers:
            if handler.extras_name == name:
                return handler


def load(format_name, config_class, options=None, search_paths=None):
    handler_cls = find_handler(format_name, search_paths)
    if not handler_cls:
        raise UnknownHandlerError(format_name)

    handler = handler_cls(options)
    handler.import_requirements()

    cfg_data = handler.fetch_config_data()
    return handler.deserialize(cfg_data, config_class)
