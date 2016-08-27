Aumbry
======

Aumbry is general purpose library for handling configuration within your
Python applications. The project was born from constantly needing a simple
interface for configuration models that came from multiple data sources.

Behind the scenes, Aumbry uses Alchemize to handle the conversion of the
configuration data into application specific data models for your project.

**Data Sources supported:**

* File
* Consul

**Configuration Formats Supported:**

* Yaml
* Json

Installation
------------

.. code-block:: shell

    # Install base package
    pip install aumbry

    # Install consul support
    pip install aumbry['consul']

    # Install yaml support
    pip install aumbry['yaml']
