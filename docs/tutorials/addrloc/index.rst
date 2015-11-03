.. _tutorials.addrloc:

==================================
An introduction to AddressLocation
==================================

.. How to run only this test:

  $ python setup.py test -s tests.DocsTests.test_addrloc


Here is the :xfile:`models.py` file which we will use in this
tutorial:

.. literalinclude:: models.py

Here is the data we use to fill our database:

.. literalinclude:: fixtures/demo.py
  
You can initialize your demo database by running::

  $ python manage.py initdb_demo

.. This document does the equivalent:

    >>> from django.core.management import call_command
    >>> call_command('initdb_demo', interactive=False, verbosity=0)

Here are the tables we are going to use in this tutorial:

.. literalinclude:: ui.py

Here is our ``Companies`` table in a testable console format:

>>> from lino.api.shell import *
>>> rt.show(addrloc.Companies)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
======== ======================================
 Name     Address
-------- --------------------------------------
 First    Favrunpark 13, 4700 Eupen
 Second   Tartu mnt 71, 10115 Tallinn, Estonia
======== ======================================
<BLANKLINE>


>>> tpl = "{name}\n{addr}\n----------"
>>> for obj in addrloc.Company.objects.all():
...     print tpl.format(name=obj.name, addr=obj.address_location())
First
Favrunpark 13
4700 Eupen
----------
Second
Tartu mnt 71
10115 Tallinn
Estonia
----------
