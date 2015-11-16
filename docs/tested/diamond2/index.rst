.. _lino.tested.diamond2:

===============================
Diamond inheritance (continued)
===============================

.. This document is part of the test suite.  
   To test only this  document, run:

    $ python setup.py test -s tests.DocsTests.test_diamond2

    doctest init:

    >>> from __future__ import print_function

This document shows a case of multi-table diamond inheritance which
was caused problems in Django 1.7.  The difference with
:doc:`../diamond/index` is that now we have two abstract parents.

This document also shows that Lino has a work-around for both
problems. Unfortunately that workaround works only until Django
1.6. We had some fun to adapt it to newer Django versions.

The source code used to generate and test this document is at
:srcref:`docs/tested/diamond2/`.


Our database structure is defined in :file:`main/models.py` as
follows:

.. literalinclude:: main/models.py


The problem
===========


>>> from main.models import PizzeriaBar
>>> p = PizzeriaBar(name="A", min_age="B", specialty="C",
...     pizza_bar_specific_field="Doodle")

Despite the fact that we specify a non-blank value for `name`, we get
a database object whose `name` is blank, while the
`pizza_bar_specific_field` field is not:

>>> print(p.name)
<BLANKLINE>
>>> print(p.pizza_bar_specific_field)
Doodle


.. include:: django16.rst
.. include:: django17.rst


.. toctree::
    :hidden:

    django16
    django17
