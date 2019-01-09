from alchemize.transmute import JsonTransmuter
from aumbry.contract import AbstractSource
from aumbry.errors import UnknownSourceError
import deepmerge
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


def load(source_name, config_class, options=None, search_paths=None,
         preprocessor=None, handler=None):
    """Loads a configuration from a source into the specified Config type

    Args:
        source_name (str): The name of the desired source.
        config_class (AumbryConfig): The resulting class of configuration you
            wish to deserialize the data into.
        options (dict, optional): The options used by the source handler. The
            keys are determined by each source handler. Refer to your source
            handler documentation on what options are available.
        search_paths (list, optional): A list paths for custom source handlers
        preprocessor (function): A function that pre-processes the source
            data before loading into the configuration object.
        handler (AbstractHandler): An instance of a handler to process the
            configuration data.

    Returns:
        An instance of the passed in config_class
    """
    source_cls = find_source(source_name, search_paths)
    if not source_cls:
        raise UnknownSourceError(source_name)

    source = source_cls(options)

    if not handler:
        handler = config_class.__handler__()

    source.import_requirements()
    handler.import_requirements()

    cfg_data = source.fetch_config_data(config_class)

    if preprocessor:
        cfg_data = preprocessor(cfg_data)

    return handler.deserialize(cfg_data, config_class)


def merge(config_class, sources, preprocessor=None, handler=None):
    """Loads a configuration from multiple sources into the specified Config
    type. Each source has to be the same type.

    Args:
        config_class (AumbryConfig): The resulting class of configuration you
            wish to deserialize the data into.
        sources: an iterable collection of dicts with with the following keys:
            source_name (str): The name of the desired source.
            options (dict, optional): The options used by the source handler.
                The keys are determined by each source handler. Refer to your
                source handler documentation on what options are available.
            search_paths (list, optional): A list paths for custom source
                handlers
        preprocessor (function): A function that pre-processes the source
            data before loading into the configuration object.
        handler (AbstractHandler): An instance of a handler to process the
            configuration data.

    Returns:
        An instance of the passed in config_class
    """
    if not handler:
        handler = config_class.__handler__()
    handler.import_requirements()

    cfg_data = {}
    cfg_merger = deepmerge.Merger(
        [
            (list, ["override"]),
            (dict, ["merge"])
        ],
        ["override"],
        ["override"]
    )
    for source_data in sources:
        source_cls = find_source(source_data['source_name'],
                                 source_data.get('search_paths'))
        if not source_cls:
            raise UnknownSourceError(source_data['source_name'])

        source = source_cls(source_data.get('options'))
        source.import_requirements()
        source_cfg_raw = source.fetch_config_data(config_class)

        if preprocessor:
            source_cfg_raw = preprocessor(source_cfg_raw)

        source_cfg_data = handler.parse(source_cfg_raw)
        cfg_data = cfg_merger.merge(cfg_data, source_cfg_data)

    return JsonTransmuter.transmute_from(cfg_data, config_class)


def save(source_name, config_inst, options=None, search_paths=None,
         preprocessor=None, handler=None):
    """Loads a configuration from a source into the specified Config type

    Args:
        source_name (str): The name of the desired source.
        config_inst (AumbryConfig): The instance of a configuration class
            wish save.
        options (dict, optional): The options used by the source handler. The
            keys are determined by each source handler. Refer to your source
            handler documentation on what options are available.
        search_paths (list, optional): A list paths for custom source handlers
        preprocessor (function): A function that pre-processes the configration
            data before saving to the source.
        handler (AbstractHandler): An instance of a handler to process the
            configuration data. Defaults to the configuration handler.

    """
    source_cls = find_source(source_name, search_paths)
    if not source_cls:
        raise UnknownSourceError(source_name)

    source = source_cls(options)

    if not handler:
        handler = config_inst.__handler__()

    source.import_requirements()
    handler.import_requirements()

    data = handler.serialize(config_inst)

    if preprocessor:
        data = preprocessor(data)

    return source.save_config_data(data, handler, config_inst)
