CLI Documentation
=================

.. warning::

    This is an unstable feature of aumbry. Use with discretion!

Installation
------------

The Aumbry command-line interface is available as an extra requirement available
on PyPI.

.. code-block:: bash

    pip install aumbry[cli]


Usage
-----

.. code-block:: bash

    usage: aumbry [-h] {upload,edit} ...

    CLI Tool for Aumbry

    positional arguments:
      {upload,edit}
        upload       Uploads a configuration file
        edit         Edits a configuration file

    optional arguments:
      -h, --help     show this help message and exit

Upload
^^^^^^

The upload sub-command allows for you to push up a configuration.

.. code-block:: bash

    aumbry upload \
        --file-type yml \
        --param-store-region us-east-1 \
        --param-store-prefix /my/aws/prefix \
        ./path/to/my/config.yml \
        my.aumbry.config:ConfigClass \
        parameter_store


Edit
^^^^

The edit sub-command enabled you to open up your configuration file.

.. code-block:: bash

    aumbry edit ./path/to/my/config.yml


Encrypted Configuration
-----------------------

Encryption and Decryption of configuration happens using Cryptography's
Fernet capability. To use this functionality, provide your key
via the ``--fernet-key`` cli option.

