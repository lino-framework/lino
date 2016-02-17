"""If you want to see which version of Lino you have, you can say
"hello" to Lino:

.. code-block:: bash

    $ python -m lino.hello

This command just issues a text with the version number of Lino (and
its dependencies) to the console::

    Lino 1.6.15, Django 1.6.7, Python 2.7.4, Babel 1.3, Jinja 2.7.2, Sphinx 1.3a0, python-dateutil 2.1, OdfPy ODFPY/0.9.6, docutils 0.11, suds 0.4, PyYaml 3.10, Appy 0.9.0 (2014/06/23 22:15).

"""
from __future__ import print_function

from lino.api.ad import Site
print(Site().using_text())
