asynccli
========

.. image:: https://img.shields.io/pypi/v/asynccli.svg
    :target: https://pypi.python.org/pypi/asynccli
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/status/asynccli.svg
    :target: https://pypi.python.org/pypi/asynccli
    :alt: Version status

.. image:: https://img.shields.io/pypi/pyversions/asynccli.svg
    :target: https://pypi.python.org/pypi/asynccli
    :alt: Python 3.5 and 3.6

.. image:: https://travis-ci.org/ahopkins/asynccli.svg?branch=master
    :target: https://travis-ci.org/ahopkins/asynccli
    :alt: Latest Travis CI build status

.. image:: https://api.codacy.com/project/badge/Grade/b6f3abd70b6a4ead91c4b0bb820e1ddd
    :target: https://www.codacy.com/app/ahopkins/asynccli?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ahopkins/asynccli&amp;utm_campaign=Badge_Grade
    :alt: Codacy grade

.. image:: https://api.codacy.com/project/badge/Coverage/b6f3abd70b6a4ead91c4b0bb820e1ddd
    :target: https://www.codacy.com/app/ahopkins/asynccli?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ahopkins/asynccli&amp;utm_campaign=Badge_Coverage
    :alt: Codacy coverage

A CLI framework based on asyncio.

.. note:: This is still in **active** development. Things will change. For now, the basic framework is operational. If you are interested in helping out, or would like to see any particular features added, let me know.

Usage
-----

The simplest usage is to just pass in an ``async`` function.

.. code:: python

    import asynccli


    async def mycli():
        print("Hello, world.")


    if __name__ == '__main__':
        app = asynccli.App(mycli)
        app.run()


It can also be instantiated as a class, as long it has a ``call`` method.

.. code:: python

    import asynccli


    class DivisionCalculator(asynccli.CLI):
        numerator = asynccli.Integer(help_text='This is the numerator.')
        denominator = asynccli.Integer()

        async def call(self):
            print(self.first_num / self.second_num)


    if __name__ == '__main__':
        app = asynccli.App(DivisionCalculator)
        app.run()

In the ``DivisionCalculator`` example above, you would call your script like this:

.. code::

    $ /path/to/script.py 2 3
    0.6666666666666666

What if you want to have a tiered CLI with a hierarchy of commands? First, create your command by subclassing ``CLI`` as above. Then, wrap the whole thing inside of the ``TieredCLI`` class, and pass that to the ``App``.

.. code:: python

    class Calculator(asynccli.TieredCLI):
        d = DivisionCalculator

Now, to invoke the script, you have an extra argument to call:

.. code::

    $ /path/to/script.py d 2 3
    0.6666666666666666

Installation
------------

.. code::

    pip install asynccli

Requirements
------------

Currently it requires Python 3.5 to make use of ``async``/``await``. It uses ``argparse`` under the hood, and therefore has **no dependencies** outside of the standard library.

Roadmap
-------

- Additional ``Argument`` types
- Integration of additional ``argparse`` features
- Add ``uvloop``
- Better support for help documentation

License
-------

`MIT <https://github.com/ahopkins/asynccli/blob/master/LICENSE>`_

Authors
-------

``asynccli`` was written by `Adam Hopkins <admhpkns@gmail.com>`_.
