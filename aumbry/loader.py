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
    """Loads a configration from a source into the specified Config type

    Args:
        source_name (str): The name of the desired source.
        config_class (AumbryConfig): The resulting class of configuration you
            wish to deserialize the data into.
        options (dict, optional): The options used by the source handler. The
            keys are determined by each source handler. Refer to your source
            handler documentation on what options are available.
        search_paths (list, optional): A list paths for custom source handlers

    Returns:
        An instance of the passed in config_class
    """
    source_cls = find_source(source_name, search_paths)
    if not source_cls:
        raise UnknownSourceError(source_name)

    source = source_cls(options)
    handler = config_class.__handler__()

    source.import_requirements()
    handler.import_requirements()

    cfg_data = source.fetch_config_data()
    return handler.deserialize(cfg_data, config_class)


def save(source_name, config_inst, options=None, search_paths=None):
    """Loads a configration from a source into the specified Config type

    Args:
        source_name (str): The name of the desired source.
        config_inst (AumbryConfig): The instance of a configuration class
            wish save.
        options (dict, optional): The options used by the source handler. The
            keys are determined by each source handler. Refer to your source
            handler documentation on what options are available.
        search_paths (list, optional): A list paths for custom source handlers
    """
    source_cls = find_source(source_name, search_paths)
    if not source_cls:
        raise UnknownSourceError(source_name)

    source = source_cls(options)
    handler = config_inst.__handler__()

    source.import_requirements()
    handler.import_requirements()

    data = handler.serialize(config_inst)
    return source.save_config_data(data, handler)
