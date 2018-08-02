Developer Setup
===============

Requirements
------------

The following are required to build the docs.

.. literalinclude:: ../requirements.txt

Install
-------
Clone and install the repository::

    git clone https://github.com/t-makaro/animatplot.git
    cd animatplot
    pip install -e .

Testing
-------

From the root animatplot directory simply run::

    pytest

.. warning::

    Tests are currently very limited. Please run examples to ensure everything works.

Linting
-------

This project currently uses ``pycodestyle`` for linting.

