asynccli
========

.. image:: https://img.shields.io/pypi/v/asynccli.svg
    :target: https://pypi.python.org/pypi/asynccli
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/ahopkins/asynccli.png
   :target: https://travis-ci.org/ahopkins/asynccli
   :alt: Latest Travis CI build status

A CLI framework based on asyncio.

.. note:: This is still in **active** development. Things will change.

Usage
-----

The simplest usage is to just pass in an `async` function.

.. code:: python

    import asynccli


    async def mycli():
        print("Hello, world.")


    if __name__ == '__main__':
        app = asynccli.App(mycli)
        app.run()


It can also be instantiated as a class, as long it has a `call` method.

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

Installation
------------

    pip install asynccli

Requirements
^^^^^^^^^^^^

Currently it requires Python 3.5 to make use of `async`/`await`

License
-------

`MIT <https://github.com/ahopkins/asynccli/blob/master/LICENSE>`_

Authors
-------

`asynccli` was written by `Adam Hopkins <admhpkns@gmail.com>`_.
.
