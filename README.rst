Aumbry
======

.. image:: https://travis-ci.org/pyarmory/aumbry.svg?branch=master
    :target: https://travis-ci.org/pyarmory/aumbry
    :alt: Travis CI Build

.. image:: http://codecov.io/github/pyarmory/aumbry/coverage.svg?branch=master
    :target: http://codecov.io/github/pyarmory/aumbry?branch=master
    :alt: Coverage

.. image:: https://readthedocs.org/projects/aumbry/badge/?version=latest
    :target: https://readthedocs.org/projects/aumbry/?badge=latest

.. image:: https://codeclimate.com/github/pyarmory/aumbry/badges/gpa.svg
   :target: https://codeclimate.com/github/pyarmory/aumbry
   :alt: Code Climate


Aumbry is general purpose library for handling configuration within your
Python applications. The project was born from constantly needing a simple
interface for configuration models that came from multiple data sources.

Behind the scenes, Aumbry uses Alchemize to handle the conversion of the
configuration data into application specific data models for your project.

**Data Sources supported:**

* File
* Consul
* Etcd2
* AWS Parameter Store

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

    # Install etcd2 support
    pip install aumbry['etcd2']

    # Install yaml support
    pip install aumbry['yaml']

    # Install parameter store dependencies
    pip install aumbry['param_store']

    # Installing multiple dependencies
    pip install aumbry['etcd2','yaml']
