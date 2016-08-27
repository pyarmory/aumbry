Using Aumbry
============

Dependencies
------------
Many developers are very conscious of the number of dependencies that they
include in their projects. To that end, Aumbry doesn't install the dependencies
for parsing yaml or loading from consul by default. However, Aumbry attempts
to make this relatively easy on users by enabling users to easily install
the extra dependencies using the following convention:

.. code-block:: bash

    # For Consul dependencies
    pip install aumbry['consul']

    # For Yaml dependencies
    pip install aumbry['yaml']


Loading from a File
-------------------
One of the simplest and most common way of loading configuration is from a
file. For this example, we'll use a JSON configuration file.

Lets say we have the following JSON configuration that we want to load

.. code-block:: json

    {
        "something": "it works!"
    }


The next steps are to define a configuration class that matches what we're
trying to do and load the config up.

.. code-block:: python

    import aumbry


    class SampleConfig(aumbry.JsonConfig):
        __mapping__ = {
            'something': ['something', str],
        }


    # You can either specify the options here or via environment variables
    options = {
        'CONFIG_FILE_PATH': './my_config.json',
    }

    # Time to load it up!
    config = aumbry.load(aumbry.FILE, SampleConfig, options)

    print(config.something) # it works!

File Options
^^^^^^^^^^^^^^
Like all options, these can be manually specified when calling ``load()``
or via environment variables.

===================== ========== ============================
       Key             Default   Notes
===================== ========== ============================
CONFIG_FILE_PATH                  Required
===================== ========== ============================


Loading from Consul
-------------------

As mentioned under the Dependencies section, the dependencies to load from
consul are not included by default. As a result, we need to first install
our extra dependencies.

.. code-block:: shell

    pip install aumbry['consul']

Much like our loading from a file example, we need a configuration class and
set our options for the Consul source.

.. code-block:: python

    import aumbry


    class SampleConfig(aumbry.JsonConfig):
        __mapping__ = {
            'something': ['something', str],
        }


    # You can either specify the options here or via environment variables
    options = {
        'CONSUL_URI': 'http://myhost:8500',
        'CONSUL_KEY': 'test',
    }

    # Time to load it up!
    config = aumbry.load(aumbry.CONSUL, SampleConfig, options)

    print(config.something) # it works!

It is important to note that the Consul source will block until it either
cannot load, reaches max retries, or successfully loads.

Consul Options
^^^^^^^^^^^^^^
Like all options, these can be manually specified when calling ``load()``
or via environment variables.

===================== ========== ============================
       Key             Default   Notes
===================== ========== ============================
CONSUL_URI                       Required
CONSUL_KEY                       Required
CONSUL_TIMEOUT            10     Timeout per-request
CONSUL_RETRY_MAX           1     Number of retries to attempt
CONSUL_RETRY_INTERVAL     10     Wait period between retries
===================== ========== ============================


Building Configuration Models
-----------------------------
Because Aumbry uses Alchemize_ for model de/serialization, it's just a matter
of defining out the models in the Alchemize method.

Example Yaml Configuration

.. code-block:: yaml

    ---
    base-uri: http://localhost
    database:
      servers:
        - localhost:5432
      username: postgres
      password: something
      name: app

Example Code Load and Parse that config

.. code-block:: python

    import aumbry


    class DatabaseConfig(aumbry.YamlConfig):
        __mapping__ = {
            'servers': ['servers', list],
            'username': ['username', str],
            'password': ['password', str],
            'database': ['database', str]
        }


    class AppConfig(aumbry.YamlConfig):
        __mapping__ = {
            'base-uri': ['base_uri', str],
            'database': ['database', DatabaseConfig],
        }


    cfg = aumbry.load(
        aumbry.FILE,
        AppConfig,
        {
            'CONFIG_FILE_PATH': '/etc/app/config.yml'
        }
    )

    print(cfg.database.username) # postgres

One of the things you might have noticed is that the explicit mapping allows
for us to take an attribute name such as ``base-uri`` which isn't compatible
with Python, and map it over to ``base_uri``.

More details can be found on building your mappings in the Alchemize_
documentation.

.. _Alchemize: https://alchemize.readthedocs.io/en/latest/
