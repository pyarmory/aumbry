from maul.contract import AbstractHandler
from maul.errors import UnknownHandlerError
from pike.discovery import py
from pike.manager import PikeManager


def find_handler(name, search_path=None):
    if not search_path:
        search_path = py.get_module_by_name('maul.contrib').__path__

    with PikeManager(search_path) as mgr:
        handlers = mgr.get_all_inherited_classes(AbstractHandler)

        for handler in handlers:
            if handler.extras_name == name:
                return handler


def load(format_name, config_class, options=None, search_path=None):
    handler_cls = find_handler(format_name, search_path)
    if not handler_cls:
        raise UnknownHandlerError(format_name)

    handler = handler_cls(options)
    handler.import_requirements()

    cfg_data = handler.fetch_config_data()
    return handler.deserialize(cfg_data, config_class)
