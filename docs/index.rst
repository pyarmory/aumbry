Welcome to Aumbry's documentation!
==================================

Aumbry is general purpose library for handling configuration within your
Python applications. The project was born from constantly needing a simple
interface for configuration models that came from multiple data sources.

Behind the scenes, Aumbry uses Alchemize_ to handle the conversion of the
configuration data into application specific data models for your project.

Installation
------------

Aumbry is available on PyPI

.. code-block:: bash

    # Install aumbry core
    pip install aumbry

    # For Consul dependencies
    pip install aumbry['consul']

    # For Etcd2 dependencies
    pip install aumbry['etcd2']

    # For Yaml dependencies
    pip install aumbry['yaml']

Contents:

.. toctree::
   :maxdepth: 2

   using
   api

.. _Alchemize: https://alchemize.readthedocs.io

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

